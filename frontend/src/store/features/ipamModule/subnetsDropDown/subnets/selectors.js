export const selectTableData = (state) => state.ipam_subnets?.all_data;
export const selectSelectedSubnet = (state) =>
  state.ipam_subnets?.selected_subnet;
