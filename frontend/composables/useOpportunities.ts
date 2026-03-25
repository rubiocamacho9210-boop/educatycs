import type { Opportunity } from "~/types/opportunity"

export const useOpportunities = (
  params: MaybeRef<Record<string, string | number | boolean | undefined>>,
) => {
  const config = useRuntimeConfig()

  return useFetch<Opportunity[]>("/opportunities/", {
    baseURL: config.public.apiBase,
    query: params,
  })
}
