export const selectTypeSummary = (state) =>
  state.ipam_dashboard?.type_summary_data;
export const selectTopTenSubnet = (state) =>
  state.ipam_dashboard?.top_ten_subnet_data;
export const selectSubnetSummary = (state) =>
  state.ipam_dashboard?.subnet_summary_data;

export const selectIpAvailbility = (state) =>
  state.ipam_dashboard?.ip_availibility_data;
export const selectTopTenOpenPorts = (state) =>
  state.ipam_dashboard?.top_ten_open_ports_data;
export const selectDns = (state) => state.ipam_dashboard?.dns_data;
// export const selectConfigurationBackupSummary = (state) =>
// state.ncm_dashboard.configuration_backup_summary_data;
// export const selectRecentRcmAlarms = (state) =>
// state.ncm_dashboard.recent_rcm_alarms_data;
// export const selectRecentRcmAlarmsCount = (state) =>
// state.ncm_dashboard.recent_rcm_alarms_count_data;
// export const selectNcmDeviceSummaryTable = (state) =>
// state.ncm_dashboard.ncm_device_summary_data;
// export const selectNcmChangeByVendor = (state) =>
// state.ncm_dashboard.ncm_change_by_vendor_data;
