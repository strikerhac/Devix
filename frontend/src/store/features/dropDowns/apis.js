import { monetxApi } from "../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    fetchSiteNames: builder.query({
      query: () => "/api/v1/uam/site/get_sites_dropdown",
    }),

    fetchRackNames: builder.query({
      query: (params) => ({
        url: `/api/v1/uam/rack/get_racks_by_site_dropdown`,
        params: { site_name: params.site_name },
      }),
    }),

    fetchVendorNames: builder.query({
      query: () => "/api/v1/atom/static_list/get_vendor_list",
    }),

    fetchFunctionNames: builder.query({
      query: () => "/api/v1/atom/static_list/get_function_list",
    }),

    fetchDeviceTypeNames: builder.query({
      query: () => "/api/v1/atom/static_list/get_device_type_list",
    }),

    fetchPasswordGroupNames: builder.query({
      query: () => "/api/v1/atom/password_group/get_password_group_dropdown",
    }),

    fetchPasswordGroupTypeNames: builder.query({
      query: () => "/api/v1/atom/static_list/get_password_group_type_dropdown",
    }),

    fetchProductionStatusNames: builder.query({
      query: () => "/api/v1/atom/static_list/get_status_dropdown",
    }),

    fetchSubnetNames: builder.query({
      query: () => "/api/v1/auto_discovery/get_subnets_dropdown",
    }),

    fetchMonitoringCredentialsNames: builder.query({
      query: () =>
        "/api/v1/monitoring/credentials/get_all_monitoring_credentials",
    }),

    fetchV3CredentialsAuthorizationProtocolNames: builder.query({
      query: () =>
        "/api/v1/monitoring/monitoring_static_list/get_authorization_protocol",
    }),

    fetchV3CredentialsEncryptionProtocolNames: builder.query({
      query: () =>
        "/api/v1/monitoring/monitoring_static_list/get_encryption_protocol",
    }),

    fetchIpamDevicesFetchDates: builder.query({
      query: () => "/api/v1/ipam/ipam_device/get_ipam_devices_fetch_dates",
    }),

    fetchAccountTypeNames: builder.query({
      query: () => "/api/v1/users/user_static_list/get_user_account_type",
    }),

    fetchActiveStatusNames: builder.query({
      query: () => "/api/v1/users/user_static_list/get_user_status",
    }),

    fetchUserRoleNames: builder.query({
      query: () => "/api/v1/users/user/get_user_role_dropdown",
    }),

    fetchAtomCriticalityNames: builder.query({
      query: () => "/api/v1/atom/static_list/get_criticality_values_dropdown",
    }),

    fetchAtomVirtualNames: builder.query({
      query: () => "/api/v1/atom/static_list/get_virutal_values_dropdown",
    }),
  }),
});

export const {
  useFetchSiteNamesQuery,
  useFetchRackNamesQuery,
  useFetchVendorNamesQuery,
  useFetchFunctionNamesQuery,
  useFetchDeviceTypeNamesQuery,
  useFetchPasswordGroupNamesQuery,
  useFetchPasswordGroupTypeNamesQuery,
  useFetchProductionStatusNamesQuery,
  useFetchSubnetNamesQuery,
  useFetchActiveStatusNamesQuery,
  useFetchMonitoringCredentialsNamesQuery,
  useFetchV3CredentialsAuthorizationProtocolNamesQuery,
  useFetchV3CredentialsEncryptionProtocolNamesQuery,
  useFetchAccountTypeNamesQuery,
  useFetchUserRoleNamesQuery,
  useFetchAtomCriticalityNamesQuery,
  useFetchAtomVirtualNamesQuery,
} = extendedApi;

export const useFetchIpamDevicesFetchDatesLazyQuery =
  extendedApi.endpoints.fetchIpamDevicesFetchDates.useLazyQuery;
