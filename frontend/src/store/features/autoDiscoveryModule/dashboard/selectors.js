export const selectSnmpStatus = (state) =>
  state.auto_discovery_dashboard?.snmp_status_data;
export const selectCredentialsSummary = (state) =>
  state.auto_discovery_dashboard?.credentials_summary_data;
export const selectTopVendorForDiscovery = (state) =>
  state.auto_discovery_dashboard?.top_vendor_for_discovery_data;
export const selectTopOs = (state) =>
  state.auto_discovery_dashboard?.top_os_data;
export const selectCountPerFunction = (state) =>
  state.auto_discovery_dashboard?.count_per_function_data;
