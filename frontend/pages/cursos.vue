<script setup lang="ts">
useSeo({
  title: 'Cursos en línea gratuitos en español',
  description: 'Explora cientos de cursos gratuitos de Coursera, edX, Khan Academy, MIT OpenCourseWare y más plataformas internacionales. Aprende desde cualquier lugar, en español.',
  path: '/cursos',
})

interface Resource {
  name: string
  description: string
  url: string
  badge: string
}

const resources: Resource[] = [
  {
    name: 'Coursera',
    description: 'Miles de cursos de universidades como Stanford, Michigan y UNAM. Muchos con certificado gratuito para auditores.',
    url: 'https://www.coursera.org/',
    badge: 'Gratuito / Pago',
  },
  {
    name: 'edX',
    description: 'Cursos de MIT, Harvard, Berkeley y más. Posibilidad de auditar cursos sin costo en la mayoría de programas.',
    url: 'https://www.edx.org/',
    badge: 'Gratuito / Pago',
  },
  {
    name: 'Khan Academy',
    description: 'Cursos completamente gratuitos de matemáticas, ciencias, programación, historia y más. Sin registros de pago.',
    url: 'https://es.khanacademy.org/',
    badge: 'Gratuito',
  },
  {
    name: 'MIT OpenCourseWare',
    description: 'Materiales de todos los cursos del MIT disponibles de forma libre y gratuita para el mundo.',
    url: 'https://ocw.mit.edu/',
    badge: 'Gratuito',
  },
  {
    name: 'FutureLearn',
    description: 'Cursos cortos de universidades del Reino Unido y organizaciones internacionales en inglés y español.',
    url: 'https://www.futurelearn.com/',
    badge: 'Gratuito / Pago',
  },
  {
    name: 'UNAM Educación Continua',
    description: 'Cursos abiertos y diplomados de la Universidad Nacional Autónoma de México disponibles en línea.',
    url: 'https://educacioncontinua.unam.mx/',
    badge: 'México',
  },
]
</script>

<template>
  <div>
    <HeroCarousel />

    <main class="mx-auto max-w-[1440px] space-y-12 px-4 py-10 sm:px-8 lg:px-[120px]">

      <!-- Encabezado -->
      <section class="space-y-3">
        <span class="inline-block rounded-full border border-cyan-300/30 bg-cyan-300/15 px-3 py-1 text-xs font-semibold text-cyan-700 dark:text-cyan-100">Aprendizaje en línea</span>
        <h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-4xl">Cursos en línea</h1>
        <p class="max-w-2xl text-base leading-relaxed text-slate-600 dark:text-slate-200">
          Cursos gratuitos o de bajo costo de las mejores universidades y plataformas del mundo — desde programación y ciencia hasta idiomas y negocios.
        </p>
      </section>

      <!-- Recursos externos curados -->
      <section class="space-y-4">
        <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Plataformas de cursos recomendadas</h2>
        <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <a
            v-for="r in resources"
            :key="r.name"
            :href="r.url"
            target="_blank"
            rel="noopener noreferrer"
            class="glass-card flex flex-col gap-3 rounded-xl p-5 transition-all hover:-translate-y-0.5 hover:shadow-2xl focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:ring-offset-0"
          >
            <div class="flex items-center justify-between gap-2">
              <span class="rounded-full border border-cyan-300/30 bg-cyan-300/15 px-2.5 py-0.5 text-xs font-semibold text-cyan-700 dark:text-cyan-100">{{ r.badge }}</span>
              <svg class="h-4 w-4 shrink-0 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </div>
            <p class="text-sm font-semibold text-slate-900 dark:text-white">{{ r.name }}</p>
            <p class="text-xs leading-relaxed text-slate-500 dark:text-slate-300">{{ r.description }}</p>
          </a>
        </div>
      </section>

    </main>
  </div>
</template>
