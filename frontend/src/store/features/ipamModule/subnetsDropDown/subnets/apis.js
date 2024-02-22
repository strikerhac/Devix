import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllIpamSubnets: builder.query({
      query: () => "/api/v1/ipam/ipam_device/get_all_subnet",
    }),

    addIpamSubnets: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ipam/ipam_device/add_subnets",
        method: "POST",
        body: data,
      }),
    }),

    deleteIpamSubnets: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ipam/ipam_device/delete_subnets",
        method: "POST",
        body: data,
      }),
    }),

    addIpamSubnet: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ipam/ipam_device/add_subnet",
        method: "POST",
        body: data,
      }),
    }),

    updateIpamSubnet: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ipam/ipam_device/edit_subnet",
        method: "POST",
        body: data,
      }),
    }),

    scanAllIpamSubnets: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ipam/ipam_device/scan_all_subnets",
        method: "POST",
        body: data,
      }),
    }),

    scanIpamSubnet: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ipam/ipam_device/scan_subnet",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const {
  useGetAllIpamSubnetsQuery: useFetchRecordsQuery,
  useAddIpamSubnetsMutation: useAddRecordsMutation,
  useDeleteIpamSubnetsMutation: useDeleteRecordsMutation,
  useAddIpamSubnetMutation: useAddRecordMutation,
  useUpdateIpamSubnetMutation: useUpdateRecordMutation,
  useScanAllIpamSubnetsMutation,
  useScanIpamSubnetMutation,
} = extendedApi;
