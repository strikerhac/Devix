import { monetxApi } from "../../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllS3s: builder.query({
      query: () => "/api/v1/monitoring/monitoring_clouds/get_all_s3",
    }),

    changeS3Status: builder.mutation({
      query: (data) => ({
        url: "/api/v1/monitoring/monitoring_clouds/change_s3_status",
        method: "POST",
        body: { id: 0, ec2_status: "enabled" | "disabled" },
      }),
    }),
  }),
});

export const {
  useGetAllS3sQuery: useFetchRecordsQuery,
  useChangeS3StatusMutation,
} = extendedApi;
