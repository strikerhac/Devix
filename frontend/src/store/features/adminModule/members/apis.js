import { monetxApi } from "../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllAdminMembers: builder.query({
      query: () => "/api/v1/users/user/get_all_users",
    }),

    deleteAdminMembers: builder.mutation({
      query: (data) => ({
        url: "/api/v1/users/user/delete_user",
        method: "POST",
        body: data,
      }),
    }),

    addAdminMember: builder.mutation({
      query: (data) => ({
        url: "/api/v1/users/user/add_user",
        method: "POST",
        body: data,
      }),
    }),

    updateAdminMember: builder.mutation({
      query: (data) => ({
        url: "/api/v1/users/user/edit_user",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const {
  useGetAllAdminMembersQuery: useFetchRecordsQuery,
  useDeleteAdminMembersMutation: useDeleteRecordsMutation,
  useAddAdminMemberMutation: useAddRecordMutation,
  useUpdateAdminMemberMutation: useUpdateRecordMutation,
} = extendedApi;
