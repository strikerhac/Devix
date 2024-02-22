import { extendedApi } from "./apis";
import { createSlice } from "@reduxjs/toolkit";
import {
  TABLE_DATA_UNIQUE_ID,
  ELEMENT_NAME,
} from "../../../../containers/ncmModule/manageConfigurations/constants";
import { persistReducer } from "redux-persist";
import persistConfig from "./persistConfig";

const initialState = {
  all_data: [],
  atoms_to_add_in_ncm_devices: [],
  selected_device: null,
};

const defaultSlice = createSlice({
  name: ELEMENT_NAME,
  initialState,
  reducers: {
    setSelectedDevice: (state, action) => {
      state.selected_device = action.payload;
    },
  },
  extraReducers(builder) {
    builder
      .addMatcher(
        extendedApi.endpoints.getAllNcmDevices.matchFulfilled,
        (state, action) => {
          state.all_data = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.getSeverity.matchFulfilled,
        (state, action) => {
          state.severity_data = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.getDeviceType.matchFulfilled,
        (state, action) => {
          state.device_type_data = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.getAtomsToAddInNcmDevices.matchFulfilled,
        (state, action) => {
          state.atoms_to_add_in_ncm_devices = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.addAtomsInNcmDevices.matchFulfilled,
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
        extendedApi.endpoints.deleteNcmDevices.matchFulfilled,
        (state, action) => {
          const deletedIds = action.payload?.data || [];
          if (deletedIds.length > 0) {
            state.all_data = state.all_data.filter((item) => {
              const shouldKeepItem = deletedIds.some((deletedId) => {
                return deletedId === item[TABLE_DATA_UNIQUE_ID];
              });
              return !shouldKeepItem;
            });
          }
        }
      )
      .addMatcher(
        extendedApi.endpoints.getAllCompletedBackups.matchFulfilled,
        (state, action) => {
          const data = action.payload.data?.forEach((responseItem) => {
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
        extendedApi.endpoints.bulkBackupNcmConfigurationsByDeviceIds
          .matchFulfilled,
        (state, action) => {
          const data = action.payload.data?.forEach((responseItem) => {
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
      );
  },
});

export const { setSelectedDevice } = defaultSlice.actions;

const persistedReducer = persistReducer(persistConfig, defaultSlice.reducer);
export default persistedReducer;
