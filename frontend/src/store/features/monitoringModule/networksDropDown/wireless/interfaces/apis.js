import { monetxApi } from "../../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllInterfacesInWireless: builder.query({
      query: () =>
        "/api/v1/monitoring/monitoring_network/get_all_devices_interfaces_in_wireless",
    }),
  }),
});

export const { useGetAllInterfacesInWirelessQuery: useFetchRecordsQuery } =
  extendedApi;
