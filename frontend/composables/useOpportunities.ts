import type { Opportunity } from "~/types/opportunity"
import { buildApiUrl } from "~/utils/api"

export const useOpportunities = (
  params: MaybeRef<Record<string, string | number | boolean | undefined>>,
) => {
  const config = useRuntimeConfig()

  return useFetch<Opportunity[]>(buildApiUrl(config.public.apiBase, "/opportunities/"), {
    query: params,
  })
}
