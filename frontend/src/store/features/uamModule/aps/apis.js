import { monetxApi } from "../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    //table apis
    fetchAps: builder.query({
      query: () => "/api/v1/uam/uam_aps/get_all_aps",
    }),
  }),
});
export const { useFetchApsQuery: useFetchRecordsQuery } = extendedApi;
