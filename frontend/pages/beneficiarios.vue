<script setup lang="ts">
useSeo({
  title: '¿A quién va dirigido? Estudiantes, docentes y profesionistas',
  description: 'EducaTYCs está dirigido a cualquier hispanohablante: estudiantes de preparatoria y universidad, docentes que quieren actualizarse y profesionistas que buscan crecer o cambiar de carrera.',
  path: '/beneficiarios',
})

// ── Stats count-up ──────────────────────────────────────────────
const statsDef = [
  { end: 1600, prefix: '+', suffix: '', separator: true,  label: 'oportunidades disponibles' },
  { end: 8,    prefix: '',  suffix: '', separator: true,  label: 'fuentes reconocidas' },
  { end: 500,  prefix: '',  suffix: 'M', separator: false, label: 'hispanohablantes en el mundo' },
]

const counts   = ref(statsDef.map(() => 0))
const visible  = ref(false)
const statsRef = ref<HTMLElement | null>(null)

function fmt(n: number, def: typeof statsDef[number]) {
  const s = def.end >= 1000 ? n.toLocaleString('en-US') : String(n)
  return `${def.prefix}${s}${def.suffix}`
}

function runCount(idx: number, end: number, delay: number) {
  setTimeout(() => {
    const duration = 1600
    const start    = performance.now()
    const tick = (now: number) => {
      const t = Math.min((now - start) / duration, 1)
      const eased = 1 - Math.pow(2, -10 * t)   // easeOutExpo
      counts.value[idx] = Math.round(eased * end)
      if (t < 1) requestAnimationFrame(tick)
      else counts.value[idx] = end
    }
    requestAnimationFrame(tick)
  }, delay)
}

onMounted(() => {
  const observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting && !visible.value) {
        visible.value = true
        statsDef.forEach((s, i) => runCount(i, s.end, i * 180))
      }
    },
    { threshold: 0.35 },
  )
  if (statsRef.value) observer.observe(statsRef.value)
})

interface Profile {
  number: string
  color: string
  borderColor: string
  textColor: string
  title: string
  description: string
  benefits: string[]
  cta: string
  href: string
}

// ── Text-to-Speech ──────────────────────────────────────────────
const playingIdx = ref<number | null>(null)

function toggleProfile(idx: number) {
  if (!import.meta.client) return

  if (playingIdx.value === idx) {
    window.speechSynthesis.cancel()
    playingIdx.value = null
    return
  }

  window.speechSynthesis.cancel()

  const p = profiles[idx]
  const text = `${p.title}. ${p.description}. ${p.benefits.join('. ')}.`

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

const profiles: Profile[] = [
  {
    number: '01',
    color: 'bg-cyan-300/12',
    borderColor: 'border-cyan-300/30',
    textColor: 'text-cyan-700 dark:text-cyan-100',
    title: 'Estudiantes',
    description: 'Desde preparatoria hasta posgrado — si quieres aprender algo nuevo, certificarte o prepararte para el mercado laboral, aquí encuentras opciones gratuitas.',
    benefits: [
      'Cursos de universidades como MIT, Harvard, UNAM y Coursera',
      'Becas nacionales e internacionales para financiar tus estudios',
      'Certificaciones digitales reconocidas por empleadores',
      'Programas STEM, idiomas, programación y más',
    ],
    cta: 'Ver cursos disponibles',
    href: '/cursos',
  },
  {
    number: '02',
    color: 'bg-fuchsia-300/12',
    borderColor: 'border-fuchsia-300/30',
    textColor: 'text-fuchsia-700 dark:text-fuchsia-100',
    title: 'Docentes',
    description: 'Si eres maestro, profesor o formador, aquí encuentras talleres y cursos para actualizar tus habilidades digitales y mejorar tu práctica educativa.',
    benefits: [
      'Talleres de herramientas digitales para el aula',
      'Formación en inteligencia artificial y tecnología educativa',
      'Certificaciones de Google, Microsoft y plataformas internacionales',
      'Programas de desarrollo profesional docente en línea',
    ],
    cta: 'Ver talleres para docentes',
    href: '/talleres',
  },
  {
    number: '03',
    color: 'bg-violet-300/12',
    borderColor: 'border-violet-300/30',
    textColor: 'text-violet-700 dark:text-violet-100',
    title: 'Profesionistas',
    description: 'Si ya trabajas y quieres subir de nivel, cambiar de carrera o acceder a financiamiento para especializarte, aquí tienes recursos pensados para ti.',
    benefits: [
      'Becas internacionales para maestrías y doctorados (DAAD, Fulbright, OEA)',
      'Cursos de upskilling en programación, datos, marketing y negocios',
      'Talleres de empleabilidad y competencias digitales',
      'Programas de becas Santander y Erasmus+ para Latam',
    ],
    cta: 'Ver becas disponibles',
    href: '/becas',
  },
]
</script>

<template>
  <div>
    <HeroCarousel />

    <main class="mx-auto max-w-[1440px] space-y-12 px-4 py-14 sm:px-8 lg:px-[120px]">

      <!-- Encabezado -->
      <section class="space-y-3">
        <span class="inline-block rounded-full border border-cyan-300/30 bg-cyan-300/15 px-3 py-1 text-xs font-semibold text-cyan-700 dark:text-cyan-100">Para todo hispanohablante</span>
        <h1 class="text-3xl font-bold text-slate-900 dark:text-white sm:text-4xl">¿A quién va dirigido?</h1>
        <p class="max-w-2xl text-base leading-relaxed text-slate-600 dark:text-slate-200">
          EducaTYCs es para cualquier persona de habla hispana que quiera aprender, crecer profesionalmente o acceder a financiamiento educativo — sin importar el país, edad o nivel.
        </p>
      </section>

      <!-- Perfiles -->
      <section class="grid gap-6 lg:grid-cols-3">
        <article
          v-for="(p, idx) in profiles"
          :key="p.title"
          class="glass-card flex flex-col rounded-xl p-8"
        >
          <div :class="`mb-4 grid h-10 w-10 place-items-center rounded-lg border ${p.borderColor} ${p.color} text-[13px] font-bold ${p.textColor}`">
            {{ p.number }}
          </div>
          <div class="flex flex-wrap items-center gap-3">
            <h2 class="text-2xl font-bold text-slate-900 dark:text-white">{{ p.title }}</h2>
            <TtsButton :playing="playingIdx === idx" @click="toggleProfile(idx)" />
          </div>
          <p class="mt-3 text-sm leading-7 text-slate-600 dark:text-slate-200">{{ p.description }}</p>

          <ul class="mt-5 space-y-2">
            <li
              v-for="benefit in p.benefits"
              :key="benefit"
              class="flex items-start gap-2 text-sm text-slate-600 dark:text-slate-300"
            >
              <span :class="`mt-1 shrink-0 ${p.textColor}`">✓</span>
              {{ benefit }}
            </li>
          </ul>

          <div class="mt-auto pt-6">
            <NuxtLink
              :to="p.href"
              :class="`inline-flex items-center gap-2 rounded-lg border ${p.borderColor} px-4 py-2.5 text-sm font-semibold ${p.textColor} transition-colors hover:bg-slate-100 dark:hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:ring-offset-0`"
            >
              {{ p.cta }}
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </NuxtLink>
          </div>
        </article>
      </section>

      <!-- Estadísticas rápidas -->
      <section
        ref="statsRef"
        class="glass-panel overflow-hidden rounded-2xl p-8 sm:p-10"
      >
        <div class="grid sm:grid-cols-3">
          <div
            v-for="(stat, i) in statsDef"
            :key="stat.label"
            class="flex flex-col items-center gap-2 px-6 py-4 text-center transition-all duration-700"
            :class="[
              visible ? 'translate-y-0 opacity-100' : 'translate-y-6 opacity-0',
              stat.separator ? 'sm:border-r sm:border-slate-200 sm:dark:border-white/10' : '',
            ]"
            :style="{ transitionDelay: `${i * 120}ms` }"
          >
            <p
              class="bg-gradient-to-br from-cyan-500 via-violet-500 to-fuchsia-500 bg-clip-text text-5xl font-extrabold tabular-nums text-transparent dark:from-cyan-300 dark:via-violet-300 dark:to-fuchsia-300"
            >
              {{ fmt(counts[i], stat) }}
            </p>
            <p class="text-sm font-medium text-slate-500 dark:text-slate-300">{{ stat.label }}</p>
          </div>
        </div>
      </section>

    </main>
  </div>
</template>
