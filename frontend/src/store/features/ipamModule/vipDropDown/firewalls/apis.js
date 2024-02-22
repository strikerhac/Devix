import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllIpamFirewalls: builder.query({
      query: () => "/api/v1/ipam/ipam_device/get_all_firewall_vip",
    }),
  }),
});

export const { useGetAllIpamFirewallsQuery: useFetchRecordsQuery } =
  extendedApi;
