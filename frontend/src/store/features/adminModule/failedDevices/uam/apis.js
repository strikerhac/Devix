import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllAdminUamFailedDevices: builder.query({
      query: () => "/api/v1/users/failed_devices/get_uam_failed_devices",
    }),
  }),
});

export const { useGetAllAdminUamFailedDevicesQuery: useFetchRecordsQuery } =
  extendedApi;
