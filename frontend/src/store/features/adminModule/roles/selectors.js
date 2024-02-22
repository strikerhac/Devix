export const selectTableData = (state) => state.admin_roles?.all_data;
export const selectSelectedRole = (state) => state.admin_roles?.selected_role;
export const selectSelectedRoleForComparison = (state) =>
  state.admin_roles?.selected_role_for_comparison;
