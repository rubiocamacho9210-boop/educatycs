<script setup lang="ts">
// ── Types ────────────────────────────────────────────────────────
interface Message {
  from: 'bot' | 'user'
  text: string
}

interface QuickReply {
  label: string
  value: string
}

// ── State ────────────────────────────────────────────────────────
const open      = ref(false)
const input     = ref('')
const messages  = ref<Message[]>([])
const messagesEl = ref<HTMLElement | null>(null)

// ── Knowledge base ───────────────────────────────────────────────
const QUICK_REPLIES: QuickReply[] = [
  { label: '¿Qué es EducaTYCs?',        value: '¿qué es educatycs?' },
  { label: '¿Cómo busco?',              value: '¿cómo busco oportunidades?' },
  { label: '¿Qué tipos hay?',           value: '¿qué tipos de oportunidades hay?' },
  { label: '¿Es gratuito?',             value: '¿es gratuito?' },
  { label: '¿Para quién es?',           value: '¿para quién es?' },
  { label: '¿Cómo contactar?',          value: '¿cómo puedo contactarlos?' },
  { label: '¿Cómo apoyar?',             value: '¿cómo puedo apoyar el proyecto?' },
]

const RULES: { keywords: string[]; answer: string }[] = [
  {
    keywords: ['qué es', 'que es', 'educatycs', 'plataforma', 'de qué trata', 'de que trata'],
    answer:
      'EducaTYCs es una plataforma gratuita que reúne cursos, becas y talleres en línea para cualquier persona hispanohablante. Nació como proyecto de servicio social en la Universidad Tecmilenio en 2026, con el objetivo de que nadie tenga que buscar en decenas de sitios distintos para encontrar una oportunidad educativa.',
  },
  {
    keywords: ['cómo busco', 'como busco', 'buscar', 'encontrar', 'filtro', 'filtrar', 'buscador'],
    answer:
      'En la página principal encontrarás un buscador y varios filtros. Puedes buscar por palabra clave, filtrar por tipo de oportunidad (cursos, becas o talleres), por fuente o por tema. También puedes usar las etiquetas de colores que aparecen bajo los filtros para explorar por categoría.',
  },
  {
    keywords: ['tipos', 'categorías', 'categorias', 'qué hay', 'que hay', 'cursos', 'becas', 'talleres'],
    answer:
      'Tenemos tres tipos principales:\n• 📚 Cursos — más de 1,600 de plataformas como Khan Academy, Coursera, UNAM y edX.\n• 🏆 Becas — internacionales como DAAD, Fulbright, Erasmus+, OEA, Chevening y más.\n• 🛠️ Talleres — de habilidades digitales de Capacítate para el Empleo y Grow with Google.',
  },
  {
    keywords: ['gratuito', 'gratis', 'costo', 'precio', 'cobran', 'pagar', 'registro', 'registrar'],
    answer:
      'Sí, EducaTYCs es 100 % gratuito. No necesitas registrarte ni dar tu correo para ver las oportunidades. Las oportunidades del catálogo también son gratuitas en su mayoría — cuando alguna tiene costo, lo indicamos.',
  },
  {
    keywords: ['para quién', 'para quien', 'dirigido', 'estudiante', 'docente', 'maestro', 'profesionista', 'profesional'],
    answer:
      'EducaTYCs está dirigido a cualquier persona de habla hispana:\n• 🎓 Estudiantes — desde preparatoria hasta posgrado.\n• 👩‍🏫 Docentes — talleres para actualizar habilidades digitales y práctica educativa.\n• 💼 Profesionistas — cursos de upskilling, becas para maestrías y certificaciones.',
  },
  {
    keywords: ['contacto', 'contactar', 'escribir', 'mensaje', 'correo', 'reportar', 'error', 'enlace'],
    answer:
      'Puedes escribirnos desde la sección Contacto en el menú. Respondemos dudas, sugerencias de nuevas oportunidades y reportes de enlaces rotos o información desactualizada.',
  },
  {
    keywords: ['apoyar', 'donativo', 'donar', 'ko-fi', 'kofi', 'dinero', 'contribuir', 'ayudar', 'financiar'],
    answer:
      'Puedes apoyarnos en Ko-fi con una donación voluntaria desde ko-fi.com/educatycs. Los fondos se usan exclusivamente para pagar el servidor y el dominio. Si se juntan suficientes donativos, el siguiente paso es desarrollar una app móvil para Android e iOS. ¡Todo suma!',
  },
  {
    keywords: ['app', 'aplicación', 'aplicacion', 'móvil', 'movil', 'android', 'ios', 'futuro', 'planes'],
    answer:
      'Una app multiplataforma para Android e iOS es la meta a largo plazo. Si los donativos del proyecto lo permiten, permitiría explorar oportunidades desde el celular incluso con conexión lenta. Puedes apoyar ese objetivo en ko-fi.com/educatycs.',
  },
  {
    keywords: ['hola', 'buenos días', 'buenas tardes', 'buenas noches', 'hey', 'hi'],
    answer:
      '¡Hola! 👋 Estoy aquí para ayudarte con cualquier duda sobre EducaTYCs. Puedes preguntarme lo que quieras o elegir una opción rápida.',
  },
  {
    keywords: ['gracias', 'muchas gracias', 'thank'],
    answer: '¡De nada! Si tienes más preguntas, aquí estoy. 😊',
  },
  {
    keywords: ['adios', 'adiós', 'hasta luego', 'bye', 'chao', 'chau'],
    answer: '¡Hasta luego! Espero haberte ayudado. Recuerda que puedes volver cuando quieras. 👋',
  },
]

const FALLBACK =
  'No estoy seguro de entender tu pregunta. Prueba con alguna de las opciones rápidas o visita la sección de Preguntas frecuentes para más información.'

// ── Logic ────────────────────────────────────────────────────────
function getAnswer(text: string): string {
  const normalized = text.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
  for (const rule of RULES) {
    if (rule.keywords.some(k => normalized.includes(k.normalize('NFD').replace(/[\u0300-\u036f]/g, '')))) {
      return rule.answer
    }
  }
  return FALLBACK
}

function addMessage(from: 'bot' | 'user', text: string) {
  messages.value.push({ from, text })
  nextTick(() => {
    if (messagesEl.value)
      messagesEl.value.scrollTop = messagesEl.value.scrollHeight
  })
}

function send(text: string) {
  const trimmed = text.trim()
  if (!trimmed) return
  input.value = ''
  addMessage('user', trimmed)
  setTimeout(() => addMessage('bot', getAnswer(trimmed)), 350)
}

function openChat() {
  open.value = true
  if (messages.value.length === 0) {
    setTimeout(() => addMessage('bot', '¡Hola! 👋 Soy el asistente de EducaTYCs. ¿En qué te puedo ayudar hoy?'), 200)
  }
}

function handleKey(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    send(input.value)
  }
}

// ── Computed: show quick replies only when last message is from bot ─
const showQuickReplies = computed(() => {
  if (!messages.value.length) return false
  return messages.value[messages.value.length - 1].from === 'bot'
})

// ── Text-to-Speech ───────────────────────────────────────────────
const playingMsgIdx = ref<number | null>(null)

function toggleSpeak(idx: number, text: string) {
  if (!import.meta.client) return

  if (playingMsgIdx.value === idx) {
    window.speechSynthesis.cancel()
    playingMsgIdx.value = null
    return
  }

  window.speechSynthesis.cancel()

  const u = new SpeechSynthesisUtterance(text)
  u.lang  = 'es-MX'
  u.rate  = 0.93
  u.pitch = 1.0

  const voices = window.speechSynthesis.getVoices()
  const esVoice = voices.find(v => v.lang.startsWith('es')) ?? null
  if (esVoice) u.voice = esVoice

  u.onend   = () => { if (playingMsgIdx.value === idx) playingMsgIdx.value = null }
  u.onerror = () => { playingMsgIdx.value = null }

  playingMsgIdx.value = idx
  window.speechSynthesis.speak(u)
}

onUnmounted(() => {
  if (import.meta.client) window.speechSynthesis.cancel()
})
</script>

<template>
  <!-- Floating button -->
  <div class="fixed bottom-5 right-5 z-50 flex flex-col items-end gap-3">

    <!-- Chat panel -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="translate-y-4 opacity-0 scale-95"
      enter-to-class="translate-y-0 opacity-100 scale-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="translate-y-0 opacity-100 scale-100"
      leave-to-class="translate-y-4 opacity-0 scale-95"
    >
      <div
        v-if="open"
        class="flex w-[min(360px,calc(100vw-2.5rem))] flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-2xl dark:border-white/15 dark:bg-slate-900"
        role="dialog"
        aria-label="Asistente de EducaTYCs"
      >
        <!-- Header -->
        <div class="flex items-center justify-between bg-gradient-to-r from-cyan-500 to-violet-600 px-4 py-3">
          <div class="flex items-center gap-2.5">
            <div class="flex h-8 w-8 items-center justify-center rounded-full bg-white/20 text-white text-sm font-bold">E</div>
            <div>
              <p class="text-sm font-semibold text-white leading-none">Asistente EducaTYCs</p>
              <p class="text-[11px] text-white/70 mt-0.5">Respuestas sobre la plataforma</p>
            </div>
          </div>
          <button
            type="button"
            aria-label="Cerrar chat"
            class="rounded-lg p-1 text-white/80 hover:bg-white/20 transition-colors"
            @click="open = false"
          >
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Messages -->
        <div
          ref="messagesEl"
          class="flex flex-col gap-3 overflow-y-auto px-4 py-4"
          style="max-height: 320px; min-height: 160px;"
        >
          <div
            v-for="(msg, i) in messages"
            :key="i"
            :class="msg.from === 'bot' ? 'items-start' : 'items-end'"
            class="flex flex-col gap-1"
          >
            <div
              :class="msg.from === 'bot'
                ? 'rounded-2xl rounded-tl-sm bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-100'
                : 'rounded-2xl rounded-tr-sm bg-gradient-to-br from-cyan-500 to-violet-600 text-white'"
              class="max-w-[85%] px-3.5 py-2.5 text-sm leading-6 whitespace-pre-line"
            >
              {{ msg.text }}
            </div>
            <!-- TTS button — solo en mensajes del bot -->
            <button
              v-if="msg.from === 'bot'"
              type="button"
              :aria-label="playingMsgIdx === i ? 'Detener audio' : 'Escuchar respuesta'"
              class="flex items-center gap-1 rounded-full px-2 py-0.5 text-[10px] font-medium transition-colors"
              :class="playingMsgIdx === i
                ? 'text-cyan-600 dark:text-cyan-300'
                : 'text-slate-400 hover:text-cyan-600 dark:text-slate-500 dark:hover:text-cyan-300'"
              @click="toggleSpeak(i, msg.text)"
            >
              <!-- Equalizer cuando está sonando -->
              <span v-if="playingMsgIdx === i" class="flex items-end gap-px h-3" aria-hidden="true">
                <span class="w-0.5 rounded-sm bg-current animate-eq-1" />
                <span class="w-0.5 rounded-sm bg-current animate-eq-2" />
                <span class="w-0.5 rounded-sm bg-current animate-eq-3" />
              </span>
              <!-- Speaker cuando no está sonando -->
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.707.707L4.586 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.586l3.707-3.707a1 1 0 011.09-.217zM14.657 2.929a1 1 0 011.414 0A9.972 9.972 0 0119 10a9.972 9.972 0 01-2.929 7.071 1 1 0 01-1.414-1.414A7.971 7.971 0 0017 10c0-2.21-.894-4.208-2.343-5.657a1 1 0 010-1.414zm-2.829 2.828a1 1 0 011.415 0A5.983 5.983 0 0115 10a5.984 5.984 0 01-1.757 4.243 1 1 0 01-1.415-1.415A3.984 3.984 0 0013 10a3.983 3.983 0 00-1.172-2.828 1 1 0 010-1.415z" clip-rule="evenodd" />
              </svg>
              {{ playingMsgIdx === i ? 'Detener' : 'Escuchar' }}
            </button>
          </div>
        </div>

        <!-- Quick replies -->
        <div v-if="showQuickReplies" class="flex flex-wrap gap-1.5 border-t border-slate-100 px-3 py-2.5 dark:border-white/10">
          <button
            v-for="qr in QUICK_REPLIES"
            :key="qr.value"
            type="button"
            class="rounded-full border border-slate-200 bg-slate-50 px-2.5 py-1 text-[11px] font-medium text-slate-600 transition-colors hover:border-cyan-400/50 hover:bg-cyan-50 hover:text-cyan-700 dark:border-white/15 dark:bg-white/5 dark:text-slate-300 dark:hover:border-cyan-400/40 dark:hover:text-cyan-300"
            @click="send(qr.value)"
          >
            {{ qr.label }}
          </button>
        </div>

        <!-- Input -->
        <div class="flex items-center gap-2 border-t border-slate-100 px-3 py-2.5 dark:border-white/10">
          <input
            v-model="input"
            type="text"
            placeholder="Escribe tu pregunta…"
            maxlength="200"
            class="flex-1 rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:ring-offset-0 dark:border-white/15 dark:bg-slate-800 dark:text-slate-100 dark:placeholder:text-slate-500"
            @keydown="handleKey"
          />
          <button
            type="button"
            aria-label="Enviar mensaje"
            :disabled="!input.trim()"
            class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-cyan-500 to-violet-600 text-white transition-opacity disabled:opacity-40"
            @click="send(input)"
          >
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>
      </div>
    </Transition>

    <!-- Toggle button -->
    <button
      type="button"
      :aria-label="open ? 'Cerrar asistente' : 'Abrir asistente'"
      :aria-expanded="open"
      class="flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-br from-cyan-500 to-violet-600 text-white shadow-lg shadow-violet-500/30 transition-transform hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:ring-offset-2"
      @click="open ? (open = false) : openChat()"
    >
      <!-- Chat icon -->
      <svg v-if="!open" class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
      </svg>
      <!-- Close icon -->
      <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
      </svg>
    </button>

  </div>
</template>

<style scoped>
@keyframes eq {
  0%, 100% { height: 0.2rem; }
  50%       { height: 0.75rem; }
}
.animate-eq-1 { animation: eq 0.8s ease-in-out infinite; }
.animate-eq-2 { animation: eq 0.8s ease-in-out infinite 0.2s; }
.animate-eq-3 { animation: eq 0.8s ease-in-out infinite 0.4s; }
</style>
