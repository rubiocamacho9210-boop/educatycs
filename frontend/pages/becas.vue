<script setup lang="ts">
useSeo({
  title: 'Becas y financiamiento educativo para hispanohablantes',
  description: 'Encuentra becas nacionales e internacionales: Santander, DAAD, Fulbright, Erasmus+, OEA y más. Financia tus estudios de licenciatura, maestría o doctorado.',
  path: '/becas',
})

interface Resource {
  name: string
  description: string
  url: string
  badge: string
}

const resources: Resource[] = [
  {
    name: 'Becas Santander',
    description: 'Becas para universitarios latinoamericanos en formación, idiomas, emprendimiento y movilidad internacional.',
    url: 'https://app.santanderopenacademy.com/es/program/de-excelencia-academica-2026',
    badge: 'Internacional',
  },
  {
    name: 'DAAD — Servicio Alemán de Intercambio Académico',
    description: 'Becas para estudiar o investigar en Alemania. Programas de maestría, doctorado y estancias de investigación.',
    url: 'https://www.daad.mx/',
    badge: 'Alemania',
  },
  {
    name: 'FUNED — Fundación para la Educación Superior',
    description: 'Becas y créditos educativos para estudiantes mexicanos de licenciatura y posgrado en instituciones de calidad.',
    url: 'https://funed.org.mx/',
    badge: 'México',
  },
  {
    name: 'Erasmus+ para Latinoamérica',
    description: 'Programa de la Unión Europea con becas de movilidad para estudiar, hacer prácticas o formarse en Europa.',
    url: 'https://erasmus-plus.ec.europa.eu/',
    badge: 'Europa',
  },
  {
    name: 'Comexus — Beca Fulbright-García Robles',
    description: 'Becas para estudiantes y profesores mexicanos que deseen realizar estudios o investigación en EUA.',
    url: 'https://www.comexus.org.mx/',
    badge: 'EUA',
  },
  {
    name: 'OEA — Becas y Programas de Formación',
    description: 'Becas de la Organización de los Estados Americanos para posgrado y desarrollo profesional en América.',
    url: 'https://www.oas.org/es/becas/',
    badge: 'Latam',
  },
]
</script>

<template>
  <div>
    <HeroCarousel />

    <main class="mx-auto max-w-[1440px] space-y-12 px-4 py-10 sm:px-8 lg:px-[120px]">

      <!-- Encabezado -->
      <section class="space-y-3">
        <span class="inline-block rounded-full border border-purple-300/30 bg-purple-300/15 px-3 py-1 text-xs font-semibold text-purple-700 dark:text-purple-100">Becas disponibles</span>
        <h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-4xl">Becas y financiamiento</h1>
        <p class="max-w-2xl text-base leading-relaxed text-slate-600 dark:text-slate-200">
          Programas de becas nacionales e internacionales para estudiar, investigar o capacitarte — dentro de México, en Latinoamérica y en el extranjero.
        </p>
      </section>

      <!-- Recursos externos curados -->
      <section class="space-y-4">
        <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Organismos y convocatorias destacadas</h2>
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
              <span class="rounded-full border border-purple-300/30 bg-purple-300/15 px-2.5 py-0.5 text-xs font-semibold text-purple-700 dark:text-purple-100">{{ r.badge }}</span>
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
