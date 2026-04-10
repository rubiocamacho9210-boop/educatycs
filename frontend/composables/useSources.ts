import type { SourceInfo } from '~/types/opportunity'

interface SourcesApiResponse {
  sources: Record<string, { name: string; count: number }>
}

export const useSources = () => {
  return useFetch('/api/opportunities/sources', {
    transform: (raw: SourcesApiResponse): SourceInfo[] =>
      Object.entries(raw.sources).map(([key, info]) => ({
        value: key,
        label: info.name,
        count: info.count,
      })),
  })
}
