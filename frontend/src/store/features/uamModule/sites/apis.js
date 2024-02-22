import { monetxApi } from "../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    //table apis
    fetchSites: builder.query({
      query: () => "/api/v1/uam/site/get_all_sites",
    }),

    deleteSites: builder.mutation({
      query: (data) => ({
        url: "/api/v1/uam/site/delete_sites",
        method: "POST",
        body: data,
      }),
    }),

    // form apis
    addSite: builder.mutation({
      query: (data) => ({
        url: "/api/v1/uam/site/add_site",
        method: "POST",
        body: data,
      }),
    }),

    updateSite: builder.mutation({
      query: (data) => ({
        url: "/api/v1/uam/site/edit_site",
        method: "POST",
        body: data,
      }),
    }),
  }),
});
export const {
  useFetchSitesQuery: useFetchRecordsQuery,
  useDeleteSitesMutation: useDeleteRecordsMutation,
  // form apis
  useAddSiteMutation: useAddRecordMutation,
  useUpdateSiteMutation: useUpdateRecordMutation,
} = extendedApi;
