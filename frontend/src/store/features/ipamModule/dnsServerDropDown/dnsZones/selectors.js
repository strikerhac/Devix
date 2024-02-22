export const selectTableData = (state) => state.ipam_dns_zones?.all_data;
export const selectSelectedDnsZone = (state) =>
  state.ipam_dns_zones?.selected_dns_zone;
