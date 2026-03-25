<script setup lang="ts">
import { hasActiveFilters } from '~/utils/filters'
import type { SourceInfo } from '~/types/opportunity'

const props = defineProps<{
  search: string
  type: string
  source: string
  tag: string
  sources: SourceInfo[]
  hiddenTypes?: string[]
}>()

const emit = defineEmits<{
  'update:search': [value: string]
  'update:type': [value: string]
  'update:source': [value: string]
  clear: []
}>()

const activeFilters = computed(() =>
  hasActiveFilters(props.search, props.type, props.source, props.tag),
)

const ALL_TYPES = [
  { value: '', label: 'Todos los tipos' },
  { value: 'course', label: 'Cursos' },
  { value: 'scholarship', label: 'Becas' },
  { value: 'workshop', label: 'Talleres' },
  { value: 'event', label: 'Eventos' },
  { value: 'other', label: 'Otros' },
]

const opportunityTypes = computed(() =>
  ALL_TYPES.filter(t => !t.value || !props.hiddenTypes?.includes(t.value)),
)
</script>

<template>
  <div class="glass-panel rounded-2xl p-4">
    <div class="flex flex-col gap-3 sm:flex-row sm:items-center">

      <!-- Búsqueda -->
      <div class="relative flex-1">
        <svg
          class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400 dark:text-slate-300"
          aria-hidden="true"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z" />
        </svg>
        <label for="filter-search" class="sr-only">Buscar oportunidades</label>
        <input
          id="filter-search"
          :value="search"
          type="search"
          placeholder="Buscar oportunidades..."
          class="h-10 w-full rounded-lg border border-slate-200 bg-white pl-9 pr-3 text-sm text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:ring-offset-0 dark:border-white/20 dark:bg-slate-900/55 dark:text-slate-100 dark:placeholder:text-slate-400"
          @input="emit('update:search', ($event.target as HTMLInputElement).value)"
        />
      </div>

      <!-- Tipo -->
      <label for="filter-type" class="sr-only">Filtrar por tipo</label>
      <select
        id="filter-type"
        :value="type"
        aria-label="Filtrar por tipo"
        class="h-10 rounded-lg border border-slate-200 bg-white px-3 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:ring-offset-0 dark:border-white/20 dark:bg-slate-900/55 dark:text-slate-100 sm:w-44"
        @change="emit('update:type', ($event.target as HTMLSelectElement).value)"
      >
        <option v-for="opt in opportunityTypes" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>

      <!-- Fuente -->
      <template v-if="sources.length">
        <label for="filter-source" class="sr-only">Filtrar por fuente</label>
        <select
          id="filter-source"
          :value="source"
          class="h-10 rounded-lg border border-slate-200 bg-white px-3 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:ring-offset-0 dark:border-white/20 dark:bg-slate-900/55 dark:text-slate-100 sm:w-44"
          @change="emit('update:source', ($event.target as HTMLSelectElement).value)"
        >
          <option value="">Todas las fuentes</option>
          <option v-for="s in sources" :key="s.value" :value="s.value">{{ s.label }}</option>
        </select>
      </template>

      <!-- Limpiar -->
      <button
        v-if="activeFilters"
        type="button"
        class="h-10 whitespace-nowrap rounded-lg border border-fuchsia-300/35 bg-fuchsia-400/15 px-4 text-sm text-fuchsia-700 transition-colors hover:border-cyan-400 hover:text-cyan-700 dark:text-fuchsia-100 dark:hover:border-cyan-300 dark:hover:text-cyan-100 focus:outline-none focus:ring-2 focus:ring-cyan-300 focus:ring-offset-0"
        @click="emit('clear')"
      >
        Limpiar filtros
      </button>
    </div>
  </div>
</template>
