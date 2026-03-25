export const useOpportunitiesTotal = (
  params: MaybeRef<Record<string, string | number | boolean | undefined>>,
) => {
  const config = useRuntimeConfig()

  return useFetch<{ total: number }>('/opportunities/total', {
    baseURL: config.public.apiBase,
    query: params,
  })
}
