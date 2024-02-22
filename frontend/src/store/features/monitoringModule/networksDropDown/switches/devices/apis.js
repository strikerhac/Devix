import { monetxApi } from "../../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllDevicesInSwitches: builder.query({
      query: () =>
        "/api/v1/monitoring/monitoring_network/get_all_devices_in_switch",
    }),
  }),
});

export const { useGetAllDevicesInSwitchesQuery: useFetchRecordsQuery } =
  extendedApi;
