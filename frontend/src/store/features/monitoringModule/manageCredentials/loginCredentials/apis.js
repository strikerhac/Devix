import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    monitoringFetchWMICredentials: builder.query({
      query: () => "/api/v1/monitoring/credentials/get_WMI_credentials",
    }),

    monitoringDeleteWMICredentials: builder.mutation({
      query: (data) => ({
        url: "/api/v1/monitoring/credentials/delete_snmp_credentials",
        method: "POST",
        body: data,
      }),
    }),

    monitoringAddWMICredential: builder.mutation({
      query: (data) => ({
        url: "/api/v1/monitoring/credentials/add_WMI_credentials",
        method: "POST",
        body: data,
      }),
    }),

    monitoringUpdateWMICredential: builder.mutation({
      query: (data) => ({
        url: "/api/v1/monitoring/credentials/edit_WMI_credentials",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const {
  useMonitoringFetchWMICredentialsQuery: useFetchRecordsQuery,
  useMonitoringDeleteWMICredentialsMutation: useDeleteRecordsMutation,
  useMonitoringAddWMICredentialMutation: useAddRecordMutation,
  useMonitoringUpdateWMICredentialMutation: useUpdateRecordMutation,
} = extendedApi;
