import { monetxApi } from "../../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    autoDiscoveryFetchV3Credentials: builder.query({
      query: () => "/api/v1/auto_discovery/get_snmp_v3_credentials",
    }),

    autoDiscoveryDeleteV3Credentials: builder.mutation({
      query: (data) => ({
        url: "/api/v1/auto_discovery/delete_snmp_credentials",
        method: "POST",
        body: data,
      }),
    }),

    autoDiscoveryAddV3Credential: builder.mutation({
      query: (data) => ({
        url: "/api/v1/auto_discovery/add_snmp_v3_credentials",
        method: "POST",
        body: data,
      }),
    }),

    autoDiscoveryUpdateV3Credential: builder.mutation({
      query: (data) => ({
        url: "/api/v1/auto_discovery/edit_snmp_v3_credentials",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const {
  useAutoDiscoveryFetchV3CredentialsQuery: useFetchRecordsQuery,
  useAutoDiscoveryDeleteV3CredentialsMutation: useDeleteRecordsMutation,
  useAutoDiscoveryAddV3CredentialMutation: useAddRecordMutation,
  useAutoDiscoveryUpdateV3CredentialMutation: useUpdateRecordMutation,
} = extendedApi;
