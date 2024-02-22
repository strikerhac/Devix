import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllIpamDnsServers: builder.query({
      query: () => "/api/v1/ipam/ipam_device/get_dns_servers",
    }),

    deleteIpamDnsServers: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ipam/ipam_device/delete_dns_servers",
        method: "POST",
        body: data,
      }),
    }),

    addIpamDnsServer: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ipam/ipam_device/add_dns",
        method: "POST",
        body: data,
      }),
    }),

    updateIpamDnsServer: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ipam/ipam_device/edit_dns",
        method: "POST",
        body: data,
      }),
    }),

    scanIpamDnsServer: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ipam/ipam_device/scan_dns",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const {
  useGetAllIpamDnsServersQuery: useFetchRecordsQuery,
  useDeleteIpamDnsServersMutation: useDeleteRecordsMutation,
  useAddIpamDnsServerMutation: useAddRecordMutation,
  useUpdateIpamDnsServerMutation: useUpdateRecordMutation,
  useScanIpamDnsServerMutation,
} = extendedApi;
