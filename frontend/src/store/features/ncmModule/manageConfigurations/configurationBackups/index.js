import { extendedApi } from "./apis";
import { createSlice } from "@reduxjs/toolkit";
import {
  TABLE_DATA_UNIQUE_ID,
  ELEMENT_NAME,
} from "../../../../../containers/ncmModule/manageConfigurationsLanding/configurationBackups/constants";

const initialState = {
  all_data: [],
  configuration_backup_details: null,
  deleted_configuration_backups: [],
};

const defaultSlice = createSlice({
  name: ELEMENT_NAME,
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder
      .addMatcher(
        extendedApi.endpoints.getAllNcmConfigurationBackupsByNcmDeviceId
          .matchFulfilled,
        (state, action) => {
          state.all_data = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.deleteSingleNcmConfigurationBackupByNcmHistoryId
          .matchFulfilled,
        (state, action) => {
          const deletedIds = action.payload?.data || [];
          if (deletedIds.length > 0) {
            state.all_data = state.all_data.filter((item) => {
              const shouldKeepItem = deletedIds.some((deletedId) => {
                return deletedId === item[TABLE_DATA_UNIQUE_ID];
              });
              return !shouldKeepItem;
            });
            state.configuration_backup_details = null;
          }
        }
      )
      .addMatcher(
        extendedApi.endpoints.getNcmConfigurationBackupDetailsByNcmHistoryId
          .matchFulfilled,
        (state, action) => {
          state.configuration_backup_details = action.payload.data;
        }
      )
      .addMatcher(
        extendedApi.endpoints.getAllDeletedNcmConfigurationBackupsByNcmDeviceId
          .matchFulfilled,
        (state, action) => {
          state.deleted_configuration_backups = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.restoreNcmConfigurationBackupsByNcmHistoryIds
          .matchFulfilled,
        (state, action) => {
          action.payload.data.forEach((responseItem) => {
            const indexToUpdate = state.all_data.findIndex((tableItem) => {
              return (
                tableItem[TABLE_DATA_UNIQUE_ID] ===
                responseItem[TABLE_DATA_UNIQUE_ID]
              );
            });
            if (indexToUpdate !== -1) {
              state.all_data[indexToUpdate] = responseItem;
            } else {
              state.all_data = [responseItem, ...state.all_data];
            }
          });
        }
      )

      .addMatcher(
        extendedApi.endpoints.backupSingleNcmConfigurationByNcmDeviceId
          .matchFulfilled,
        (state, action) => {
          state.all_data = [action.payload.data, ...state.all_data];
        }
      );
  },
});

export default defaultSlice.reducer;
