import { monetxApi } from "../../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllInterfacesInNetworks: builder.query({
      query: () =>
        "/api/v1/monitoring/monitoring_network/get_all_devices_interfaces_in_networks",
    }),
  }),
});

export const { useGetAllInterfacesInNetworksQuery: useFetchRecordsQuery } =
  extendedApi;
