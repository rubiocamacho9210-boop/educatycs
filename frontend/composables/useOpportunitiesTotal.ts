export const useOpportunitiesTotal = (
  params: MaybeRef<Record<string, string | number | boolean | undefined>>,
) => {
  return useFetch<{ total: number }>("/api/opportunities/total", {
    query: params,
  })
}
