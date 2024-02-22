export const selectTableData = (state) => state.ipam_devices?.all_data;
export const selectAtomsToAddInIpamDevicesData = (state) =>
  state.ipam_devices?.atoms_to_add_in_ipam_devices;
export const selectIpamDevicesFetchDates = (state) =>
  state.ipam_devices?.ipam_devices_fetch_dates;
