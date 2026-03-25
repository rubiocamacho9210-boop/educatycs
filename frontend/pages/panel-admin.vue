<template>
  <div>
    <HeroCarousel />

    <main class="mx-auto flex max-w-[1440px] justify-center px-4 py-20 sm:px-8 lg:px-[120px]">
      <section class="glass-card w-full max-w-[440px] space-y-6 rounded-2xl px-8 py-10 sm:px-10 sm:py-12">
        <div class="grid h-14 w-14 place-items-center rounded-xl border border-cyan-300/30 bg-cyan-300/12 text-2xl">🔒</div>

        <div class="space-y-2">
          <h1 class="text-3xl font-bold text-white">Acceso Administrativo</h1>
          <p class="text-sm leading-relaxed text-slate-200">
            Ingresa tus credenciales para acceder al panel de gestión de oportunidades educativas.
          </p>
        </div>

        <form class="space-y-4" @submit.prevent>
          <div class="space-y-1.5">
            <label for="email" class="text-sm font-semibold text-slate-100">Correo electrónico</label>
            <input
              id="email"
              type="email"
              placeholder="admin@educatycs.mx"
              class="h-11 w-full rounded-lg border border-white/20 bg-slate-900/55 px-3.5 text-sm text-slate-100 placeholder:text-slate-400 focus:border-cyan-300 focus:outline-none"
            >
          </div>

          <div class="space-y-1.5">
            <label for="password" class="text-sm font-semibold text-slate-100">Contraseña</label>
            <input
              id="password"
              type="password"
              placeholder="••••••••••"
              class="h-11 w-full rounded-lg border border-white/20 bg-slate-900/55 px-3.5 text-sm text-slate-100 placeholder:text-slate-400 focus:border-cyan-300 focus:outline-none"
            >
          </div>

          <button
            type="submit"
            class="neon-btn h-11 w-full rounded-lg text-sm font-semibold transition-all"
          >
            Iniciar sesión
          </button>
        </form>

        <p class="whitespace-pre-line text-xs leading-relaxed text-slate-300">
          Acceso restringido a personal autorizado.
          No compartas tus credenciales.
        </p>
      </section>
    </main>
  </div>
</template>
