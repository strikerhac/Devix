import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllIpamIPDetails: builder.query({
      query: () => "/api/v1/ipam/ipam_device/get_all_ip_details",
    }),

    getIpDetailsBySubnetAddress: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ipam/ipam_device/get_ip_detail_by_subnet",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const { useGetIpDetailsBySubnetAddressMutation } = extendedApi;

export const useFetchRecordsLazyQuery =
  extendedApi.endpoints.getAllIpamIPDetails.useLazyQuery;
