import type { SourceInfo } from '~/types/opportunity'

interface SourcesApiResponse {
  sources: Record<string, { name: string; count: number }>
}

export const useSources = () => {
  const config = useRuntimeConfig()

  return useFetch('/opportunities/sources', {
    baseURL: config.public.apiBase,
    transform: (raw: SourcesApiResponse): SourceInfo[] =>
      Object.entries(raw.sources).map(([key, info]) => ({
        value: key,
        label: info.name,
        count: info.count,
      })),
  })
}
