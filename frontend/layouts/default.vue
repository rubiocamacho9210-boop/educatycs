<script setup lang="ts">
const { isDark, toggle } = useColorMode()
</script>

<template>
  <div class="neon-bg flex min-h-screen flex-col">
    <header class="sticky top-0 z-20 border-b border-slate-200 bg-white/90 backdrop-blur-xl dark:border-white/15 dark:bg-slate-950/45">
      <div class="mx-auto flex h-16 w-full max-w-[1440px] items-center justify-between px-4 sm:px-8 lg:px-[120px]">
        <NuxtLink to="/" class="leading-tight" aria-label="Ir a inicio">
          <p class="text-[17px] font-bold text-slate-900 dark:text-white">EducaTYCs</p>
          <p class="hidden text-[13px] text-slate-500 md:block dark:text-slate-300">Oportunidades educativas para hispanohablantes</p>
        </NuxtLink>

        <div class="flex items-center gap-1">
          <nav aria-label="Navegación principal" class="flex items-center gap-1">
            <NuxtLink
              to="/"
              class="rounded-md px-3.5 py-2.5 text-sm transition-colors"
              :class="$route.path === '/' ? 'font-semibold text-cyan-600 dark:text-cyan-300' : 'text-slate-600 hover:text-pink-600 dark:text-slate-200 dark:hover:text-pink-300'"
            >
              Principal
            </NuxtLink>
            <NuxtLink
              to="/acerca-de"
              class="rounded-md px-3.5 py-2.5 text-sm transition-colors"
              :class="$route.path === '/acerca-de' ? 'font-semibold text-cyan-600 dark:text-cyan-300' : 'text-slate-600 hover:text-pink-600 dark:text-slate-200 dark:hover:text-pink-300'"
            >
              Acerca de
            </NuxtLink>
            <NuxtLink
              to="/beneficiarios"
              class="rounded-md px-3.5 py-2.5 text-sm transition-colors"
              :class="$route.path === '/beneficiarios' ? 'font-semibold text-cyan-600 dark:text-cyan-300' : 'text-slate-600 hover:text-pink-600 dark:text-slate-200 dark:hover:text-pink-300'"
            >
              ¿Para quién?
            </NuxtLink>
          </nav>

          <!-- Dark/light toggle -->
          <button
            type="button"
            :aria-label="isDark ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro'"
            class="ml-2 rounded-md p-2 text-slate-500 transition-colors hover:bg-slate-100 hover:text-slate-700 dark:text-slate-400 dark:hover:bg-white/10 dark:hover:text-slate-200"
            @click="toggle"
          >
            <!-- Sun icon — shown in dark mode -->
            <svg v-if="isDark" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <!-- Moon icon — shown in light mode -->
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>
        </div>
      </div>
    </header>

    <div class="flex-1">
      <slot />
    </div>

    <ChatBot />

    <footer class="border-t border-slate-200 bg-slate-50 py-6 dark:border-white/10 dark:bg-slate-950/35">
      <div class="mx-auto max-w-[1440px] space-y-4 px-4 sm:px-8 lg:px-[120px]">
        <nav aria-label="Enlaces del sitio" class="flex flex-wrap items-center justify-center gap-x-5 gap-y-2 text-xs">
          <NuxtLink to="/terminos-y-condiciones" class="text-slate-500 transition-colors hover:text-cyan-600 dark:text-slate-200 dark:hover:text-cyan-200">Términos y condiciones</NuxtLink>
          <NuxtLink to="/aviso-de-privacidad" class="text-slate-500 transition-colors hover:text-cyan-600 dark:text-slate-200 dark:hover:text-cyan-200">Aviso de privacidad</NuxtLink>
          <NuxtLink to="/preguntas-frecuentes" class="text-slate-500 transition-colors hover:text-cyan-600 dark:text-slate-200 dark:hover:text-cyan-200">Preguntas frecuentes</NuxtLink>
          <NuxtLink to="/contacto" class="text-slate-500 transition-colors hover:text-cyan-600 dark:text-slate-200 dark:hover:text-cyan-200">Contacto</NuxtLink>
          <NuxtLink to="/acerca-de" class="text-slate-500 transition-colors hover:text-cyan-600 dark:text-slate-200 dark:hover:text-cyan-200">Acerca de</NuxtLink>
        </nav>

        <!-- Ko-fi -->
        <div class="flex justify-center">
          <a
            href="https://ko-fi.com/educatycs"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-flex items-center gap-2 rounded-full border border-[#FF5E5B]/30 bg-[#FF5E5B]/10 px-4 py-1.5 text-xs font-semibold text-[#FF5E5B] transition-colors hover:bg-[#FF5E5B]/20 dark:border-[#FF5E5B]/40 dark:bg-[#FF5E5B]/10 dark:text-[#FF8C8A]"
            aria-label="Apoyar a EducaTYCs en Ko-fi"
          >
            <!-- Ko-fi cup icon -->
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 shrink-0" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M18.5 3H5.5C4.12 3 3 4.12 3 5.5v9C3 17.43 5.57 20 8.5 20h7c2.93 0 5.5-2.57 5.5-5.5V9h.5c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2h-.5zm0 5H19V5h-.5v3zM5.5 5h11v9.5C16.5 16.43 14.93 18 13 18H9C7.07 18 5.5 16.43 5.5 14.5V5z"/>
              <path d="M9 11c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1zm4 0c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1z"/>
            </svg>
            Apoyar en Ko-fi
          </a>
        </div>

        <div class="text-center text-xs text-slate-500 dark:text-slate-300">
          © 2026 EducaTYCs. Todos los derechos reservados · Cursos, becas y talleres gratuitos en línea para hispanohablantes
        </div>
      </div>
    </footer>
  </div>
</template>
