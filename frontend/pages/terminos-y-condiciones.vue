<script setup lang="ts">
useSeo({
  title: 'Términos y Condiciones de Uso',
  description: 'Términos y condiciones que rigen el acceso y uso de la plataforma EducaTYCs. Información sobre uso permitido, limitación de responsabilidad y propiedad intelectual.',
  path: '/terminos-y-condiciones',
})

// ── Text-to-Speech ──────────────────────────────────────────────
type SectionId = '1' | '2' | '3' | '4' | '5' | '6' | '7'

const playingId = ref<SectionId | null>(null)
const s1El = ref<HTMLElement | null>(null)
const s2El = ref<HTMLElement | null>(null)
const s3El = ref<HTMLElement | null>(null)
const s4El = ref<HTMLElement | null>(null)
const s5El = ref<HTMLElement | null>(null)
const s6El = ref<HTMLElement | null>(null)
const s7El = ref<HTMLElement | null>(null)

const sectionElMap: Record<SectionId, ReturnType<typeof ref<HTMLElement | null>>> = {
  '1': s1El, '2': s2El, '3': s3El, '4': s4El,
  '5': s5El, '6': s6El, '7': s7El,
}

function toggleSection(id: SectionId) {
  if (!import.meta.client) return

  if (playingId.value === id) {
    window.speechSynthesis.cancel()
    playingId.value = null
    return
  }

  window.speechSynthesis.cancel()

  const el = sectionElMap[id].value
  if (!el) return

  const text = Array.from(el.querySelectorAll('h2, p, li'))
    .map(n => n.textContent?.trim())
    .filter(Boolean)
    .join('. ')

  if (!text) return

  const u = new SpeechSynthesisUtterance(text)
  u.lang  = 'es-MX'
  u.rate  = 0.93
  u.pitch = 1.0

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
  <main class="mx-auto max-w-[1440px] px-4 py-12 sm:px-8 lg:px-[120px]">
    <section class="glass-card rounded-2xl p-8 sm:p-10 space-y-6">
      <div>
        <h1 class="text-3xl font-bold text-slate-900 dark:text-white">Términos y Condiciones de Uso</h1>
        <p class="mt-2 text-xs text-slate-400">Última actualización: 24 de marzo de 2026</p>
      </div>

      <p class="text-sm leading-7 text-slate-700 dark:text-slate-100">
        El presente instrumento jurídico establece los términos y condiciones generales (en adelante, los <strong class="text-slate-900 dark:text-white">"Términos"</strong>) que rigen el acceso y uso de la plataforma digital denominada <strong class="text-slate-900 dark:text-white">EducaTYCs</strong> (en adelante, la <strong class="text-slate-900 dark:text-white">"Plataforma"</strong>), operada por sus titulares (en adelante, el <strong class="text-slate-900 dark:text-white">"Titular"</strong>). El acceso, navegación o uso de la Plataforma en cualquier forma constituye la aceptación plena, expresa e incondicional de los presentes Términos por parte del usuario (en adelante, el <strong class="text-slate-900 dark:text-white">"Usuario"</strong>). En caso de no estar de acuerdo con alguna de las disposiciones aquí contenidas, el Usuario deberá abstenerse de utilizar la Plataforma.
      </p>

      <div ref="s1El">
        <div class="flex flex-wrap items-center gap-3">
          <h2 class="text-xl font-semibold text-slate-800 dark:text-cyan-100">1. Naturaleza y objeto de la Plataforma</h2>
          <TtsButton :playing="playingId === '1'" @click="toggleSection('1')" />
        </div>
        <p class="mt-3 text-sm leading-7 text-slate-700 dark:text-slate-100">
          EducaTYCs es una plataforma de agregación y difusión de información educativa de carácter gratuito, cuyo objeto exclusivo es compilar, clasificar y presentar oportunidades educativas —incluyendo cursos, becas, talleres y eventos formativos— ofrecidas por terceros. El Titular actúa en calidad de intermediario informativo y <strong class="text-slate-900 dark:text-white">no es parte</strong> en ninguna relación jurídica, contractual o académica que pudiera establecerse entre el Usuario y las instituciones, organismos o plataformas educativas referenciadas.
        </p>
      </div>

      <div ref="s2El">
        <div class="flex flex-wrap items-center gap-3">
          <h2 class="text-xl font-semibold text-slate-800 dark:text-cyan-100">2. Uso permitido</h2>
          <TtsButton :playing="playingId === '2'" @click="toggleSection('2')" />
        </div>
        <p class="mt-3 text-sm leading-7 text-slate-700 dark:text-slate-100">
          El Usuario queda autorizado a acceder y utilizar la Plataforma exclusivamente para fines informativos, personales y no comerciales. Queda expresamente prohibido:
        </p>
        <ul class="mt-3 space-y-2 text-sm leading-7 text-slate-700 dark:text-slate-100 list-none">
          <li class="flex gap-2"><span class="text-cyan-600 shrink-0 dark:text-cyan-300">a)</span> El uso de sistemas automatizados, robots, scrapers o cualquier herramienta de extracción masiva de datos sin autorización escrita previa del Titular.</li>
          <li class="flex gap-2"><span class="text-cyan-600 shrink-0 dark:text-cyan-300">b)</span> La reproducción, distribución, modificación o explotación comercial del contenido de la Plataforma sin consentimiento expreso.</li>
          <li class="flex gap-2"><span class="text-cyan-600 shrink-0 dark:text-cyan-300">c)</span> Cualquier acción que afecte, interrumpa o degrade la disponibilidad, integridad o seguridad de la Plataforma o sus infraestructuras asociadas.</li>
          <li class="flex gap-2"><span class="text-cyan-600 shrink-0 dark:text-cyan-300">d)</span> El uso de la Plataforma para fines ilícitos, fraudulentos o contrarios a la moral, al orden público o a la legislación aplicable.</li>
        </ul>
      </div>

      <div ref="s3El">
        <div class="flex flex-wrap items-center gap-3">
          <h2 class="text-xl font-semibold text-slate-800 dark:text-cyan-100">3. Exactitud y vigencia de la información</h2>
          <TtsButton :playing="playingId === '3'" @click="toggleSection('3')" />
        </div>
        <p class="mt-3 text-sm leading-7 text-slate-700 dark:text-slate-100">
          La información publicada en la Plataforma proviene de fuentes externas y de acceso público. El Titular realiza esfuerzos razonables para mantenerla actualizada; sin embargo, <strong class="text-slate-900 dark:text-white">no garantiza</strong> la exactitud, completitud, vigencia ni disponibilidad de ninguna convocatoria, beca, curso o taller referenciado. Los requisitos de inscripción, fechas límite, montos de financiamiento, criterios de selección y demás condiciones particulares son determinados de manera exclusiva por cada institución oferente, y el Usuario deberá verificarlos directamente con la fuente correspondiente.
        </p>
        <p class="mt-3 text-sm leading-7 text-slate-700 dark:text-slate-100">
          Asimismo, el Usuario reconoce que el acceso a determinados cursos, becas, talleres u otras oportunidades educativas referenciadas en la Plataforma <strong class="text-slate-900 dark:text-white">puede requerir el registro o la creación de una cuenta en la plataforma o institución tercera correspondiente</strong>, así como el cumplimiento de los términos, condiciones y políticas de privacidad propias de dicha institución. El Titular no es responsable de los requisitos de registro, las políticas de acceso, los cambios de modalidad (gratuita a de pago), ni de ninguna otra condición impuesta por los servicios de terceros. EducaTYCs únicamente facilita el enlace a dichas oportunidades y <strong class="text-slate-900 dark:text-white">no tiene ningún vínculo, afiliación ni responsabilidad</strong> respecto de la operación, contenido o disponibilidad de las plataformas externas.
        </p>
      </div>

      <div ref="s4El">
        <div class="flex flex-wrap items-center gap-3">
          <h2 class="text-xl font-semibold text-slate-800 dark:text-cyan-100">4. Limitación de responsabilidad</h2>
          <TtsButton :playing="playingId === '4'" @click="toggleSection('4')" />
        </div>
        <p class="mt-3 text-sm leading-7 text-slate-700 dark:text-slate-100">
          En la máxima medida permitida por la legislación aplicable, el Titular <strong class="text-slate-900 dark:text-white">no asume responsabilidad alguna</strong> por:
        </p>
        <ul class="mt-3 space-y-2 text-sm leading-7 text-slate-700 dark:text-slate-100 list-none">
          <li class="flex gap-2"><span class="text-cyan-600 shrink-0 dark:text-cyan-300">a)</span> Daños directos, indirectos, incidentales, consecuentes o punitivos derivados del uso o la imposibilidad de uso de la Plataforma.</li>
          <li class="flex gap-2"><span class="text-cyan-600 shrink-0 dark:text-cyan-300">b)</span> La cancelación, modificación o incumplimiento de convocatorias por parte de terceros.</li>
          <li class="flex gap-2"><span class="text-cyan-600 shrink-0 dark:text-cyan-300">c)</span> La veracidad o licitud del contenido publicado en sitios de terceros a los que la Plataforma enlace.</li>
          <li class="flex gap-2"><span class="text-cyan-600 shrink-0 dark:text-cyan-300">d)</span> Pérdidas económicas, académicas o de cualquier naturaleza derivadas de decisiones tomadas con base en la información publicada.</li>
        </ul>
      </div>

      <div ref="s5El">
        <div class="flex flex-wrap items-center gap-3">
          <h2 class="text-xl font-semibold text-slate-800 dark:text-cyan-100">5. Propiedad intelectual</h2>
          <TtsButton :playing="playingId === '5'" @click="toggleSection('5')" />
        </div>
        <p class="mt-3 text-sm leading-7 text-slate-700 dark:text-slate-100">
          La denominación, diseño, logotipos, código fuente, estructura, selección y disposición del contenido de la Plataforma son propiedad del Titular o de sus licenciantes y se encuentran protegidos por las leyes de propiedad intelectual e industrial aplicables. El acceso a la Plataforma no otorga al Usuario ningún derecho de propiedad sobre dichos elementos. Las marcas, nombres comerciales y demás signos distintivos de terceros que aparezcan en la Plataforma son propiedad de sus respectivos titulares.
        </p>
      </div>

      <div ref="s6El">
        <div class="flex flex-wrap items-center gap-3">
          <h2 class="text-xl font-semibold text-slate-800 dark:text-cyan-100">6. Modificaciones</h2>
          <TtsButton :playing="playingId === '6'" @click="toggleSection('6')" />
        </div>
        <p class="mt-3 text-sm leading-7 text-slate-700 dark:text-slate-100">
          El Titular se reserva el derecho de modificar, suspender o discontinuar, en todo o en parte, la Plataforma o los presentes Términos en cualquier momento y sin previo aviso. Las modificaciones entrarán en vigor desde su publicación en la Plataforma. El uso continuado de la Plataforma tras la publicación de modificaciones constituirá aceptación de los nuevos Términos.
        </p>
      </div>

      <div ref="s7El">
        <div class="flex flex-wrap items-center gap-3">
          <h2 class="text-xl font-semibold text-slate-800 dark:text-cyan-100">7. Legislación aplicable y jurisdicción</h2>
          <TtsButton :playing="playingId === '7'" @click="toggleSection('7')" />
        </div>
        <p class="mt-3 text-sm leading-7 text-slate-700 dark:text-slate-100">
          Los presentes Términos se rigen e interpretan conforme a la legislación de los Estados Unidos Mexicanos. Para la resolución de cualquier controversia derivada de la interpretación, cumplimiento o incumplimiento de los presentes Términos, las partes se someten expresamente a la jurisdicción de los tribunales competentes, renunciando a cualquier otro fuero que pudiera corresponderles por razón de su domicilio presente o futuro.
        </p>
      </div>

      <p class="text-xs leading-6 text-slate-400 border-t border-slate-200 pt-4 dark:border-white/10">
        Si tiene dudas respecto al contenido de los presentes Términos, puede contactarnos a través de la sección <a href="/contacto" class="text-cyan-600 hover:underline dark:text-cyan-300">Contacto</a> de la Plataforma.
      </p>
    </section>
  </main>
</template>
