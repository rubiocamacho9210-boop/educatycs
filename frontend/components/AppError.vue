<script setup lang="ts">
defineProps<{
  message?: string
}>()
</script>

<template>
  <div class="rounded-md border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-400/30 dark:bg-red-400/10 dark:text-red-300">
    {{ message ?? 'No se pudo cargar la información. Intenta de nuevo más tarde.' }}
  </div>
</template>
