import { monetxApi } from "../../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllInterfacesInFirewalls: builder.query({
      query: () =>
        "/api/v1/monitoring/monitoring_network/get_all_devices_interfaces_in_firewall",
    }),
  }),
});

export const { useGetAllInterfacesInFirewallsQuery: useFetchRecordsQuery } =
  extendedApi;
