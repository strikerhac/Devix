import { monetxApi } from "../../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllDevicesInNetworks: builder.query({
      query: () =>
        "/api/v1/monitoring/monitoring_network/get_all_devices_in_networks",
    }),
  }),
});

export const { useGetAllDevicesInNetworksQuery: useFetchRecordsQuery } =
  extendedApi;
