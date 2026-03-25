<script setup lang="ts">
interface Slide {
  tag: string
  title: string
  subtitle: string
  cta: string
  href: string
  gradient: string
  image: string
}

const slides: Slide[] = [
  {
    tag: 'Más de 1,600 oportunidades',
    title: 'Aprende gratis\nen línea',
    subtitle: 'Cursos, becas y talleres gratuitos\nen español para hispanohablantes de todo el mundo.',
    cta: 'Explorar cursos',
    href: '/cursos',
    gradient: 'from-blue-800 to-blue-950',
    image: 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1080&q=80',
  },
  {
    tag: 'Para docentes',
    title: 'Formación digital\npara educadores',
    subtitle: 'Talleres y certificaciones en tecnología\npara transformar tu práctica docente.',
    cta: 'Ver talleres',
    href: '/talleres',
    gradient: 'from-slate-800 to-indigo-950',
    image: 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Latin_American_country_flags_in_LKSC%2C_Stanford_University.jpg/1280px-Latin_American_country_flags_in_LKSC%2C_Stanford_University.jpg',
  },
  {
    tag: 'Becas disponibles',
    title: 'Financia tu\neducación',
    subtitle: 'Becas STEM, idiomas y más programas\ncon financiamiento completo o parcial.',
    cta: 'Solicitar beca',
    href: '/becas',
    gradient: 'from-purple-800 to-purple-950',
    image: 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=1080&q=80',
  },
]

const current = ref(0)
let timer: ReturnType<typeof setInterval> | undefined

function nextSlide() {
  current.value = (current.value + 1) % slides.length
}

function previousSlide() {
  current.value = (current.value - 1 + slides.length) % slides.length
}

function goToSlide(index: number) {
  current.value = index
}

onMounted(() => {
  timer = setInterval(nextSlide, 6000)
})

onBeforeUnmount(() => {
  if (timer)
    clearInterval(timer)
})
</script>

<template>
  <section class="relative mx-auto h-[360px] w-full max-w-[1440px] overflow-hidden sm:h-[420px] lg:h-[480px]">
    <article
      v-for="(slide, index) in slides"
      :key="slide.title"
      class="absolute inset-0 transition-all duration-500"
      :class="index === current ? 'opacity-100' : 'pointer-events-none opacity-0'"
    >
      <div class="grid h-full grid-cols-1 md:grid-cols-[1fr_520px]">
        <div :class="`flex h-full flex-col justify-center bg-gradient-to-r ${slide.gradient} px-6 py-10 sm:px-10 lg:px-[72px]`">
          <span class="mb-5 w-max rounded bg-white/20 px-3 py-1 text-xs font-semibold text-white">{{ slide.tag }}</span>
          <h2 class="whitespace-pre-line text-3xl font-bold leading-tight text-white sm:text-4xl">
            {{ slide.title }}
          </h2>
          <p class="mt-4 whitespace-pre-line text-sm leading-relaxed text-white/80 sm:text-base">
            {{ slide.subtitle }}
          </p>
          <NuxtLink
            :to="slide.href"
            class="mt-7 w-max rounded-lg bg-amber-500 px-7 py-3.5 text-sm font-bold text-white transition-colors hover:bg-amber-600"
          >
            {{ slide.cta }}
          </NuxtLink>
        </div>

        <div class="hidden h-full md:block">
          <img :src="slide.image" :alt="slide.title" class="h-full w-full object-cover">
        </div>
      </div>
    </article>

    <button
      type="button"
      aria-label="Slide anterior"
      class="absolute left-4 top-1/2 grid h-12 w-12 -translate-y-1/2 place-items-center rounded-full border border-white/20 bg-black/20 text-2xl leading-none text-white"
      @click="previousSlide"
    >
      ‹
    </button>
    <button
      type="button"
      aria-label="Siguiente slide"
      class="absolute right-4 top-1/2 grid h-12 w-12 -translate-y-1/2 place-items-center rounded-full border border-white/20 bg-black/20 text-2xl leading-none text-white"
      @click="nextSlide"
    >
      ›
    </button>

    <div class="absolute bottom-5 left-1/2 flex -translate-x-1/2 items-center gap-2">
      <button
        v-for="(_, index) in slides"
        :key="index"
        :aria-label="`Ir al slide ${index + 1}`"
        class="h-2 rounded-full transition-all"
        :class="index === current ? 'w-6 bg-white' : 'w-2 bg-white/40'"
        @click="goToSlide(index)"
      />
    </div>
  </section>
</template>
