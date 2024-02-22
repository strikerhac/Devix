import { monetxApi } from "../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllAutoDiscoveryDiscoveredDevices: builder.query({
      query: () => "/api/v1/auto_discovery/get_all_discovery_data",
    }),

    getAutoDiscoveryDiscoveredDevicesBySubnet: builder.mutation({
      query: (data) => ({
        url: "/api/v1/auto_discovery/auto_discover",
        method: "POST",
        body: data,
      }),
    }),

    getAutoDiscoveryDiscoveryFunctionCountsBySubnet: builder.mutation({
      query: (data) => ({
        url: "/api/v1/auto_discovery/get_discovery_function_count",
        method: "POST",
        body: data,
      }),
    }),

    autoDiscoveryAutoDiscoverDevicesBySubnet: builder.mutation({
      query: (data) => ({
        url: "/api/v1/auto_discovery/auto_discover",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const {
  useGetAutoDiscoveryDiscoveredDevicesBySubnetMutation: useFetchRecordsMutation,
  useGetAutoDiscoveryDiscoveryFunctionCountsBySubnetMutation,
  useAutoDiscoveryAutoDiscoverDevicesBySubnetMutation,
} = extendedApi;

export const useGetAllAutoDiscoveryDiscoveredDevicesLazyQuery =
  extendedApi.endpoints.getAllAutoDiscoveryDiscoveredDevices.useLazyQuery;
