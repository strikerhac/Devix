export const selectTableData = (state) =>
  state.ncm_manage_configurations?.all_data;
export const selectAtomsToAddInNcmDevicesData = (state) =>
  state.ncm_manage_configurations?.atoms_to_add_in_ncm_devices;
export const selectSelectedDevice = (state) =>
  state.ncm_manage_configurations?.selected_device;
export const selectSeverity = (state) =>
  state.ncm_manage_configurations?.severity_data;
export const selectDeviceType = (state) =>
  state.ncm_manage_configurations?.device_type_data;
