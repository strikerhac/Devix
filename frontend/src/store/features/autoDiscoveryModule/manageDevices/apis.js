import { monetxApi } from "../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    autoDiscoveryFetchManageDevices: builder.query({
      query: () => "/api/v1/auto_discovery/get_manage_devices",
    }),

    autoDiscoveryCheckCredentialsStatus: builder.query({
      query: () => "/api/v1/auto_discovery/check_credentials_status",
    }),
  }),
});

export const { useAutoDiscoveryFetchManageDevicesQuery: useFetchRecordsQuery } =
  extendedApi;

export const useAutoDiscoveryCheckCredentialsStatusLazyQuery =
  extendedApi.endpoints.autoDiscoveryCheckCredentialsStatus.useLazyQuery;
