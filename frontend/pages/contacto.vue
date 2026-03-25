<script setup lang="ts">
useSeo({
  title: 'Contacto',
  description: 'Escríbenos si tienes dudas, quieres sugerir una oportunidad educativa o encontraste información incorrecta. Te respondemos a la brevedad.',
  path: '/contacto',
})

const nombre = ref('')
const email = ref('')
const asunto = ref('')
const mensaje = ref('')

const estado = ref<'idle' | 'enviando' | 'enviado' | 'error'>('idle')
const errorDetalle = ref('')

const EMAILJS_SERVICE_ID = 'service_8k6pasb'
const EMAILJS_TEMPLATE_ID = 'template_m2yqz9e'
const EMAILJS_PUBLIC_KEY = 'ZhuLJN8jMZqhkL_Ic'

async function enviar() {
  if (!nombre.value || !email.value || !mensaje.value) return

  estado.value = 'enviando'

  try {
    const { default: emailjs } = await import('@emailjs/browser')
    await emailjs.send(
      EMAILJS_SERVICE_ID,
      EMAILJS_TEMPLATE_ID,
      {
        name: nombre.value,
        email: email.value,
        title: asunto.value || 'Sin asunto',
        message: mensaje.value,
      },
      EMAILJS_PUBLIC_KEY,
    )
    estado.value = 'enviado'
    nombre.value = ''
    email.value = ''
    asunto.value = ''
    mensaje.value = ''
  }
  catch (err: unknown) {
    console.error('EmailJS error:', err)
    errorDetalle.value = err instanceof Error ? err.message : JSON.stringify(err)
    estado.value = 'error'
  }
}
</script>

<template>
  <main class="mx-auto max-w-[1440px] px-4 py-12 sm:px-8 lg:px-[120px]">
    <section class="glass-card rounded-2xl p-8 sm:p-10 space-y-8">

      <!-- Encabezado -->
      <div class="space-y-2">
        <h1 class="text-3xl font-bold text-slate-900 dark:text-white">Contacto</h1>
        <p class="max-w-xl text-sm leading-7 text-slate-600 dark:text-slate-200">
          ¿Tienes dudas, sugerencias o encontraste una oportunidad con datos incorrectos? Escríbenos y te respondemos a la brevedad.
        </p>
      </div>

      <div class="grid gap-10 lg:grid-cols-2 lg:items-start">

        <!-- Formulario -->
        <form class="space-y-4" @submit.prevent="enviar">
          <div class="grid gap-4 sm:grid-cols-2">
            <div class="space-y-1.5">
              <label for="nombre" class="block text-xs font-semibold uppercase tracking-wide text-slate-600 dark:text-slate-300">Nombre</label>
              <input
                id="nombre"
                v-model="nombre"
                type="text"
                placeholder="Tu nombre"
                required
                class="w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-sm text-slate-800 placeholder-slate-400 outline-none transition focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 dark:border-white/15 dark:bg-slate-900/60 dark:text-white dark:placeholder-slate-500"
              >
            </div>
            <div class="space-y-1.5">
              <label for="email" class="block text-xs font-semibold uppercase tracking-wide text-slate-600 dark:text-slate-300">Correo electrónico</label>
              <input
                id="email"
                v-model="email"
                type="email"
                placeholder="tu@correo.com"
                required
                class="w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-sm text-slate-800 placeholder-slate-400 outline-none transition focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 dark:border-white/15 dark:bg-slate-900/60 dark:text-white dark:placeholder-slate-500"
              >
            </div>
          </div>

          <div class="space-y-1.5">
            <label for="asunto" class="block text-xs font-semibold uppercase tracking-wide text-slate-600 dark:text-slate-300">Asunto <span class="normal-case text-slate-500">(opcional)</span></label>
            <input
              id="asunto"
              v-model="asunto"
              type="text"
              placeholder="¿De qué se trata?"
              class="w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-sm text-slate-800 placeholder-slate-400 outline-none transition focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 dark:border-white/15 dark:bg-slate-900/60 dark:text-white dark:placeholder-slate-500"
            >
          </div>

          <div class="space-y-1.5">
            <label for="mensaje" class="block text-xs font-semibold uppercase tracking-wide text-slate-600 dark:text-slate-300">Mensaje</label>
            <textarea
              id="mensaje"
              v-model="mensaje"
              rows="5"
              placeholder="Escribe tu mensaje aquí..."
              required
              class="w-full resize-none rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-sm text-slate-800 placeholder-slate-400 outline-none transition focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 dark:border-white/15 dark:bg-slate-900/60 dark:text-white dark:placeholder-slate-500"
            />
          </div>

          <!-- Feedback -->
          <div v-if="estado === 'enviado'" class="rounded-lg border border-cyan-300/30 bg-cyan-300/10 px-4 py-3 text-sm text-cyan-700 dark:text-cyan-100">
            ¡Mensaje enviado! Te responderemos pronto.
          </div>
          <div v-if="estado === 'error'" class="rounded-lg border border-red-400/30 bg-red-400/10 px-4 py-3 text-sm text-red-700 space-y-1 dark:text-red-200">
            <p>Ocurrió un error al enviar. Por favor intenta de nuevo en unos momentos.</p>
            <p v-if="errorDetalle" class="text-xs text-red-600 font-mono dark:text-red-300">{{ errorDetalle }}</p>
          </div>

          <button
            type="submit"
            :disabled="estado === 'enviando'"
            class="rounded-lg bg-cyan-500 px-6 py-2.5 text-sm font-semibold text-slate-950 transition-colors hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-50 focus:outline-none focus:ring-2 focus:ring-cyan-300"
          >
            {{ estado === 'enviando' ? 'Enviando...' : 'Enviar mensaje' }}
          </button>
        </form>

        <!-- Info lateral -->
        <div class="space-y-4">
<div class="rounded-xl border border-slate-200 bg-slate-50 p-5 space-y-1 dark:border-white/15 dark:bg-slate-900/45">
            <p class="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">Horario de atención</p>
            <p class="text-sm font-semibold text-slate-800 dark:text-slate-100">Lunes a viernes · 9:00 a 17:00 (CST)</p>
          </div>

          <div class="rounded-xl border border-slate-200 bg-slate-50 p-5 space-y-2 dark:border-white/15 dark:bg-slate-900/45">
            <p class="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">¿Para qué puedes escribirnos?</p>
            <ul class="space-y-1.5 text-sm text-slate-600 dark:text-slate-300">
              <li class="flex gap-2"><span class="text-cyan-600 dark:text-cyan-300">✓</span> Reportar una oportunidad con datos incorrectos o vencidos</li>
              <li class="flex gap-2"><span class="text-cyan-600 dark:text-cyan-300">✓</span> Sugerir una beca, curso o taller que no aparece</li>
              <li class="flex gap-2"><span class="text-cyan-600 dark:text-cyan-300">✓</span> Preguntas generales sobre la plataforma</li>
              <li class="flex gap-2"><span class="text-cyan-600 dark:text-cyan-300">✓</span> Propuestas de colaboración o alianzas</li>
            </ul>
          </div>
        </div>

      </div>
    </section>
  </main>
</template>
