import { monetxApi } from "../../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllDevicesInWireless: builder.query({
      query: () =>
        "/api/v1/monitoring/monitoring_network/get_all_devices_in_wireless",
    }),
  }),
});

export const { useGetAllDevicesInWirelessQuery: useFetchRecordsQuery } =
  extendedApi;
