import { fileURLToPath } from "node:url"

const appManifestStubPath = fileURLToPath(new URL("./stubs/app-manifest-stub.mjs", import.meta.url))

const siteUrl = process.env.NUXT_PUBLIC_SITE_URL || "https://educatycs.mx"

export default defineNuxtConfig({
  compatibilityDate: "2026-02-20",
  devtools: { enabled: false },
  modules: ["@nuxtjs/tailwindcss", "@nuxtjs/sitemap"],
  experimental: {
    appManifest: false,
  },
  tailwindcss: {
    cssPath: "~/assets/css/main.css",
    configPath: "tailwind.config.js",
    viewer: false,
  },
  alias: {
    "#app-manifest": appManifestStubPath,
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000",
      gaId: process.env.NUXT_PUBLIC_GA_ID || "G-MQ6QDH92TV",
      siteUrl,
    },
  },
  app: {
    head: {
      htmlAttrs: { lang: "es" },
      charset: "utf-8",
      viewport: "width=device-width, initial-scale=1",
      meta: [
        { name: "author", content: "EducaTYCs" },
        { name: "robots", content: "index, follow" },
        { property: "og:site_name", content: "EducaTYCs" },
        { property: "og:type", content: "website" },
        { property: "og:locale", content: "es_MX" },
        { name: "twitter:card", content: "summary_large_image" },
        { name: "twitter:site", content: "@educatycs" },
      ],
      link: [
        { rel: "canonical", href: siteUrl },
        { rel: "icon", type: "image/x-icon", href: "/favicon.ico" },
      ],
    },
  },
  sitemap: {
    siteUrl,
    urls: [
      "/",
      "/cursos",
      "/becas",
      "/talleres",
      "/acerca-de",
      "/beneficiarios",
      "/contacto",
      "/preguntas-frecuentes",
      "/terminos-y-condiciones",
      "/aviso-de-privacidad",
    ],
  },
})
