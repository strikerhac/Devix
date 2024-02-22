export const selectTableData = (state) => state.ipam_dns_servers?.all_data;
export const selectSelectedDnsServer = (state) =>
  state.ipam_dns_servers?.selected_dns_server;
