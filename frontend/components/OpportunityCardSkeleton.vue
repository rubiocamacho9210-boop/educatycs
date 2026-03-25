<script setup lang="ts">
defineProps<{
  compact?: boolean
}>()
</script>

<template>
  <!-- Compact skeleton row -->
  <div
    v-if="compact"
    class="glass-card flex items-center gap-3 rounded-xl px-4 py-3 sm:gap-4"
  >
    <div class="h-5 w-14 shrink-0 animate-pulse rounded-full bg-slate-200 dark:bg-slate-700/60" />
    <div class="min-w-0 flex-1 space-y-1.5">
      <div class="h-3.5 w-2/3 animate-pulse rounded bg-slate-200 dark:bg-slate-700/60" />
      <div class="h-3 w-1/3 animate-pulse rounded bg-slate-200 dark:bg-slate-700/60" />
    </div>
    <div class="h-5 w-16 shrink-0 animate-pulse rounded-full bg-slate-200 dark:bg-slate-700/60" />
    <div class="h-7 w-16 shrink-0 animate-pulse rounded-md bg-slate-200 dark:bg-slate-700/60" />
  </div>

  <!-- Card skeleton -->
  <div v-else class="glass-card flex flex-col rounded-xl p-5">
    <div class="flex flex-wrap items-center gap-2">
      <div class="h-5 w-14 animate-pulse rounded-full bg-slate-200 dark:bg-slate-700/60" />
      <div class="h-5 w-10 animate-pulse rounded-full bg-slate-200 dark:bg-slate-700/60" />
    </div>
    <div class="mt-3 h-4 w-3/4 animate-pulse rounded bg-slate-200 dark:bg-slate-700/60" />
    <div class="mt-1.5 h-3 w-1/2 animate-pulse rounded bg-slate-200 dark:bg-slate-700/60" />
    <div class="mt-2 space-y-1.5">
      <div class="h-3 w-full animate-pulse rounded bg-slate-200 dark:bg-slate-700/60" />
      <div class="h-3 w-5/6 animate-pulse rounded bg-slate-200 dark:bg-slate-700/60" />
    </div>
    <div class="mt-3 flex gap-1.5">
      <div class="h-5 w-14 animate-pulse rounded-full bg-slate-200 dark:bg-slate-700/60" />
      <div class="h-5 w-16 animate-pulse rounded-full bg-slate-200 dark:bg-slate-700/60" />
    </div>
    <div class="mt-auto border-t border-slate-100 pt-4 dark:border-white/10">
      <div class="h-8 w-20 animate-pulse rounded-md bg-slate-200 dark:bg-slate-700/60" />
    </div>
  </div>
</template>
