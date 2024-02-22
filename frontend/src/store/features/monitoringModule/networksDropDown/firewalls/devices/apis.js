import { monetxApi } from "../../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllDevicesInFirewalls: builder.query({
      query: () =>
        "/api/v1/monitoring/monitoring_network/get_all_devices_in_firewall",
    }),
  }),
});

export const { useGetAllDevicesInFirewallsQuery: useFetchRecordsQuery } =
  extendedApi;
