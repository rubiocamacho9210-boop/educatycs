<script setup lang="ts">
useSeo({
  title: 'Talleres y capacitación digital gratuita',
  description: 'Talleres prácticos de habilidades digitales, empleabilidad y tecnología: Grow with Google, Microsoft Learn, STPS, Conecta Empleo y más. Gratis y en línea.',
  path: '/talleres',
})

interface Resource {
  name: string
  description: string
  url: string
  badge: string
}

const resources: Resource[] = [
  {
    name: 'Grow with Google',
    description: 'Talleres y cursos gratuitos de habilidades digitales, marketing, productividad y programación de Google.',
    url: 'https://grow.google/',
    badge: 'Gratuito',
  },
  {
    name: 'Capacítate para el Empleo — STPS',
    description: 'Talleres de formación laboral gratuitos del gobierno mexicano para mejorar tus competencias profesionales.',
    url: 'https://capacitateparaelempleo.org/',
    badge: 'México',
  },
  {
    name: 'Conecta Empleo — Fundación Telefónica',
    description: 'Talleres de empleabilidad y competencias digitales para jóvenes en situación de desempleo en Latam.',
    url: 'https://conectaempleo.fundaciontelefonica.com/',
    badge: 'Latam',
  },
  {
    name: 'CONOCER — Certificación de Competencias',
    description: 'Talleres y estándares de competencia laboral del Consejo Nacional de Normalización y Certificación de México.',
    url: 'https://www.conocer.gob.mx/',
    badge: 'México',
  },
  {
    name: 'Microsoft Learn',
    description: 'Talleres y rutas de aprendizaje gratuitas sobre Azure, IA, desarrollo y herramientas Microsoft 365.',
    url: 'https://learn.microsoft.com/es-es/',
    badge: 'Gratuito',
  },
]
</script>

<template>
  <div>
    <HeroCarousel />

    <main class="mx-auto max-w-[1440px] space-y-12 px-4 py-10 sm:px-8 lg:px-[120px]">

      <!-- Encabezado -->
      <section class="space-y-3">
        <span class="inline-block rounded-full border border-indigo-300/30 bg-indigo-300/15 px-3 py-1 text-xs font-semibold text-indigo-700 dark:text-indigo-100">Formación práctica</span>
        <h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-4xl">Talleres y capacitación digital</h1>
        <p class="max-w-2xl text-base leading-relaxed text-slate-600 dark:text-slate-200">
          Talleres prácticos de habilidades digitales, empleabilidad y formación profesional — muchos gratuitos y accesibles desde cualquier lugar.
        </p>
      </section>

      <!-- Recursos externos curados -->
      <section class="space-y-4">
        <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Plataformas de talleres destacadas</h2>
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
              <span class="rounded-full border border-indigo-300/30 bg-indigo-300/15 px-2.5 py-0.5 text-xs font-semibold text-indigo-700 dark:text-indigo-100">{{ r.badge }}</span>
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
