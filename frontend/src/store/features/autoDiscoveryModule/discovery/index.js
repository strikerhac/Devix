import { extendedApi } from "./apis";
import { createSlice } from "@reduxjs/toolkit";
import {
  TABLE_DATA_UNIQUE_ID,
  ELEMENT_NAME,
} from "../../../../containers/autoDiscoveryModule/discovery/constants";

const initialState = {
  all_data: [],
  device_counts: null,
};

const defaultSlice = createSlice({
  name: ELEMENT_NAME,
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder
      .addMatcher(
        extendedApi.endpoints.getAllAutoDiscoveryDiscoveredDevices
          .matchFulfilled,
        (state, action) => {
          state.all_data = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.getAutoDiscoveryDiscoveredDevicesBySubnet
          .matchFulfilled,
        (state, action) => {
          state.all_data = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.getAutoDiscoveryDiscoveryFunctionCountsBySubnet
          .matchFulfilled,
        (state, action) => {
          state.device_counts = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.autoDiscoveryAutoDiscoverDevicesBySubnet
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
      );
  },
});

export default defaultSlice.reducer;
