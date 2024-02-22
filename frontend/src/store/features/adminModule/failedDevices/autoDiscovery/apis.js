import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllAdminAutoDiscoveryFailedDevices: builder.query({
      query: () =>
        "/api/v1/users/failed_devices/get_auto_discovery_failed_devices",
    }),
  }),
});

export const {
  useGetAllAdminAutoDiscoveryFailedDevicesQuery: useFetchRecordsQuery,
} = extendedApi;
