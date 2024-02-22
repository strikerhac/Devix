import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getFailedDevicesCounts: builder.query({
      query: () => "/api/v1/users/failed_devices/get_failed_devices_count",
    }),
  }),
});

export const { useGetFailedDevicesCountsQuery: useFetchRecordsQuery } =
  extendedApi;
