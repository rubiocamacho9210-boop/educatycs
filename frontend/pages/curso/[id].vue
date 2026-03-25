<script setup lang="ts">
import type { Opportunity, OpportunityType } from '~/types/opportunity'

const route = useRoute()
const config = useRuntimeConfig()

const { data: opportunity, status, error } = await useFetch<Opportunity>(
  `/opportunities/${route.params.id}`,
  { baseURL: config.public.apiBase },
)

const typeLabels: Record<OpportunityType, string> = {
  course: 'Curso',
  workshop: 'Taller',
  scholarship: 'Beca',
  event: 'Evento',
  other: 'Programa',
}

useHead({
  title: computed(() => opportunity.value?.title ?? 'Detalle'),
})
</script>

<template>
  <main class="mx-auto max-w-3xl px-4 py-10">
    <!-- Volver -->
    <NuxtLink
      to="/"
      class="inline-flex items-center gap-1 text-sm text-slate-500 hover:text-cyan-600 dark:text-slate-300 dark:hover:text-cyan-200"
    >
      ← Volver al listado
    </NuxtLink>

    <!-- Loading -->
    <AppLoading v-if="status === 'pending'" class="mt-6" />

    <!-- Error / 404 -->
    <div v-else-if="error || !opportunity" class="mt-6">
      <AppError message="Oportunidad no encontrada. Puede que haya sido eliminada o el enlace sea incorrecto." />
      <NuxtLink to="/" class="mt-4 inline-block text-sm text-cyan-600 underline hover:text-cyan-700 dark:text-cyan-200 dark:hover:text-cyan-100">
        Volver al inicio
      </NuxtLink>
    </div>

    <!-- Contenido -->
    <article v-else class="glass-card mt-6 rounded-2xl p-6 sm:p-8">
      <!-- Encabezado -->
      <div class="flex flex-wrap items-center gap-2">
        <span class="rounded-full border border-cyan-300/30 bg-cyan-300/15 px-3 py-1 text-xs font-semibold text-cyan-700 dark:text-cyan-100">
          {{ typeLabels[opportunity.opportunity_type] }}
        </span>
        <span class="text-xs text-slate-500 dark:text-slate-300">{{ opportunity.location ?? 'Online' }}</span>
        <span v-if="opportunity.is_free" class="rounded-full border border-emerald-300/30 bg-emerald-300/15 px-3 py-1 text-xs font-semibold text-emerald-700 dark:text-emerald-100">
          Gratuito
        </span>
      </div>

      <h1 class="mt-4 text-2xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-3xl">{{ opportunity.title }}</h1>
      <p class="mt-1 text-sm font-medium text-slate-500 dark:text-slate-300">{{ opportunity.provider }}</p>

      <!-- Descripción -->
      <p v-if="opportunity.description" class="mt-6 text-sm leading-relaxed text-slate-600 dark:text-slate-100 sm:text-base">
        {{ opportunity.description }}
      </p>

      <!-- Fechas -->
      <dl v-if="opportunity.start_date || opportunity.end_date" class="mt-6 flex flex-wrap gap-6">
        <div v-if="opportunity.start_date">
          <dt class="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-300">Inicio</dt>
          <dd class="mt-1 text-sm text-slate-700 dark:text-slate-100">{{ opportunity.start_date }}</dd>
        </div>
        <div v-if="opportunity.end_date">
          <dt class="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-300">Cierre</dt>
          <dd class="mt-1 text-sm text-slate-700 dark:text-slate-100">{{ opportunity.end_date }}</dd>
        </div>
      </dl>

      <!-- Tags -->
      <div v-if="opportunity.tags.length" class="mt-6 flex flex-wrap gap-2">
        <span
          v-for="tag in opportunity.tags"
          :key="tag"
          class="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-medium text-slate-600 dark:border-white/25 dark:bg-slate-900/45 dark:text-slate-100"
        >
          {{ tag }}
        </span>
      </div>

      <!-- Fuente -->
      <p class="mt-6 text-xs text-slate-500 dark:text-slate-300">Fuente: {{ opportunity.provider }}</p>

      <!-- CTA -->
      <a
        :href="opportunity.source_url"
        target="_blank"
        rel="noopener noreferrer"
        :aria-label="`Ir al sitio oficial de ${opportunity.title} (abre en nueva pestaña)`"
        class="neon-btn mt-6 inline-flex items-center gap-2 rounded-md px-5 py-2.5 text-sm font-semibold transition-all focus:outline-none focus:ring-2 focus:ring-cyan-300 focus:ring-offset-0"
      >
        Ir al sitio oficial
        <svg aria-hidden="true" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
        </svg>
      </a>
    </article>
  </main>
</template>
