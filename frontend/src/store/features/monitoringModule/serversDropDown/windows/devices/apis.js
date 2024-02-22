import { monetxApi } from "../../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllDevicesInWindows: builder.query({
      query: () =>
        "/api/v1/monitoring/monitoring_server/get_all_devices_in_windows",
    }),
  }),
});

export const { useGetAllDevicesInWindowsQuery: useFetchRecordsQuery } =
  extendedApi;
