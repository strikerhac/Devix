import { monetxApi } from "../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    //table apis
    fetchDevices: builder.query({
      query: () => "/api/v1/uam/uam_device/get_all_devices",
    }),

    dismantleDevices: builder.mutation({
      query: (data) => ({
        url: "/api/v1/uam/uam_device/dismantle_onboard_device",
        method: "POST",
        body: data,
      }),
    }),

    // device detail modal apis
    fetchSitesByIPAddress: builder.query({
      query: (params) => ({
        url: `/api/v1/uam/uam_device/get_site_detail_by_ip_address`,
        params: { ip_address: params.ip_address },
      }),
    }),

    fetchRacksByIPAddress: builder.query({
      query: (params) => ({
        url: `/api/v1/uam/uam_device/get_rack_detail_by_ip_address`,
        params: { ip_address: params.ip_address },
      }),
    }),

    fetchBoardsByIPAddress: builder.query({
      query: (params) => ({
        url: `/api/v1/uam/uam-module/get_board_details_by_ip_address`,
        params: { ip_address: params.ip_address },
      }),
    }),

    fetchSubBoardsByIPAddress: builder.query({
      query: (params) => ({
        url: `/api/v1/uam/uam-module/get_subboard_details_by_ip_address`,
        params: { ip_address: params.ip_address },
      }),
    }),

    fetchSFPsByIPAddress: builder.query({
      query: (params) => ({
        url: `/api/v1/uam/uam_sfp/get_sfps_details_by_ip_address`,
        params: { ip_address: params.ip_address },
      }),
    }),

    fetchLicensesByIPAddress: builder.query({
      query: (params) => ({
        url: `/api/v1/uam/uam_license/get_liscence_detail_by_ip_address`,
        params: { ip_address: params.ip_address },
      }),
    }),
  }),
});
export const {
  useFetchDevicesQuery: useFetchRecordsQuery,
  useDismantleDevicesMutation: useDismantleRecordsMutation,
  useFetchSitesByIPAddressQuery,
  useFetchRacksByIPAddressQuery,
  useFetchBoardsByIPAddressQuery,
  useFetchSubBoardsByIPAddressQuery,
  useFetchSFPsByIPAddressQuery,
  useFetchLicensesByIPAddressQuery,
} = extendedApi;
