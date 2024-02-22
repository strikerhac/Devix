export const selectTableData = (state) => state.uam_devices?.all_data;
export const selectSitesByIPAddressData = (state) =>
  state.uam_devices?.sites_by_ip_address;
export const selectRacksByIPAddressData = (state) =>
  state.uam_devices?.racks_by_ip_address;
export const selectBoardsByIPAddressData = (state) =>
  state.uam_devices?.boards_by_ip_address;
export const selectSubBoardsByIPAddressData = (state) =>
  state.uam_devices?.sub_boards_by_ip_address;
export const selectSFPsByIPAddressData = (state) =>
  state.uam_devices?.sfps_by_ip_address;
export const selectLicensesByIPAddressData = (state) =>
  state.uam_devices?.licenses_by_ip_address;
