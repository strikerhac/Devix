import { monetxApi } from "../../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllDevicesInLinux: builder.query({
      query: () =>
        "/api/v1/monitoring/monitoring_server/get_all_devices_in_linux",
    }),
  }),
});

export const { useGetAllDevicesInLinuxQuery: useFetchRecordsQuery } =
  extendedApi;
