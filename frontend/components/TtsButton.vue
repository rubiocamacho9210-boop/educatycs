<script setup lang="ts">
defineProps<{ playing: boolean }>()
defineEmits<{ click: [] }>()
</script>

<template>
  <button
    type="button"
    :aria-label="playing ? 'Detener lectura' : 'Escuchar sección'"
    :title="playing ? 'Detener lectura' : 'Escuchar sección'"
    class="inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-medium transition-colors"
    :class="playing
      ? 'border-cyan-400/60 bg-cyan-400/15 text-cyan-600 dark:text-cyan-300'
      : 'border-slate-300/60 bg-slate-100 text-slate-500 hover:border-cyan-400/60 hover:bg-cyan-400/10 hover:text-cyan-600 dark:border-white/20 dark:bg-white/5 dark:text-slate-400 dark:hover:border-cyan-400/40 dark:hover:text-cyan-300'"
    @click="$emit('click')"
  >
    <!-- Equalizer animation when playing -->
    <span v-if="playing" class="flex items-end gap-px h-3.5" aria-hidden="true">
      <span class="w-0.5 rounded-sm bg-current animate-eq-1" />
      <span class="w-0.5 rounded-sm bg-current animate-eq-2" />
      <span class="w-0.5 rounded-sm bg-current animate-eq-3" />
    </span>
    <!-- Speaker icon when not playing -->
    <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fill-rule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.707.707L4.586 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.586l3.707-3.707a1 1 0 011.09-.217zM14.657 2.929a1 1 0 011.414 0A9.972 9.972 0 0119 10a9.972 9.972 0 01-2.929 7.071 1 1 0 01-1.414-1.414A7.971 7.971 0 0017 10c0-2.21-.894-4.208-2.343-5.657a1 1 0 010-1.414zm-2.829 2.828a1 1 0 011.415 0A5.983 5.983 0 0115 10a5.984 5.984 0 01-1.757 4.243 1 1 0 01-1.415-1.415A3.984 3.984 0 0013 10a3.983 3.983 0 00-1.172-2.828 1 1 0 010-1.415z" clip-rule="evenodd" />
    </svg>
    <span>{{ playing ? 'Detener' : 'Escuchar' }}</span>
  </button>
</template>

<style scoped>
@keyframes eq {
  0%, 100% { height: 0.25rem; }
  50%       { height: 0.875rem; }
}

.animate-eq-1 { animation: eq 0.8s ease-in-out infinite; }
.animate-eq-2 { animation: eq 0.8s ease-in-out infinite 0.2s; }
.animate-eq-3 { animation: eq 0.8s ease-in-out infinite 0.4s; }
</style>
