import { monetxApi } from "../../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    monitoringFetchV1V2Credentials: builder.query({
      query: () => "/api/v1/monitoring/credentials/get_snmp_v1_v2_credentials",
    }),

    monitoringDeleteV1V2Credentials: builder.mutation({
      query: (data) => ({
        url: "/api/v1/monitoring/credentials/delete_snmp_credentials",
        method: "POST",
        body: data,
      }),
    }),

    monitoringAddV1V2Credential: builder.mutation({
      query: (data) => ({
        url: "/api/v1/monitoring/credentials/add_snmp_v1_v2_credentials",
        method: "POST",
        body: data,
      }),
    }),

    monitoringUpdateV1V2Credential: builder.mutation({
      query: (data) => ({
        url: "/api/v1/monitoring/credentials/edit_snmp_v1_v2_credentials",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const {
  useMonitoringFetchV1V2CredentialsQuery: useFetchRecordsQuery,
  useMonitoringDeleteV1V2CredentialsMutation: useDeleteRecordsMutation,
  useMonitoringAddV1V2CredentialMutation: useAddRecordMutation,
  useMonitoringUpdateV1V2CredentialMutation: useUpdateRecordMutation,
} = extendedApi;
