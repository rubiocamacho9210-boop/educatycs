<script setup lang="ts">
useSeo({
  title: 'Preguntas frecuentes',
  description: '¿Qué es EducaTYCs? ¿Es gratis? ¿Dan becas directamente? Resolvemos las dudas más comunes sobre la plataforma.',
  path: '/preguntas-frecuentes',
})

const faqs = [
  {
    q: '¿Qué es EducaTYCs?',
    a: 'Es una página gratuita donde reunimos cursos, becas y talleres en línea para que cualquier persona de habla hispana los encuentre en un solo lugar, sin tener que buscar en mil sitios distintos.',
  },
  {
    q: '¿Cuánto cuesta usar EducaTYCs?',
    a: 'Nada. La página es completamente gratuita. No tienes que registrarte, ni dar tu correo, ni pagar nada para ver las oportunidades.',
  },
  {
    q: '¿EducaTYCs me da la beca o me inscribe al curso?',
    a: 'No. Nosotros solo te mostramos la información y te llevamos al sitio oficial donde puedes aplicar. Todo el proceso de inscripción o solicitud lo haces directamente con la institución que ofrece la oportunidad.',
  },
  {
    q: '¿Las oportunidades que aparecen son gratuitas?',
    a: 'La mayoría sí, pero no todas. Algunas pueden tener costo o ser parcialmente gratuitas. Te recomendamos revisar los detalles directamente en el enlace de cada oportunidad antes de aplicar.',
  },
  {
    q: '¿Con qué frecuencia se actualiza el contenido?',
    a: 'Revisamos y actualizamos el catálogo de manera regular para que la información esté lo más al día posible. Sin embargo, como las convocatorias dependen de otras instituciones, siempre es buena idea confirmar directamente con ellas si una oportunidad sigue vigente.',
  },
  {
    q: '¿Puedo encontrar oportunidades aunque no sea de México?',
    a: 'Sí. EducaTYCs está pensado para cualquier persona que hable español, sin importar de qué país sea. Incluimos oportunidades de instituciones de todo el mundo que están disponibles en línea.',
  },
  {
    q: '¿Puedo buscar algo específico, como becas de idiomas o cursos de programación?',
    a: 'Sí. En la página principal puedes usar el buscador y los filtros para encontrar exactamente lo que te interesa: por tipo de oportunidad, por tema o por la plataforma que la ofrece.',
  },
  {
    q: 'Encontré una oportunidad con información incorrecta o un enlace que no funciona, ¿qué hago?',
    a: 'Escríbenos desde la sección de Contacto y dinos cuál es la oportunidad y qué está mal. Lo revisamos y corregimos lo antes posible. Gracias por ayudarnos a mejorar.',
  },
  {
    q: '¿EducaTYCs guarda mi información personal?',
    a: 'No. No pedimos que te registres y no guardamos ningún dato tuyo. Puedes navegar con total tranquilidad. Si quieres saber más, revisa nuestro Aviso de privacidad.',
  },
  {
    q: '¿Puedo sugerir una beca, curso o taller que no aparece en la página?',
    a: 'Claro que sí. Mándanos la información desde la sección de Contacto y la revisamos para incluirla si cumple con los criterios de la plataforma.',
  },
  {
    q: '¿Cómo puedo apoyar a EducaTYCs?',
    a: 'Puedes hacerlo a través de Ko-fi, una plataforma segura para donaciones voluntarias. Solo entra a ko-fi.com/educatycs y elige el monto que quieras aportar — desde un café. No es obligatorio ni necesitas cuenta, y cada donación ayuda directamente a mantener la plataforma en línea.',
  },
  {
    q: '¿Para qué se usan los donativos?',
    a: 'EducaTYCs es un proyecto sin fines de lucro. Los donativos se destinan exclusivamente a cubrir los gastos operativos de la plataforma: el servidor donde corre la página, el dominio web y las herramientas necesarias para mantener el catálogo actualizado. Sin esos costos cubiertos, la plataforma no puede seguir disponible de forma gratuita para todos.',
  },
]

// ── Text-to-Speech ──────────────────────────────────────────────
const playingIdx = ref<number | null>(null)

function toggleFaq(idx: number) {
  if (!import.meta.client) return

  if (playingIdx.value === idx) {
    window.speechSynthesis.cancel()
    playingIdx.value = null
    return
  }

  window.speechSynthesis.cancel()

  const faq = faqs[idx]
  const text = `${faq.q}. ${faq.a}`

  const u = new SpeechSynthesisUtterance(text)
  u.lang  = 'es-MX'
  u.rate  = 0.93
  u.pitch = 1.0

  const voices = window.speechSynthesis.getVoices()
  const esVoice = voices.find(v => v.lang.startsWith('es')) ?? null
  if (esVoice) u.voice = esVoice

  u.onend   = () => { if (playingIdx.value === idx) playingIdx.value = null }
  u.onerror = () => { playingIdx.value = null }

  playingIdx.value = idx
  window.speechSynthesis.speak(u)
}

onUnmounted(() => {
  if (import.meta.client) window.speechSynthesis.cancel()
})
</script>

<template>
  <main class="mx-auto max-w-[1440px] px-4 py-12 sm:px-8 lg:px-[120px]">
    <section class="glass-card rounded-2xl p-8 sm:p-10 space-y-4">
      <div class="space-y-2">
        <h1 class="text-3xl font-bold text-slate-900 dark:text-white">Preguntas frecuentes</h1>
        <p class="text-sm text-slate-500 dark:text-slate-300">Todo lo que necesitas saber sobre EducaTYCs, sin rodeos.</p>
      </div>

      <div class="divide-y divide-slate-200 dark:divide-white/10">
        <article
          v-for="(faq, idx) in faqs"
          :key="faq.q"
          class="py-5"
        >
          <div class="flex flex-wrap items-center gap-3">
            <h2 class="text-base font-semibold text-slate-800 dark:text-cyan-100">{{ faq.q }}</h2>
            <TtsButton :playing="playingIdx === idx" @click="toggleFaq(idx)" />
          </div>
          <p class="mt-2 text-sm leading-7 text-slate-600 dark:text-slate-200">{{ faq.a }}</p>
        </article>
      </div>

      <p class="text-sm text-slate-500 border-t border-slate-200 pt-4 dark:text-slate-300 dark:border-white/10">
        ¿Tienes otra duda? Escríbenos desde la sección de
        <NuxtLink to="/contacto" class="text-cyan-600 hover:underline dark:text-cyan-300">Contacto</NuxtLink>.
      </p>
    </section>
  </main>
</template>
