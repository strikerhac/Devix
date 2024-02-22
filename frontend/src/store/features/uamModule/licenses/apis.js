import { monetxApi } from "../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    //table apis
    fetchLicenses: builder.query({
      query: () => "/api/v1/uam/uam_license/get_all_licenses",
    }),
  }),
});
export const { useFetchLicensesQuery: useFetchRecordsQuery } = extendedApi;
