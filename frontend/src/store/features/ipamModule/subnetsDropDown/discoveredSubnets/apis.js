import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllIpamDiscoveredSubnets: builder.query({
      query: () => "/api/v1/ipam/ipam_device/get_all_discovered_subnet",
    }),
  }),
});

export const { useGetAllIpamDiscoveredSubnetsQuery: useFetchRecordsQuery } =
  extendedApi;
