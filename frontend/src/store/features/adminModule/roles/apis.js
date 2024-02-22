import { monetxApi } from "../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAdminAllUserRoles: builder.query({
      query: () => "/api/v1/users/user/get_all_user_roles",
    }),

    addAdminUserRole: builder.mutation({
      query: (data) => ({
        url: "/api/v1/users/user/add_user_role",
        method: "POST",
        body: data,
      }),
    }),

    updateAdminUserRole: builder.mutation({
      query: (data) => ({
        url: "/api/v1/users/user/edit_user_role",
        method: "POST",
        body: data,
      }),
    }),

    updateAdminUserRoleConfiguration: builder.mutation({
      query: (data) => ({
        url: "/api/v1/users/user/edit_role_configuration",
        method: "POST",
        body: data,
      }),
    }),

    deleteAdminUserRoles: builder.mutation({
      query: (data) => ({
        url: "/api/v1/users/user/delete_role",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const {
  useGetAdminAllUserRolesQuery: useFetchRecordsQuery,
  useAddAdminUserRoleMutation: useAddRecordMutation,
  useUpdateAdminUserRoleMutation: useUpdateRecordMutation,
  useUpdateAdminUserRoleConfigurationMutation,
  useDeleteAdminUserRolesMutation: useDeleteRecordsMutation,
} = extendedApi;
