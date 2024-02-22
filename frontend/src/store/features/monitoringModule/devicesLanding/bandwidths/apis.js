import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllBandwidthsByInterface: builder.mutation({
      query: (data) => ({
        url: "/api/v1/monitoring/devices/get_interface_band",
        method: "POST",
        body: data,
      }), // {ip_address:"",interface_name:"" }
    }),
  }),
});

export const {
  useGetAllBandwidthsByInterfaceMutation: useFetchRecordsMutation,
} = extendedApi;
