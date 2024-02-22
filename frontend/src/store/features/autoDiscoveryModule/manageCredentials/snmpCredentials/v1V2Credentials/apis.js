import { monetxApi } from "../../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    autoDiscoveryFetchV1V2Credentials: builder.query({
      query: () => "/api/v1/auto_discovery/get_snmp_v1_v2_credentials",
    }),

    autoDiscoveryDeleteV1V2Credentials: builder.mutation({
      query: (data) => ({
        url: "/api/v1/auto_discovery/delete_snmp_credentials",
        method: "POST",
        body: data,
      }),
    }),

    autoDiscoveryAddV1V2Credential: builder.mutation({
      query: (data) => ({
        url: "/api/v1/auto_discovery/add_snmp_v1_v2_credentials",
        method: "POST",
        body: data,
      }),
    }),

    autoDiscoveryUpdateV1V2Credential: builder.mutation({
      query: (data) => ({
        url: "/api/v1/auto_discovery/edit_snmp_v1_v2_credentials",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const {
  useAutoDiscoveryFetchV1V2CredentialsQuery: useFetchRecordsQuery,
  useAutoDiscoveryDeleteV1V2CredentialsMutation: useDeleteRecordsMutation,
  useAutoDiscoveryAddV1V2CredentialMutation: useAddRecordMutation,
  useAutoDiscoveryUpdateV1V2CredentialMutation: useUpdateRecordMutation,
} = extendedApi;
