import { monetxApi } from "../../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllDevicesInServers: builder.query({
      query: () =>
        "/api/v1/monitoring/monitoring_server/get_all_devices_in_servers",
    }),
  }),
});

export const { useGetAllDevicesInServersQuery: useFetchRecordsQuery } =
  extendedApi;
