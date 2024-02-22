export const selectConfigurationByTime = (state) =>
  state.dashboard_dashboard?.configuration_by_time_data;
export const selectDeviceStatusOverview = (state) =>
  state.dashboard_dashboard?.device_status_overview_data;
export const selectUnusedSfps = (state) =>
  state.dashboard_dashboard?.unused_sfps_data;
export const selectEol = (state) => state.dashboard_dashboard?.eol_data;
