export const selectConfigurationChangeByDevice = (state) =>
  state.ncm_dashboard?.configuration_change_by_device_data;
export const selectConfigurationBackupSummary = (state) =>
  state.ncm_dashboard?.configuration_backup_summary_data;
export const selectRecentRcmAlarms = (state) =>
  state.ncm_dashboard?.recent_rcm_alarms_data;
export const selectRecentRcmAlarmsCount = (state) =>
  state.ncm_dashboard?.recent_rcm_alarms_count_data;
export const selectNcmDeviceSummaryTable = (state) =>
  state.ncm_dashboard?.ncm_device_summary_data;
export const selectNcmChangeByVendor = (state) =>
  state.ncm_dashboard?.ncm_change_by_vendor_data;
