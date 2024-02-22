export const selectTableData = (state) =>
  state.ncm_configuration_backups?.all_data;
export const selectConfigurationBackupDetails = (state) =>
  state.ncm_configuration_backups?.configuration_backup_details;
export const selectDeletedConfigurationBackups = (state) =>
  state.ncm_configuration_backups?.deleted_configuration_backups;
