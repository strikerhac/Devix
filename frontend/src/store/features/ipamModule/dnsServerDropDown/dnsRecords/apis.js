import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllIpamDnsRecords: builder.query({
      query: () => "/api/v1/ipam/ipam_device/get_dns_records",
    }),

    getIpamDnsRecordsByZoneId: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ipam/ipam_device/get_dns_record_by_zone_id",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const { useGetIpamDnsRecordsByZoneIdMutation } = extendedApi;

export const useFetchRecordsLazyQuery =
  extendedApi.endpoints.getAllIpamDnsRecords.useLazyQuery;
