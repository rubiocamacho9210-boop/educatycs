<script setup lang="ts">
useSeo({
  title: 'Acerca de EducaTYCs — Proyecto de servicio social Tecmilenio',
  description: 'EducaTYCs nació en 2026 como proyecto de servicio social en la Universidad Tecmilenio. Nuestra misión: conectar a los 500 millones de hispanohablantes con oportunidades educativas gratuitas en línea, alineados con el ODS 4 de la ONU.',
  path: '/acerca-de',
})

// ── Text-to-Speech ──────────────────────────────────────────────
type SectionId = 'origen' | 'mision' | 'vision' | 'objetivo' | 'roadmap'

const playingId  = ref<SectionId | null>(null)
const origenEl   = ref<HTMLElement | null>(null)
const misionEl   = ref<HTMLElement | null>(null)
const visionEl   = ref<HTMLElement | null>(null)
const objetivoEl = ref<HTMLElement | null>(null)
const roadmapEl  = ref<HTMLElement | null>(null)

const sectionElMap: Record<SectionId, ReturnType<typeof ref<HTMLElement | null>>> = {
  origen:   origenEl,
  mision:   misionEl,
  vision:   visionEl,
  objetivo: objetivoEl,
  roadmap:  roadmapEl,
}

function toggleSection(id: SectionId) {
  if (!import.meta.client) return

  // Stop if already playing this section
  if (playingId.value === id) {
    window.speechSynthesis.cancel()
    playingId.value = null
    return
  }

  window.speechSynthesis.cancel()

  const el = sectionElMap[id].value
  if (!el) return

  const text = Array.from(el.querySelectorAll('h2, p'))
    .map(n => n.textContent?.trim())
    .filter(Boolean)
    .join('. ')

  if (!text) return

  const u = new SpeechSynthesisUtterance(text)
  u.lang  = 'es-MX'
  u.rate  = 0.93
  u.pitch = 1.0

  // Pick a Spanish voice if available
  const voices = window.speechSynthesis.getVoices()
  const esVoice = voices.find(v => v.lang.startsWith('es')) ?? null
  if (esVoice) u.voice = esVoice

  u.onend   = () => { if (playingId.value === id) playingId.value = null }
  u.onerror = () => { playingId.value = null }

  playingId.value = id
  window.speechSynthesis.speak(u)
}

onUnmounted(() => {
  if (import.meta.client) window.speechSynthesis.cancel()
})
</script>

<template>
  <div>
    <HeroCarousel />

    <main class="mx-auto max-w-[1440px] space-y-14 px-4 py-14 sm:px-8 lg:px-[120px]">

      <!-- Encabezado -->
      <section class="space-y-3">
        <span class="inline-block rounded-full border border-cyan-300/30 bg-cyan-300/15 px-3 py-1 text-xs font-semibold text-cyan-700 dark:text-cyan-100">Proyecto educativo</span>
        <h1 class="text-3xl font-bold text-slate-900 dark:text-white sm:text-4xl">Acerca de EducaTYCs</h1>
        <p class="max-w-3xl text-base leading-relaxed text-slate-600 dark:text-slate-200">
          Lo que empezó como un proyecto de servicio social universitario se convirtió en una plataforma gratuita para conectar a millones de hispanohablantes con oportunidades educativas en línea, desde cualquier lugar del mundo.
        </p>
      </section>

      <div class="h-px w-full bg-slate-200 dark:bg-white/20" />

      <!-- Origen -->
      <section ref="origenEl" class="grid gap-8 lg:grid-cols-2 lg:items-center">
        <div class="space-y-4">
          <div class="grid h-10 w-10 place-items-center rounded-lg border border-cyan-300/30 bg-cyan-300/12 text-[13px] font-bold text-cyan-700 dark:text-cyan-100">00</div>
          <div class="flex flex-wrap items-center gap-3">
            <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Cómo nació</h2>
            <TtsButton :playing="playingId === 'origen'" @click="toggleSection('origen')" />
          </div>
          <p class="text-sm leading-8 text-slate-600 dark:text-slate-200">
            EducaTYCs nació en 2026 como parte de un proyecto de servicio social desarrollado en la <strong class="text-slate-900 dark:text-white">Universidad Tecmilenio</strong>. El punto de partida fue una pregunta que cualquier estudiante o profesionista se ha hecho alguna vez: ¿dónde puedo encontrar cursos, becas o talleres gratuitos que realmente valgan la pena? La respuesta, en la práctica, siempre era la misma — había que buscar en decenas de sitios distintos, comparar fechas, verificar requisitos y, muchas veces, enterarse tarde de una convocatoria que hubiera sido perfecta.
          </p>
          <p class="text-sm leading-8 text-slate-600 dark:text-slate-200">
            El equipo detrás del proyecto identificó que el problema no era la falta de oportunidades educativas: organizaciones internacionales, universidades, gobiernos y plataformas digitales generan miles de opciones cada año. El problema era la dispersión. Nadie las reunía en un solo lugar, en español, de forma ordenada y accesible para cualquier persona, sin importar de qué país fuera ni qué dispositivo usara. Con ese diagnóstico claro, EducaTYCs tomó forma.
          </p>
        </div>
        <div class="glass-card rounded-xl p-8 space-y-4">
          <p class="text-sm leading-8 text-slate-600 dark:text-slate-200">
            Lo que comenzó como una iniciativa académica acotada fue creciendo en alcance y ambición. Durante el desarrollo del proyecto, el equipo comprendió que la necesidad no era local ni regional: era de todos los hispanohablantes. Más de 500 millones de personas en el mundo comparten el español como lengua materna o de uso cotidiano, y muchas de ellas enfrentan exactamente la misma barrera: la información educativa está fragmentada, en inglés, o detrás de sistemas de registro complicados.
          </p>
          <p class="text-sm leading-8 text-slate-600 dark:text-slate-200">
            Así, el proyecto de servicio social se transformó en una plataforma pública, abierta y gratuita, con la convicción de que el acceso al conocimiento no debería depender del país de origen, del nivel económico ni de saber exactamente dónde buscar.
          </p>
          <div class="border-t border-slate-200 pt-4 dark:border-white/10 space-y-3">
            <p class="text-xs font-semibold uppercase tracking-widest text-cyan-600 dark:text-cyan-300">Alineado con la ODS 4 — Educación de Calidad</p>
            <p class="text-sm leading-8 text-slate-600 dark:text-slate-200">
              EducaTYCs se desarrolló con plena conciencia de los <strong class="text-slate-900 dark:text-white">Objetivos de Desarrollo Sostenible de la ONU</strong>, en particular el <strong class="text-slate-900 dark:text-white">ODS 4: Educación de Calidad</strong>, que establece el compromiso global de garantizar una educación inclusiva, equitativa y de calidad, y promover oportunidades de aprendizaje permanente para todas las personas. Este objetivo reconoce que la educación es el motor más poderoso para reducir la pobreza, disminuir las desigualdades y construir sociedades más justas — pero también reconoce que, para millones de personas, el acceso real sigue siendo una barrera.
            </p>
            <p class="text-sm leading-8 text-slate-600 dark:text-slate-200">
              En América Latina y el mundo hispanohablante, esa barrera tiene un nombre muy concreto: la <strong class="text-slate-900 dark:text-white">dispersión de la información</strong>. Las oportunidades existen — universidades, organismos internacionales y plataformas digitales generan miles de programas gratuitos cada año — pero llegar a ellas requiere tiempo, conectividad y saber exactamente dónde buscar. Herramientas como EducaTYCs son necesarias precisamente porque acortan esa distancia: concentran lo que está disperso, lo presentan en el idioma del usuario y eliminan los pasos intermedios que hacen que mucha gente se rinda antes de intentarlo.
            </p>
            <p class="text-sm leading-8 text-slate-600 dark:text-slate-200">
              Contribuir al ODS 4 no es solo una declaración de principios para este proyecto — es la razón por la que existe.
            </p>
          </div>
        </div>
      </section>

      <div class="h-px w-full bg-slate-200 dark:bg-white/20" />

      <!-- Misión -->
      <section ref="misionEl" class="grid gap-8 lg:grid-cols-2 lg:items-center">
        <div class="glass-card rounded-xl p-8 space-y-4 lg:order-2">
          <p class="text-sm leading-8 text-slate-600 dark:text-slate-200">
            Cada día, personas de distintos países, edades y trayectorias llegan a EducaTYCs buscando algo concreto: una beca para seguir estudiando, un curso para cambiar de carrera, un taller para actualizar sus habilidades digitales o simplemente algo nuevo que aprender. Lo que todos tienen en común es que no deberían tener que gastar horas rastreando sitios dispersos para encontrarlo.
          </p>
          <p class="text-sm leading-8 text-slate-600 dark:text-slate-200">
            Por eso, la misión de EducaTYCs es clara y no se negocia: reunir en un solo lugar las mejores oportunidades educativas gratuitas disponibles en línea, presentarlas de forma ordenada y accesible, y conectar a las personas con ellas de la manera más directa posible. Sin intermediarios, sin costos, sin burocracia.
          </p>
        </div>
        <div class="space-y-4 lg:order-1">
          <div class="grid h-10 w-10 place-items-center rounded-lg border border-cyan-300/30 bg-cyan-300/12 text-[13px] font-bold text-cyan-700 dark:text-cyan-100">01</div>
          <div class="flex flex-wrap items-center gap-3">
            <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Misión</h2>
            <TtsButton :playing="playingId === 'mision'" @click="toggleSection('mision')" />
          </div>
          <p class="text-sm leading-8 text-slate-600 dark:text-slate-200">
            La misión de EducaTYCs es <strong class="text-slate-900 dark:text-white">facilitar el acceso a oportunidades educativas gratuitas</strong> para cualquier persona hispanohablante que quiera aprender, crecer profesionalmente o financiar su formación, sin importar el país desde el que lo haga. Para cumplirla, la plataforma recopila, verifica y organiza de forma continua cursos, becas, talleres y eventos formativos ofrecidos por instituciones reconocidas a nivel nacional e internacional.
          </p>
          <p class="text-sm leading-8 text-slate-600 dark:text-slate-200">
            Esto implica un trabajo constante de investigación, actualización y curaduría: no se trata solo de listar enlaces, sino de asegurarse de que la información sea relevante, esté vigente y sea comprensible para alguien que llega por primera vez. La misión de EducaTYCs no termina cuando una persona encuentra una oportunidad — termina cuando esa persona puede tomar una decisión informada sobre su educación.
          </p>
        </div>
      </section>

      <div class="h-px w-full bg-slate-200 dark:bg-white/20" />

      <!-- Visión -->
      <section ref="visionEl" class="grid gap-8 lg:grid-cols-2 lg:items-center">
        <div class="space-y-4">
          <div class="grid h-10 w-10 place-items-center rounded-lg border border-fuchsia-300/30 bg-fuchsia-300/12 text-[13px] font-bold text-fuchsia-700 dark:text-fuchsia-100">02</div>
          <div class="flex flex-wrap items-center gap-3">
            <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Visión</h2>
            <TtsButton :playing="playingId === 'vision'" @click="toggleSection('vision')" />
          </div>
          <p class="text-sm leading-8 text-slate-600 dark:text-slate-200">
            La visión de EducaTYCs es convertirse en <strong class="text-slate-900 dark:text-white">el punto de referencia más confiable en español para encontrar oportunidades educativas en línea</strong>. No el más grande ni el más llamativo, sino el más útil: aquel al que cualquier persona regresa porque sabe que encontrará información real, actualizada y relevante para su situación.
          </p>
          <p class="text-sm leading-8 text-slate-600 dark:text-slate-200">
            El aprendizaje en línea ha democratizado el acceso al conocimiento de una manera que hubiera sido inimaginable hace veinte años. Hoy es posible tomar un curso del MIT desde Ciudad de México, solicitar una beca europea desde Buenos Aires o certificarse con Google desde Bogotá. Sin embargo, ese potencial sigue siendo invisible para millones de hispanohablantes, no por falta de interés, sino por falta de información accesible.
          </p>
        </div>
        <div class="glass-card rounded-xl p-8 space-y-4">
          <p class="text-sm leading-8 text-slate-600 dark:text-slate-200">
            EducaTYCs quiere cerrar esa brecha. La visión a largo plazo es construir una comunidad de aprendizaje activa, donde la plataforma no solo sea un catálogo sino un punto de encuentro: un lugar donde las personas descubran qué es posible estudiar, se inspiren con las historias de quienes ya lo hicieron y encuentren el camino para dar el siguiente paso en su formación.
          </p>
          <p class="text-sm leading-8 text-slate-600 dark:text-slate-200">
            Impulsar una cultura de aprendizaje continuo entre los más de <strong class="text-slate-900 dark:text-white">500 millones de hispanohablantes</strong> en el mundo no es una meta menor. Es una apuesta por la equidad, la movilidad social y la convicción de que el conocimiento, cuando es accesible, transforma vidas.
          </p>
        </div>
      </section>

      <div class="h-px w-full bg-slate-200 dark:bg-white/20" />

      <!-- Objetivo -->
      <section ref="objetivoEl" class="grid gap-8 lg:grid-cols-2 lg:items-center">
        <div class="glass-card rounded-xl p-8 space-y-4 lg:order-2">
          <p class="text-sm leading-8 text-slate-600 dark:text-slate-200">
            Para lograr ese objetivo, EducaTYCs trabaja con un catálogo en constante expansión que abarca cursos de plataformas como Coursera, edX, Khan Academy y MIT OpenCourseWare; becas de organismos como DAAD, Fulbright, OEA, Erasmus+ y Santander; talleres de Google, Microsoft, Telefónica y dependencias gubernamentales; y eventos formativos de instituciones académicas de todo el mundo.
          </p>
          <p class="text-sm leading-8 text-slate-600 dark:text-slate-200">
            Cada oportunidad se presenta con la información suficiente para que el usuario entienda de qué se trata, a quién va dirigida y cómo acceder a ella — sin tecnicismos, sin letras pequeñas y sin perder tiempo. Ese es el estándar que EducaTYCs se impone a sí mismo en cada entrada del catálogo.
          </p>
        </div>
        <div class="space-y-4 lg:order-1">
          <div class="grid h-10 w-10 place-items-center rounded-lg border border-violet-300/30 bg-violet-300/12 text-[13px] font-bold text-violet-700 dark:text-violet-100">03</div>
          <div class="flex flex-wrap items-center gap-3">
            <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Objetivo del proyecto</h2>
            <TtsButton :playing="playingId === 'objetivo'" @click="toggleSection('objetivo')" />
          </div>
          <p class="text-sm leading-8 text-slate-600 dark:text-slate-200">
            El objetivo central de EducaTYCs es <strong class="text-slate-900 dark:text-white">construir y mantener una plataforma digital pública, gratuita y en español</strong> que concentre, organice y presente de forma clara las oportunidades educativas disponibles en línea para la comunidad hispanohablante. Esto implica no solo recopilar información, sino garantizar que sea comprensible, verificable y útil para personas con distintos niveles de experiencia navegando en internet.
          </p>
          <p class="text-sm leading-8 text-slate-600 dark:text-slate-200">
            Lo que comenzó como un ejercicio académico en Tecmilenio tiene hoy un propósito más amplio: demostrar que es posible construir herramientas de impacto social desde la universidad, con recursos limitados pero con una dirección clara. EducaTYCs es la prueba de que un proyecto de servicio social bien enfocado puede trascender el aula y convertirse en algo que beneficia a personas reales, todos los días.
          </p>
        </div>
      </section>

      <div class="h-px w-full bg-slate-200 dark:bg-white/20" />

      <!-- ¿Qué sigue? -->
      <section ref="roadmapEl" class="space-y-8">
        <div class="space-y-4">
          <div class="grid h-10 w-10 place-items-center rounded-lg border border-emerald-300/30 bg-emerald-300/12 text-[13px] font-bold text-emerald-700 dark:text-emerald-100">04</div>
          <div class="flex flex-wrap items-center gap-3">
            <h2 class="text-2xl font-bold text-slate-900 dark:text-white">¿Qué sigue para EducaTYCs?</h2>
            <TtsButton :playing="playingId === 'roadmap'" @click="toggleSection('roadmap')" />
          </div>
          <p class="max-w-3xl text-sm leading-8 text-slate-600 dark:text-slate-200">
            EducaTYCs es un proyecto vivo. Lo que existe hoy es solo el punto de partida — hay una hoja de ruta clara de mejoras y nuevas funcionalidades que queremos construir para hacer la plataforma aún más útil para los hispanohablantes del mundo.
          </p>
        </div>

        <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <!-- Etapa actual -->
          <div class="glass-card rounded-xl p-6 space-y-3">
            <div class="flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-emerald-500 shadow shadow-emerald-400/50" />
              <p class="text-xs font-semibold uppercase tracking-widest text-emerald-600 dark:text-emerald-300">En línea ahora</p>
            </div>
            <h3 class="text-base font-bold text-slate-900 dark:text-white">Plataforma web</h3>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-300">
              <li class="flex gap-2"><span class="text-emerald-500 shrink-0">✓</span> Catálogo con más de 1,600 oportunidades</li>
              <li class="flex gap-2"><span class="text-emerald-500 shrink-0">✓</span> Búsqueda y filtros por tipo, tema y fuente</li>
              <li class="flex gap-2"><span class="text-emerald-500 shrink-0">✓</span> Accesibilidad con lectura en voz alta</li>
              <li class="flex gap-2"><span class="text-emerald-500 shrink-0">✓</span> Actualización automática del catálogo</li>
            </ul>
          </div>

          <!-- Próximas mejoras -->
          <div class="glass-card rounded-xl p-6 space-y-3">
            <div class="flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-cyan-500 shadow shadow-cyan-400/50" />
              <p class="text-xs font-semibold uppercase tracking-widest text-cyan-600 dark:text-cyan-300">Próximamente</p>
            </div>
            <h3 class="text-base font-bold text-slate-900 dark:text-white">Mejoras en camino</h3>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-300">
              <li class="flex gap-2"><span class="text-cyan-500 shrink-0">→</span> Alertas de nuevas becas y convocatorias</li>
              <li class="flex gap-2"><span class="text-cyan-500 shrink-0">→</span> Más fuentes: CONACYT, OEI, UNESCO</li>
              <li class="flex gap-2"><span class="text-cyan-500 shrink-0">→</span> Filtros avanzados por país y nivel académico</li>
              <li class="flex gap-2"><span class="text-cyan-500 shrink-0">→</span> Sección de historias de éxito</li>
            </ul>
          </div>

          <!-- App multiplataforma -->
          <div class="glass-card rounded-xl p-6 space-y-3 border border-violet-300/25 bg-violet-300/5">
            <div class="flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-violet-500 shadow shadow-violet-400/50" />
              <p class="text-xs font-semibold uppercase tracking-widest text-violet-600 dark:text-violet-300">Meta a largo plazo</p>
            </div>
            <h3 class="text-base font-bold text-slate-900 dark:text-white">App multiplataforma</h3>
            <p class="text-sm leading-7 text-slate-600 dark:text-slate-300">
              Si los donativos lo permiten, el siguiente gran paso es desarrollar una <strong class="text-slate-900 dark:text-white">aplicación móvil para Android e iOS</strong> — para que cualquier persona pueda explorar oportunidades educativas desde su celular, sin importar si tiene buena conexión a internet.
            </p>
            <a
              href="https://ko-fi.com/educatycs"
              target="_blank"
              rel="noopener noreferrer"
              class="mt-2 inline-flex items-center gap-2 rounded-lg border border-[#FF5E5B]/30 bg-[#FF5E5B]/10 px-3 py-1.5 text-xs font-semibold text-[#FF5E5B] transition-colors hover:bg-[#FF5E5B]/20 dark:border-[#FF5E5B]/40 dark:text-[#FF8C8A]"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 shrink-0" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M18.5 3H5.5C4.12 3 3 4.12 3 5.5v9C3 17.43 5.57 20 8.5 20h7c2.93 0 5.5-2.57 5.5-5.5V9h.5c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2h-.5zm0 5H19V5h-.5v3zM5.5 5h11v9.5C16.5 16.43 14.93 18 13 18H9C7.07 18 5.5 16.43 5.5 14.5V5z"/>
                <path d="M9 11c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1zm4 0c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1z"/>
              </svg>
              Apoyar en Ko-fi
            </a>
          </div>
        </div>
      </section>

    </main>
  </div>
</template>
