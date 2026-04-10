import type { Opportunity } from "~/types/opportunity"

export const useOpportunities = (
  params: MaybeRef<Record<string, string | number | boolean | undefined>>,
) => {
  return useFetch<Opportunity[]>("/api/opportunities", {
    query: params,
  })
}
