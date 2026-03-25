interface SeoOptions {
  title: string
  description: string
  path?: string
  image?: string
}

export function useSeo({ title, description, path = '', image }: SeoOptions) {
  const config = useRuntimeConfig()
  const siteUrl = config.public.siteUrl as string
  const fullUrl = `${siteUrl}${path}`
  const ogImage = image || `${siteUrl}/og-default.png`
  const fullTitle = title.includes('EducaTYCs') ? title : `${title} — EducaTYCs`

  useSeoMeta({
    title: fullTitle,
    description,
    ogTitle: fullTitle,
    ogDescription: description,
    ogUrl: fullUrl,
    ogImage,
    twitterTitle: fullTitle,
    twitterDescription: description,
    twitterImage: ogImage,
  })

  useHead({
    link: [{ rel: 'canonical', href: fullUrl }],
  })
}
