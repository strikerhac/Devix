import { monetxApi } from "../../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllELBs: builder.query({
      query: () => "/api/v1/monitoring/monitoring_clouds/get_all_elb",
    }),

    changeELBStatus: builder.mutation({
      query: (data) => ({
        url: "/api/v1/monitoring/monitoring_clouds/change_elb_status",
        method: "POST",
        body: { id: 0, ec2_status: "enabled" | "disabled" },
      }),
    }),
  }),
});

export const {
  useGetAllELBsQuery: useFetchRecordsQuery,
  useChangeELBStatusMutation,
} = extendedApi;
