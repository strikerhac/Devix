import { monetxApi } from "../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    //table apis
    fetchSfps: builder.query({
      query: () => "/api/v1/uam/uam_sfp/get_all_sfps",
    }),
  }),
});
export const { useFetchSfpsQuery: useFetchRecordsQuery } = extendedApi;
