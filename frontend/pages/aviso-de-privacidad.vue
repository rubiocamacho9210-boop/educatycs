<script setup lang="ts">
useSeo({
  title: 'Aviso de Privacidad',
  description: 'Aviso de privacidad de EducaTYCs conforme a la LFPDPPP. Información sobre el tratamiento de datos, uso de cookies y Google Analytics 4, y derechos ARCO.',
  path: '/aviso-de-privacidad',
})

// ── Text-to-Speech ──────────────────────────────────────────────
type SectionId = '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'

const playingId = ref<SectionId | null>(null)
const s1El = ref<HTMLElement | null>(null)
const s2El = ref<HTMLElement | null>(null)
const s3El = ref<HTMLElement | null>(null)
const s4El = ref<HTMLElement | null>(null)
const s5El = ref<HTMLElement | null>(null)
const s6El = ref<HTMLElement | null>(null)
const s7El = ref<HTMLElement | null>(null)
const s8El = ref<HTMLElement | null>(null)
const s9El = ref<HTMLElement | null>(null)

const sectionElMap: Record<SectionId, ReturnType<typeof ref<HTMLElement | null>>> = {
  '1': s1El, '2': s2El, '3': s3El, '4': s4El, '5': s5El,
  '6': s6El, '7': s7El, '8': s8El, '9': s9El,
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
        <h1 class="text-3xl font-bold text-slate-900 dark:text-white">Aviso de Privacidad</h1>
        <p class="mt-2 text-xs text-slate-400">Última actualización: 24 de marzo de 2026</p>
      </div>

      <p class="text-sm leading-7 text-slate-700 dark:text-slate-100">
        En cumplimiento de lo dispuesto por la <strong class="text-slate-900 dark:text-white">Ley Federal de Protección de Datos Personales en Posesión de los Particulares</strong> (en adelante, <strong class="text-slate-900 dark:text-white">"LFPDPPP"</strong>), vigente desde el 21 de marzo de 2025, y demás disposiciones reglamentarias aplicables, el titular de la plataforma <strong class="text-slate-900 dark:text-white">EducaTYCs</strong> (en adelante, el <strong class="text-slate-900 dark:text-white">"Responsable"</strong>) pone a disposición del usuario (en adelante, el <strong class="text-slate-900 dark:text-white">"Titular"</strong>) el presente Aviso de Privacidad, con el objeto de informar sobre el tratamiento que se dará a los datos personales recabados con motivo del uso de la Plataforma.
      </p>

      <div ref="s1El">
        <div class="flex flex-wrap items-center gap-3">
          <h2 class="text-xl font-semibold text-slate-800 dark:text-cyan-100">1. Identidad y domicilio del Responsable</h2>
          <TtsButton :playing="playingId === '1'" @click="toggleSection('1')" />
        </div>
        <p class="mt-3 text-sm leading-7 text-slate-700 dark:text-slate-100">
          El Responsable del tratamiento de sus datos personales es el titular operativo de la plataforma digital <strong class="text-slate-900 dark:text-white">EducaTYCs</strong>, con presencia en línea en el dominio correspondiente. Para cualquier comunicación relacionada con el presente Aviso, el Titular podrá dirigirse a través de la sección <a href="/contacto" class="text-cyan-600 hover:underline dark:text-cyan-300">Contacto</a> disponible en la Plataforma.
        </p>
      </div>

      <div ref="s2El">
        <div class="flex flex-wrap items-center gap-3">
          <h2 class="text-xl font-semibold text-slate-800 dark:text-cyan-100">2. Datos personales que se recaban</h2>
          <TtsButton :playing="playingId === '2'" @click="toggleSection('2')" />
        </div>
        <p class="mt-3 text-sm leading-7 text-slate-700 dark:text-slate-100">
          EducaTYCs opera como una plataforma de consulta pública que <strong class="text-slate-900 dark:text-white">no requiere registro de usuario ni recopila datos personales de identificación directa</strong> tales como nombre, correo electrónico, número telefónico o domicilio. Los únicos datos de naturaleza técnica que pueden ser procesados de manera automática durante la navegación son:
        </p>
        <ul class="mt-3 space-y-2 text-sm leading-7 text-slate-700 dark:text-slate-100 list-none">
          <li class="flex gap-2"><span class="text-cyan-600 shrink-0 dark:text-cyan-300">a)</span> <strong class="text-slate-900 dark:text-white">Datos técnicos de sesión:</strong> dirección IP (anonimizada), tipo y versión de navegador, sistema operativo, páginas visitadas y duración de la sesión, recabados de forma automática por los servidores de alojamiento.</li>
          <li class="flex gap-2"><span class="text-cyan-600 shrink-0 dark:text-cyan-300">b)</span> <strong class="text-slate-900 dark:text-white">Parámetros de búsqueda y filtros:</strong> términos de consulta, tipo de oportunidad y fuente seleccionada dentro de la Plataforma, almacenados exclusivamente en la URL del navegador y no asociados a ningún perfil de usuario.</li>
          <li class="flex gap-2"><span class="text-cyan-600 shrink-0 dark:text-cyan-300">c)</span> <strong class="text-slate-900 dark:text-white">Datos de analítica web:</strong> la Plataforma utiliza <strong class="text-slate-900 dark:text-white">Google Analytics 4 (GA4)</strong>, servicio de medición de audiencias proporcionado por Google LLC. A través de este servicio se recopilan datos sobre número de visitantes, país o región de origen, tipo de dispositivo, navegador, páginas consultadas y duración de las visitas. La dirección IP se anonimiza antes de su procesamiento. Estos datos se transmiten y almacenan en los servidores de Google conforme a su propia política de privacidad.</li>
        </ul>
        <p class="mt-3 text-sm leading-7 text-slate-700 dark:text-slate-100">
          La Plataforma <strong class="text-slate-900 dark:text-white">no recaba datos personales sensibles</strong> en los términos del artículo 3, fracción VI de la LFPDPPP.
        </p>
      </div>

      <div ref="s3El">
        <div class="flex flex-wrap items-center gap-3">
          <h2 class="text-xl font-semibold text-slate-800 dark:text-cyan-100">3. Finalidades del tratamiento</h2>
          <TtsButton :playing="playingId === '3'" @click="toggleSection('3')" />
        </div>
        <p class="mt-3 text-sm leading-7 text-slate-700 dark:text-slate-100">
          Los datos técnicos indicados en el apartado anterior serán tratados exclusivamente para las siguientes <strong class="text-slate-900 dark:text-white">finalidades primarias</strong>, necesarias para la prestación del servicio:
        </p>
        <ul class="mt-3 space-y-2 text-sm leading-7 text-slate-700 dark:text-slate-100 list-none">
          <li class="flex gap-2"><span class="text-cyan-600 shrink-0 dark:text-cyan-300">i)</span> Operar, mantener y mejorar el funcionamiento técnico de la Plataforma.</li>
          <li class="flex gap-2"><span class="text-cyan-600 shrink-0 dark:text-cyan-300">ii)</span> Optimizar la relevancia y presentación del catálogo de oportunidades educativas.</li>
          <li class="flex gap-2"><span class="text-cyan-600 shrink-0 dark:text-cyan-300">iii)</span> Detectar y prevenir incidentes de seguridad, usos no autorizados o actividades ilícitas.</li>
          <li class="flex gap-2"><span class="text-cyan-600 shrink-0 dark:text-cyan-300">iv)</span> Dar cumplimiento a obligaciones legales aplicables.</li>
        </ul>
        <p class="mt-3 text-sm leading-7 text-slate-700 dark:text-slate-100">
          La Plataforma <strong class="text-slate-900 dark:text-white">no realiza tratamiento de datos con finalidades secundarias</strong> tales como mercadotecnia, publicidad personalizada o elaboración de perfiles de comportamiento.
        </p>
      </div>

      <div ref="s4El">
        <div class="flex flex-wrap items-center gap-3">
          <h2 class="text-xl font-semibold text-slate-800 dark:text-cyan-100">4. Transferencia de datos personales</h2>
          <TtsButton :playing="playingId === '4'" @click="toggleSection('4')" />
        </div>
        <p class="mt-3 text-sm leading-7 text-slate-700 dark:text-slate-100">
          El Responsable no realiza transferencias de datos personales a terceros con fines comerciales. Sin embargo, el uso de Google Analytics 4 implica la transmisión de datos de navegación a <strong class="text-slate-900 dark:text-white">Google LLC</strong>, empresa con sede en los Estados Unidos de América, en su calidad de encargada del tratamiento. Dicha transferencia se realiza en el marco de las condiciones de servicio de Google Analytics y bajo el escudo de adecuación y cláusulas contractuales tipo aplicables. Asimismo, los datos técnicos de sesión podrán ser accedidos por prestadores de servicios de infraestructura (alojamiento web, redes de distribución de contenido), quienes estarán obligados a tratarlos conforme a las instrucciones del Responsable. Dichas transferencias se encuentran previstas en el artículo 37 de la LFPDPPP y no requieren el consentimiento del Titular para su realización.
        </p>
      </div>

      <div ref="s5El">
        <div class="flex flex-wrap items-center gap-3">
          <h2 class="text-xl font-semibold text-slate-800 dark:text-cyan-100">5. Uso de cookies y tecnologías de seguimiento</h2>
          <TtsButton :playing="playingId === '5'" @click="toggleSection('5')" />
        </div>
        <p class="mt-3 text-sm leading-7 text-slate-700 dark:text-slate-100">
          La Plataforma utiliza los siguientes tipos de cookies:
        </p>
        <ul class="mt-3 space-y-2 text-sm leading-7 text-slate-700 dark:text-slate-100 list-none">
          <li class="flex gap-2"><span class="text-cyan-600 shrink-0 dark:text-cyan-300">•</span> <strong class="text-slate-900 dark:text-white">Cookies técnicas de sesión:</strong> necesarias para el correcto funcionamiento del sitio. No almacenan información personal identificable y no requieren consentimiento.</li>
          <li class="flex gap-2"><span class="text-cyan-600 shrink-0 dark:text-cyan-300">•</span> <strong class="text-slate-900 dark:text-white">Cookies de analítica — Google Analytics 4:</strong> identificadas como <code class="text-cyan-700 text-xs bg-slate-100 dark:text-cyan-200 dark:bg-white/10 px-1 rounded">_ga</code> y <code class="text-cyan-700 text-xs bg-slate-100 dark:text-cyan-200 dark:bg-white/10 px-1 rounded">_ga_XXXXXXXX</code>, con una vigencia de hasta 2 años. Permiten contabilizar visitas, identificar sesiones únicas y conocer el comportamiento de navegación de forma agregada. Estos datos son procesados por Google LLC conforme a su política de privacidad disponible en <a href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer" class="text-cyan-600 hover:underline dark:text-cyan-300">policies.google.com/privacy</a>.</li>
        </ul>
        <p class="mt-3 text-sm leading-7 text-slate-700 dark:text-slate-100">
          El Usuario puede configurar su navegador para rechazar o eliminar las cookies en cualquier momento; sin embargo, deshabilitar las cookies de analítica no afecta la funcionalidad de la Plataforma. Para bloquear específicamente el seguimiento de Google Analytics, el Usuario también puede instalar el complemento oficial disponible en <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener noreferrer" class="text-cyan-600 hover:underline dark:text-cyan-300">tools.google.com/dlpage/gaoptout</a>.
        </p>
      </div>

      <div ref="s6El">
        <div class="flex flex-wrap items-center gap-3">
          <h2 class="text-xl font-semibold text-slate-800 dark:text-cyan-100">6. Derechos ARCO</h2>
          <TtsButton :playing="playingId === '6'" @click="toggleSection('6')" />
        </div>
        <p class="mt-3 text-sm leading-7 text-slate-700 dark:text-slate-100">
          En términos de lo previsto por los artículos 28 al 40 de la LFPDPPP, el Titular tiene derecho a <strong class="text-slate-900 dark:text-white">Acceder, Rectificar, Cancelar u Oponerse</strong> (derechos <strong class="text-slate-900 dark:text-white">ARCO</strong>) al tratamiento de sus datos personales. Dado que la Plataforma no recaba datos de identificación directa, el ejercicio de dichos derechos procederá únicamente respecto de los datos técnicos que pudieran ser vinculados a su persona conforme a la legislación aplicable. Para ejercer sus derechos ARCO, el Titular deberá enviar su solicitud mediante la sección <a href="/contacto" class="text-cyan-600 hover:underline dark:text-cyan-300">Contacto</a>, indicando el derecho que desea ejercer y los datos que permitan atender su solicitud. El Responsable dará respuesta en los plazos previstos por la LFPDPPP.
        </p>
      </div>

      <div ref="s7El">
        <div class="flex flex-wrap items-center gap-3">
          <h2 class="text-xl font-semibold text-slate-800 dark:text-cyan-100">7. Revocación del consentimiento</h2>
          <TtsButton :playing="playingId === '7'" @click="toggleSection('7')" />
        </div>
        <p class="mt-3 text-sm leading-7 text-slate-700 dark:text-slate-100">
          El Titular podrá revocar en cualquier momento el consentimiento otorgado para el tratamiento de sus datos personales, siempre que ello no sea impedido por una obligación legal. La revocación no tendrá efectos retroactivos. Para hacerla efectiva, deberá seguir el mismo procedimiento indicado para el ejercicio de los derechos ARCO.
        </p>
      </div>

      <div ref="s8El">
        <div class="flex flex-wrap items-center gap-3">
          <h2 class="text-xl font-semibold text-slate-800 dark:text-cyan-100">8. Modificaciones al Aviso de Privacidad</h2>
          <TtsButton :playing="playingId === '8'" @click="toggleSection('8')" />
        </div>
        <p class="mt-3 text-sm leading-7 text-slate-700 dark:text-slate-100">
          El Responsable se reserva el derecho de modificar el presente Aviso de Privacidad en cualquier momento, a fin de adecuarlo a reformas legislativas, criterios jurisprudenciales, políticas internas o cambios en los servicios ofrecidos. Las modificaciones serán publicadas en esta misma página y entrarán en vigor a partir de su publicación. Se recomienda al Titular revisar periódicamente el presente documento.
        </p>
      </div>

      <div ref="s9El">
        <div class="flex flex-wrap items-center gap-3">
          <h2 class="text-xl font-semibold text-slate-800 dark:text-cyan-100">9. Autoridad competente</h2>
          <TtsButton :playing="playingId === '9'" @click="toggleSection('9')" />
        </div>
        <p class="mt-3 text-sm leading-7 text-slate-700 dark:text-slate-100">
          Con motivo de la reforma constitucional publicada en el Diario Oficial de la Federación y de la entrada en vigor de la nueva <strong class="text-slate-900 dark:text-white">Ley Federal de Protección de Datos Personales en Posesión de los Particulares</strong> el 21 de marzo de 2025, las funciones de supervisión, vigilancia y sanción en materia de protección de datos personales de particulares son ejercidas por la <strong class="text-slate-900 dark:text-white">Secretaría Anticorrupción y Buen Gobierno</strong>. Si el Titular considera que su derecho a la protección de datos personales ha sido vulnerado por alguna conducta del Responsable, podrá iniciar el procedimiento correspondiente ante dicha Secretaría. Para más información, visite <a href="https://www.gob.mx/buengobierno" target="_blank" rel="noopener noreferrer" class="text-cyan-600 hover:underline dark:text-cyan-300">www.gob.mx/buengobierno</a>.
        </p>
      </div>

      <p class="text-xs leading-6 text-slate-500 border-t border-slate-200 pt-4 dark:text-slate-400 dark:border-white/10">
        El uso de la Plataforma implica que el Titular ha leído y aceptado el presente Aviso de Privacidad en todos sus términos.
      </p>
    </section>
  </main>
</template>
