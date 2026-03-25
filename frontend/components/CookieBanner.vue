<script setup lang="ts">
const { initFromConsent, accept, reject, getConsent } = useAnalytics()

const visible = ref(false)

onMounted(() => {
  initFromConsent()
  visible.value = getConsent() === null
})

function onAccept() {
  accept()
  visible.value = false
}

function onReject() {
  reject()
  visible.value = false
}
</script>

<template>
  <Transition
    enter-active-class="transition duration-300 ease-out"
    enter-from-class="translate-y-4 opacity-0"
    enter-to-class="translate-y-0 opacity-100"
    leave-active-class="transition duration-200 ease-in"
    leave-from-class="translate-y-0 opacity-100"
    leave-to-class="translate-y-4 opacity-0"
  >
    <div
      v-if="visible"
      role="dialog"
      aria-label="Aviso de cookies"
      class="fixed bottom-4 left-4 right-4 z-50 mx-auto max-w-2xl rounded-xl border border-slate-200 bg-white/95 p-5 shadow-2xl backdrop-blur-xl dark:border-white/15 dark:bg-slate-900/95 sm:left-6 sm:right-auto sm:w-[480px]"
    >
      <p class="text-sm leading-6 text-slate-600 dark:text-slate-200">
        Usamos <strong class="text-slate-900 dark:text-white">Google Analytics</strong> para saber cuántas personas visitan la página y desde qué países, sin recopilar datos personales.
        <NuxtLink to="/aviso-de-privacidad" class="ml-1 text-cyan-600 underline underline-offset-2 hover:text-cyan-700 dark:text-cyan-300 dark:hover:text-cyan-200">
          Más información
        </NuxtLink>
      </p>
      <div class="mt-4 flex flex-wrap gap-2">
        <button
          type="button"
          class="rounded-lg bg-cyan-500 px-4 py-2 text-sm font-semibold text-slate-950 transition-colors hover:bg-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-400"
          @click="onAccept"
        >
          Aceptar
        </button>
        <button
          type="button"
          class="rounded-lg border border-slate-200 px-4 py-2 text-sm text-slate-600 transition-colors hover:border-slate-300 hover:text-slate-800 dark:border-white/20 dark:text-slate-300 dark:hover:border-white/40 dark:hover:text-white focus:outline-none focus:ring-2 focus:ring-slate-300 dark:focus:ring-white/30"
          @click="onReject"
        >
          Rechazar
        </button>
      </div>
    </div>
  </Transition>
</template>
