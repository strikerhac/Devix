export const selectTableData = (state) => state.monitoring_devices?.all_data;
export const selectAtomsToAddInMonitoringDevicesData = (state) =>
  state.monitoring_devices?.atoms_to_add_in_monitoring_devices;
export const selectSelectedDevice = (state) =>
  state.monitoring_devices?.selected_device;
