import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllInterfacesByIpAddress: builder.mutation({
      query: (data) => ({
        url: "/api/v1/monitoring/monitoring_network/get_interfaces_by_ip_address",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const {
  useGetAllInterfacesByIpAddressMutation: useFetchRecordsMutation,
} = extendedApi;
