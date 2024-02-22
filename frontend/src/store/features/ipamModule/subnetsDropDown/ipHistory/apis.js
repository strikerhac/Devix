import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllIpamIPHistory: builder.query({
      query: () => "/api/v1/ipam/ipam_device/get_all_ip_history",
    }),

    getIpHistoryByIpAddress: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ipam/ipam_device/get_history_by_ip",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const { useGetIpHistoryByIpAddressMutation } = extendedApi;

export const useFetchRecordsLazyQuery =
  extendedApi.endpoints.getAllIpamIPHistory.useLazyQuery;
