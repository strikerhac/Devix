import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    sendNcmRemoteCommandByNcmDeviceId: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ncm/ncm_device/send_command",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const { useSendNcmRemoteCommandByNcmDeviceIdMutation } = extendedApi;
