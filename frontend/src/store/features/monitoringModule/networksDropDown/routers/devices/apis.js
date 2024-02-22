import { monetxApi } from "../../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllDevicesInRouters: builder.query({
      query: () =>
        "/api/v1/monitoring/monitoring_network/get_all_devices_in_router",
    }),
  }),
});

export const { useGetAllDevicesInRoutersQuery: useFetchRecordsQuery } =
  extendedApi;
