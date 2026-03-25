import { buildApiUrl } from "~/utils/api"

export const useOpportunitiesTotal = (
  params: MaybeRef<Record<string, string | number | boolean | undefined>>,
) => {
  const config = useRuntimeConfig()

  return useFetch<{ total: number }>(buildApiUrl(config.public.apiBase, '/opportunities/total'), {
    query: params,
  })
}
