<script setup lang="ts">
import { getAvailableTags, buildApiQuery, buildUrlQuery, toggleTag } from '~/utils/filters'

useSeo({
  title: 'EducaTYCs — Cursos, becas y talleres gratuitos en línea',
  description: 'Más de 1,600 oportunidades educativas gratuitas en español: cursos, becas y talleres de universidades e instituciones reconocidas para hispanohablantes de todo el mundo.',
  path: '/',
})

useHead({
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'WebSite',
        name: 'EducaTYCs',
        url: 'https://educatycs.mx',
        description: 'Plataforma gratuita de oportunidades educativas en línea para hispanohablantes.',
        inLanguage: 'es',
        potentialAction: {
          '@type': 'SearchAction',
          target: 'https://educatycs.mx/?search={search_term_string}',
          'query-input': 'required name=search_term_string',
        },
      }),
    },
  ],
})

const route = useRoute()
const router = useRouter()

const search = ref((route.query.search as string) ?? '')
const type = ref((route.query.opportunity_type as string) ?? '')
const source = ref((route.query.source as string) ?? '')
const tag = ref((route.query.tag as string) ?? '')
const page = ref(Number(route.query.page) || 1)

// View mode: grid | list
const viewMode = ref<'grid' | 'list'>('grid')
onMounted(() => {
  const stored = localStorage.getItem('viewMode')
  if (stored === 'grid' || stored === 'list')
    viewMode.value = stored
})
watch(viewMode, v => localStorage.setItem('viewMode', v))

const LIMIT = 24

const query = computed(() =>
  buildApiQuery(search.value, type.value, source.value, tag.value, page.value, LIMIT),
)

const totalQuery = computed(() => ({
  search: search.value || undefined,
  opportunity_type: type.value || undefined,
  source: source.value || undefined,
  tag: tag.value || undefined,
}))

const { data: opportunities, status, error } = useOpportunities(query)
const { data: sources } = useSources()
const { data: totalData } = useOpportunitiesTotal(totalQuery)

// Check which optional types have no data to hide them from the filter
const { data: eventTotal } = useOpportunitiesTotal(ref({ opportunity_type: 'event' }))
const { data: otherTotal } = useOpportunitiesTotal(ref({ opportunity_type: 'other' }))
const hiddenTypes = computed(() => {
  const hidden: string[] = []
  if (!eventTotal.value?.total) hidden.push('event')
  if (!otherTotal.value?.total) hidden.push('other')
  return hidden
})

const totalPages = computed(() => {
  const total = totalData.value?.total ?? 0
  return total > 0 ? Math.ceil(total / LIMIT) : null
})

const availableTags = computed(() =>
  getAvailableTags(opportunities.value ?? []),
)

function clearFilters() {
  search.value = ''
  type.value = ''
  source.value = ''
  tag.value = ''
}

function syncQueryParams() {
  router.replace({
    query: buildUrlQuery(search.value, type.value, source.value, tag.value, page.value),
  })
}

watch([search, type, source, tag], () => {
  page.value = 1
  syncQueryParams()
})

watch(page, syncQueryParams)
</script>

<template>
  <div>
    <HeroCarousel />

    <main class="mx-auto max-w-[1440px] px-4 py-10 sm:px-8 lg:px-[120px]">
      <h1 class="text-2xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-3xl">Oportunidades educativas</h1>
      <p class="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-200 sm:text-base">
        Cursos, becas y talleres gratuitos en línea para hispanohablantes
      </p>

      <FilterBar
        class="mt-6"
        :search="search"
        :type="type"
        :source="source"
        :tag="tag"
        :sources="sources ?? []"
        :hidden-types="hiddenTypes"
        @update:search="search = $event"
        @update:type="type = $event"
        @update:source="source = $event"
        @clear="clearFilters"
      />

      <!-- Tags + view toggle row -->
      <div class="mt-3 flex items-start justify-between gap-3">
        <div v-if="availableTags.length" role="group" aria-label="Filtrar por tema" class="flex flex-wrap gap-2">
          <button
            v-for="t in availableTags"
            :key="t"
            type="button"
            :aria-pressed="tag === t"
            :aria-label="`Filtrar por ${t}`"
            class="rounded-full border px-3 py-1 text-xs font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:ring-offset-0"
            :class="tag === t
              ? 'border-cyan-400/50 bg-cyan-400/15 text-cyan-700 dark:border-cyan-300 dark:bg-cyan-300/18 dark:text-cyan-100'
              : 'border-slate-200 bg-white/60 text-slate-600 hover:border-fuchsia-300/60 hover:text-fuchsia-600 dark:border-white/25 dark:bg-slate-900/50 dark:text-slate-100 dark:hover:border-fuchsia-300/40 dark:hover:text-fuchsia-100'"
            @click="tag = toggleTag(tag, t)"
          >
            {{ t }}
          </button>
        </div>
        <div v-else class="flex-1" />

        <!-- View toggle -->
        <div class="flex shrink-0 items-center gap-0.5 rounded-lg border border-slate-200 p-1 dark:border-white/15">
          <button
            type="button"
            aria-label="Vista cuadrícula"
            class="rounded p-1.5 transition-colors"
            :class="viewMode === 'grid' ? 'bg-slate-100 text-slate-700 dark:bg-white/15 dark:text-white' : 'text-slate-400 hover:text-slate-600 dark:text-slate-500 dark:hover:text-slate-300'"
            @click="viewMode = 'grid'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M3 3h7v7H3V3zm11 0h7v7h-7V3zM3 14h7v7H3v-7zm11 0h7v7h-7v-7z" />
            </svg>
          </button>
          <button
            type="button"
            aria-label="Vista lista"
            class="rounded p-1.5 transition-colors"
            :class="viewMode === 'list' ? 'bg-slate-100 text-slate-700 dark:bg-white/15 dark:text-white' : 'text-slate-400 hover:text-slate-600 dark:text-slate-500 dark:hover:text-slate-300'"
            @click="viewMode = 'list'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Loading skeleton -->
      <template v-if="status === 'pending'">
        <div v-if="viewMode === 'grid'" class="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          <OpportunityCardSkeleton v-for="i in 8" :key="i" />
        </div>
        <div v-else class="mt-8 space-y-2">
          <OpportunityCardSkeleton v-for="i in 8" :key="i" compact />
        </div>
      </template>

      <AppError v-else-if="error" class="mt-6" />

      <p v-else-if="opportunities?.length === 0" class="mt-10 text-center text-sm text-slate-500 dark:text-slate-200">
        No se encontraron oportunidades con estos filtros.
      </p>

      <template v-else>
        <div v-if="viewMode === 'grid'" class="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          <OpportunityCard
            v-for="item in opportunities"
            :key="item.id"
            :opportunity="item"
          />
        </div>
        <div v-else class="mt-8 space-y-2">
          <OpportunityCard
            v-for="item in opportunities"
            :key="item.id"
            :opportunity="item"
            compact
          />
        </div>
      </template>

      <nav v-if="opportunities?.length" aria-label="Paginación" class="mt-10 flex items-center justify-center gap-4">
        <button
          type="button"
          :disabled="page === 1"
          :aria-label="`Ir a la página anterior (página ${page - 1})`"
          class="rounded-md border border-slate-200 bg-white px-4 py-2 text-sm text-slate-700 transition-colors hover:border-cyan-400 hover:text-cyan-600 disabled:cursor-not-allowed disabled:opacity-40 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:ring-offset-0 dark:border-white/35 dark:bg-white/10 dark:text-slate-100 dark:hover:border-cyan-300 dark:hover:text-cyan-200"
          @click="page--"
        >
          Anterior
        </button>
        <span aria-current="page" class="text-sm text-slate-600 dark:text-slate-200">
          Página {{ page }}{{ totalPages ? ` de ${totalPages}` : '' }}
        </span>
        <button
          type="button"
          :disabled="opportunities.length < LIMIT || (totalPages !== null && page >= totalPages)"
          :aria-label="`Ir a la página siguiente (página ${page + 1})`"
          class="rounded-md border border-slate-200 bg-white px-4 py-2 text-sm text-slate-700 transition-colors hover:border-cyan-400 hover:text-cyan-600 disabled:cursor-not-allowed disabled:opacity-40 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:ring-offset-0 dark:border-white/35 dark:bg-white/10 dark:text-slate-100 dark:hover:border-cyan-300 dark:hover:text-cyan-200"
          @click="page++"
        >
          Siguiente
        </button>
      </nav>
      <!-- ¿Qué sigue? — card compacto -->
      <aside class="mt-14 rounded-2xl border border-violet-300/25 bg-gradient-to-br from-violet-500/8 via-cyan-500/5 to-fuchsia-500/8 p-8 dark:from-violet-500/10 dark:via-cyan-500/8 dark:to-fuchsia-500/10">
        <div class="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
          <div class="space-y-2">
            <p class="text-xs font-semibold uppercase tracking-widest text-violet-600 dark:text-violet-300">El futuro de EducaTYCs</p>
            <h2 class="text-xl font-bold text-slate-900 dark:text-white">¿Qué viene después?</h2>
            <p class="max-w-xl text-sm leading-7 text-slate-600 dark:text-slate-200">
              Próximamente: alertas de convocatorias, más fuentes y filtros avanzados. Y si los donativos lo permiten, una <strong class="text-slate-900 dark:text-white">app móvil para Android e iOS</strong> para que ningún hispanohablante se pierda una oportunidad por falta de acceso.
            </p>
          </div>
          <div class="flex shrink-0 flex-col gap-3 sm:items-end">
            <NuxtLink
              to="/acerca-de#roadmap"
              class="inline-flex items-center gap-2 rounded-lg border border-violet-300/40 px-4 py-2.5 text-sm font-semibold text-violet-700 transition-colors hover:bg-violet-400/10 dark:text-violet-300 dark:hover:bg-violet-400/10"
            >
              Ver hoja de ruta
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </NuxtLink>
            <a
              href="https://ko-fi.com/educatycs"
              target="_blank"
              rel="noopener noreferrer"
              class="inline-flex items-center gap-2 rounded-lg border border-[#FF5E5B]/30 bg-[#FF5E5B]/10 px-4 py-2.5 text-sm font-semibold text-[#FF5E5B] transition-colors hover:bg-[#FF5E5B]/20 dark:border-[#FF5E5B]/40 dark:text-[#FF8C8A]"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 shrink-0" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M18.5 3H5.5C4.12 3 3 4.12 3 5.5v9C3 17.43 5.57 20 8.5 20h7c2.93 0 5.5-2.57 5.5-5.5V9h.5c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2h-.5zm0 5H19V5h-.5v3zM5.5 5h11v9.5C16.5 16.43 14.93 18 13 18H9C7.07 18 5.5 16.43 5.5 14.5V5z"/>
                <path d="M9 11c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1zm4 0c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1z"/>
              </svg>
              Apoyar en Ko-fi
            </a>
          </div>
        </div>
      </aside>

    </main>
  </div>
</template>
