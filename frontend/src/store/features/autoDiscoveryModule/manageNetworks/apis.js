import { monetxApi } from "../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    autoDiscoveryFetchNetworks: builder.query({
      query: () => "/api/v1/auto_discovery/get_all_networks",
    }),

    autoDiscoveryAddNetworks: builder.mutation({
      query: (data) => ({
        url: "/api/v1/auto_discovery/add_networks",
        method: "POST",
        body: data,
      }),
    }),

    autoDiscoveryDeleteNetworks: builder.mutation({
      query: (data) => ({
        url: "/api/v1/auto_discovery/delete_networks",
        method: "POST",
        body: data,
      }),
    }),

    autoDiscoveryAddNetwork: builder.mutation({
      query: (data) => ({
        url: "/api/v1/auto_discovery/add_network",
        method: "POST",
        body: data,
      }),
    }),

    autoDiscoveryUpdateNetwork: builder.mutation({
      query: (data) => ({
        url: "/api/v1/auto_discovery/edit_network",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const {
  useAutoDiscoveryFetchNetworksQuery: useFetchRecordsQuery,
  useAutoDiscoveryAddNetworksMutation: useAddRecordsMutation,
  useAutoDiscoveryDeleteNetworksMutation: useDeleteRecordsMutation,
  useAutoDiscoveryAddNetworkMutation: useAddRecordMutation,
  useAutoDiscoveryUpdateNetworkMutation: useUpdateRecordMutation,
} = extendedApi;
