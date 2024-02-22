import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllIpamLoadBalancers: builder.query({
      query: () => "/api/v1/ipam/ipam_device/get_all_f5",
    }),
  }),
});

export const { useGetAllIpamLoadBalancersQuery: useFetchRecordsQuery } =
  extendedApi;
