import { monetxApi } from "../../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllInterfacesInSwitches: builder.query({
      query: () =>
        "/api/v1/monitoring/monitoring_network/get_all_devices_interfaces_in_switch",
    }),
  }),
});

export const { useGetAllInterfacesInSwitchesQuery: useFetchRecordsQuery } =
  extendedApi;
