import type { SourceInfo } from '~/types/opportunity'
import { buildApiUrl } from '~/utils/api'

interface SourcesApiResponse {
  sources: Record<string, { name: string; count: number }>
}

export const useSources = () => {
  const config = useRuntimeConfig()

  return useFetch(buildApiUrl(config.public.apiBase, '/opportunities/sources'), {
    transform: (raw: SourcesApiResponse): SourceInfo[] =>
      Object.entries(raw.sources).map(([key, info]) => ({
        value: key,
        label: info.name,
        count: info.count,
      })),
  })
}
