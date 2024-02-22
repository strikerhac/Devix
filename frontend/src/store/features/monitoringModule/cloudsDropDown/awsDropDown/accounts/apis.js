import { monetxApi } from "../../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllMonitoringAwsAccounts: builder.query({
      query: () => "/api/v1/monitoring/monitoring_clouds/get_aws_credentials",
    }),

    deleteMonitoringAwsAccounts: builder.mutation({
      query: (data) => ({
        url: "/api/v1/monitoring/monitoring_clouds/delete_aws_credentials",
        method: "POST",
        body: data,
      }),
    }),

    addMonitoringAwsAccount: builder.mutation({
      query: (data) => ({
        url: "/api/v1/monitoring/monitoring_clouds/add_aws_credentials",
        method: "POST",
        body: data,
      }),
    }),

    updateMonitoringAwsAccount: builder.mutation({
      query: (data) => ({
        url: "/api/v1/monitoring/monitoring_clouds/edit_aws_credentials",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const {
  useGetAllMonitoringAwsAccountsQuery: useFetchRecordsQuery,
  useDeleteMonitoringAwsAccountsMutation: useDeleteRecordsMutation,
  useAddMonitoringAwsAccountMutation: useAddRecordMutation,
  useUpdateMonitoringAwsAccountMutation: useUpdateRecordMutation,
} = extendedApi;
