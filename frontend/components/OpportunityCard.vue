<script setup lang="ts">
import type { Opportunity, OpportunityType } from '~/types/opportunity'

defineProps<{
  opportunity: Opportunity
  compact?: boolean
}>()

const typeLabels: Record<OpportunityType, string> = {
  course: 'Curso',
  workshop: 'Taller',
  scholarship: 'Beca',
  event: 'Evento',
  other: 'Programa',
}
</script>

<template>
  <!-- Compact / list row -->
  <div
    v-if="compact"
    class="glass-card flex items-center gap-3 rounded-xl px-4 py-3 transition-all hover:shadow-lg sm:gap-4"
  >
    <span class="shrink-0 rounded-full border border-cyan-300/30 bg-cyan-300/12 px-2.5 py-0.5 text-xs font-semibold text-cyan-700 dark:text-cyan-100">
      {{ typeLabels[opportunity.opportunity_type] }}
    </span>
    <div class="min-w-0 flex-1">
      <h3 class="truncate text-sm font-semibold text-slate-900 dark:text-white">{{ opportunity.title }}</h3>
      <p class="truncate text-xs text-slate-500 dark:text-slate-300">{{ opportunity.provider }} · {{ opportunity.location ?? 'Online' }}</p>
    </div>
    <span
      v-if="opportunity.is_free"
      class="shrink-0 rounded-full border border-emerald-300/30 bg-emerald-300/15 px-2.5 py-0.5 text-xs font-semibold text-emerald-700 dark:text-emerald-100"
    >
      Gratuito
    </span>
    <NuxtLink
      :to="`/curso/${opportunity.id}`"
      :aria-label="`Ver más sobre ${opportunity.title}`"
      class="neon-btn shrink-0 rounded-md px-3 py-1.5 text-xs font-semibold transition-all focus:outline-none focus:ring-2 focus:ring-cyan-300 focus:ring-offset-0"
    >
      Ver más
    </NuxtLink>
  </div>

  <!-- Default / card grid -->
  <div v-else class="glass-card flex flex-col rounded-xl p-5 transition-all hover:-translate-y-0.5 hover:shadow-2xl">
    <!-- Tipo, modalidad y gratuito -->
    <div class="flex flex-wrap items-center gap-2">
      <span class="rounded-full border border-cyan-300/30 bg-cyan-300/12 px-2.5 py-0.5 text-xs font-semibold tracking-wide text-cyan-700 dark:text-cyan-100">
        {{ typeLabels[opportunity.opportunity_type] }}
      </span>
      <span class="text-xs text-slate-500 dark:text-slate-300">{{ opportunity.location ?? 'Online' }}</span>
      <span
        v-if="opportunity.is_free"
        class="rounded-full border border-emerald-300/30 bg-emerald-300/15 px-2.5 py-0.5 text-xs font-semibold text-emerald-700 dark:text-emerald-100"
      >
        Gratuito
      </span>
    </div>

    <!-- Título y proveedor -->
    <h3 class="mt-3 text-base font-semibold leading-snug text-slate-900 dark:text-white">{{ opportunity.title }}</h3>
    <p class="mt-0.5 text-sm font-medium text-slate-500 dark:text-slate-300">{{ opportunity.provider }}</p>

    <!-- Descripción truncada -->
    <p v-if="opportunity.description" class="mt-2 line-clamp-2 text-sm leading-relaxed text-slate-500 dark:text-slate-300">
      {{ opportunity.description }}
    </p>

    <!-- Tags -->
    <div v-if="opportunity.tags.length" class="mt-3 flex flex-wrap gap-1.5">
      <span
        v-for="tag in opportunity.tags"
        :key="tag"
        class="rounded-full border border-slate-200 bg-slate-50 px-2.5 py-0.5 text-xs text-slate-600 dark:border-white/25 dark:bg-slate-900/45 dark:text-slate-200"
      >
        {{ tag }}
      </span>
    </div>

    <!-- Botón al fondo -->
    <div class="mt-auto border-t border-slate-100 pt-4 dark:border-white/20">
      <NuxtLink
        :to="`/curso/${opportunity.id}`"
        :aria-label="`Ver más sobre ${opportunity.title}`"
        class="neon-btn inline-flex items-center gap-1.5 rounded-md px-3.5 py-1.5 text-sm font-semibold transition-all focus:outline-none focus:ring-2 focus:ring-cyan-300 focus:ring-offset-0"
      >
        Ver más
      </NuxtLink>
    </div>
  </div>
</template>
