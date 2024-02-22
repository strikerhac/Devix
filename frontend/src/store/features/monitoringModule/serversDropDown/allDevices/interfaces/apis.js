import { monetxApi } from "../../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllInterfacesInServers: builder.query({
      query: () =>
        "/api/v1/monitoring/monitoring_server/get_all_devices_interfaces_in_servers",
    }),
  }),
});

export const { useGetAllInterfacesInServersQuery: useFetchRecordsQuery } =
  extendedApi;
