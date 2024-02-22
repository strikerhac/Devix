import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllAdminIpamFailedDevices: builder.query({
      query: () => "/api/v1/users/failed_devices/get_ipam_failed_devices",
    }),
  }),
});

export const { useGetAllAdminIpamFailedDevicesQuery: useFetchRecordsQuery } =
  extendedApi;
