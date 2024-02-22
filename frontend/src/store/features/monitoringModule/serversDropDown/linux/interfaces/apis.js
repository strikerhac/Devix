import { monetxApi } from "../../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllInterfacesInLinux: builder.query({
      query: () =>
        "/api/v1/monitoring/monitoring_server/get_all_devices_interfaces_in_linux",
    }),
  }),
});

export const { useGetAllInterfacesInLinuxQuery: useFetchRecordsQuery } =
  extendedApi;
