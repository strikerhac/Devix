import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllAdminNcmFailedDevices: builder.query({
      query: () => "/api/v1/users/failed_devices/get_ncm_failed_devices",
    }),
  }),
});

export const { useGetAllAdminNcmFailedDevicesQuery: useFetchRecordsQuery } =
  extendedApi;
