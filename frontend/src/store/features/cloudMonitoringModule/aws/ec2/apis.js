import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllEC2s: builder.query({
      query: () => "/api/v1/monitoring/monitoring_clouds/get_all_ec2",
    }),

    changeEC2Status: builder.mutation({
      query: (data) => ({
        url: "/api/v1/monitoring/monitoring_clouds/change_ec2_status",
        method: "POST",
        body: { id: 0, ec2_status: "enabled" | "disabled" },
      }),
    }),
  }),
});

export const {
  useGetAllEC2sQuery: useFetchRecordsQuery,
  useChangeEC2StatusMutation,
} = extendedApi;
