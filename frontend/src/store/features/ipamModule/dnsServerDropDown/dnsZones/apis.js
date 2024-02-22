import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllIpamDnsZones: builder.query({
      query: () => "/api/v1/ipam/ipam_device/get_dns_zones",
    }),

    getIpamDnsZonesByServerId: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ipam/ipam_device/get_dns_zones_by_server_id",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const { useGetIpamDnsZonesByServerIdMutation } = extendedApi;

export const useFetchZonesLazyQuery =
  extendedApi.endpoints.getAllIpamDnsZones.useLazyQuery;
