import { monetxApi } from "../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    //table apis
    fetchAtomPasswordGroups: builder.query({
      query: () => "/api/v1/atom/password_group/get_password_groups",
    }),
    addAtomPasswordGroups: builder.mutation({
      query: (data) => ({
        url: "/api/v1/atom/password_group/add_password_groups",
        method: "POST",
        body: data,
      }),
    }),
    deleteAtomPasswordGroups: builder.mutation({
      query: (data) => ({
        url: "/api/v1/atom/password_group/delete_password_group",
        method: "POST",
        body: data,
      }),
    }),
    // form apis
    addAtomPasswordGroup: builder.mutation({
      query: (data) => ({
        url: "/api/v1/atom/password_group/add_password_group",
        method: "POST",
        body: data,
      }),
    }),
    updateAtomPasswordGroup: builder.mutation({
      query: (data) => ({
        url: "/api/v1/atom/password_group/edit_password_group",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const {
  useFetchAtomPasswordGroupsQuery: useFetchRecordsQuery,
  useAddAtomPasswordGroupsMutation: useAddRecordsMutation,
  useDeleteAtomPasswordGroupsMutation: useDeleteRecordsMutation,
  // form apis
  useAddAtomPasswordGroupMutation: useAddRecordMutation,
  useUpdateAtomPasswordGroupMutation: useUpdateRecordMutation,
} = extendedApi;
