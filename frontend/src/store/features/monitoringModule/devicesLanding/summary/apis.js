import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllAlertsByIpAddress: builder.mutation({
      query: (data) => ({
        url: "/api/v1/monitoring/alerts/get_monitoring_alerts_by_ip_address",
        method: "POST",
        body: data,
      }),
    }), // use api from alerts instead of this api
  }),
});
export const { useGetAllAlertsByIpAddressMutation: useFetchRecordsMutation } =
  extendedApi;
