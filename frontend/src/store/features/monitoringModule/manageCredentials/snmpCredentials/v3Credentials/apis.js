import { monetxApi } from "../../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    monitoringFetchV3Credentials: builder.query({
      query: () => "/api/v1/monitoring/credentials/get_snmp_v3_credentials",
    }),

    monitoringDeleteV3Credentials: builder.mutation({
      query: (data) => ({
        url: "/api/v1/monitoring/credentials/delete_snmp_credentials",
        method: "POST",
        body: data,
      }),
    }),

    monitoringAddV3Credential: builder.mutation({
      query: (data) => ({
        url: "/api/v1/monitoring/credentials/add_snmp_v3_credentials",
        method: "POST",
        body: data,
      }),
    }),

    monitoringUpdateV3Credential: builder.mutation({
      query: (data) => ({
        url: "/api/v1/monitoring/credentials/edit_snmp_v3_credentials",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const {
  useMonitoringFetchV3CredentialsQuery: useFetchRecordsQuery,
  useMonitoringDeleteV3CredentialsMutation: useDeleteRecordsMutation,
  useMonitoringAddV3CredentialMutation: useAddRecordMutation,
  useMonitoringUpdateV3CredentialMutation: useUpdateRecordMutation,
} = extendedApi;
