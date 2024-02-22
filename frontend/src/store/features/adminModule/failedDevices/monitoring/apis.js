import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllAdminMonitoringFailedDevices: builder.query({
      query: () => "/api/v1/users/failed_devices/get_monitoring_failed_devices",
    }),
  }),
});

export const {
  useGetAllAdminMonitoringFailedDevicesQuery: useFetchRecordsQuery,
} = extendedApi;
