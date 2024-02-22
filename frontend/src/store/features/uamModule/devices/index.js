import { extendedApi } from "./apis";
import { createSlice } from "@reduxjs/toolkit";
import { TABLE_DATA_UNIQUE_ID } from "../../../../containers/uamModule/devices/constants";

const initialState = {
  all_data: [],
  sites_by_ip_address: [],
  racks_by_ip_address: [],
  boards_by_ip_address: [],
  sub_boards_by_ip_address: [],
  sfps_by_ip_address: [],
  licenses_by_ip_address: [],
};

const deviceSlice = createSlice({
  name: "device",
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder
      .addMatcher(
        extendedApi.endpoints.fetchDevices.matchFulfilled,
        (state, action) => {
          state.all_data = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.dismantleDevices.matchFulfilled,
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
            }
          });
        }
      )
      .addMatcher(
        extendedApi.endpoints.fetchSitesByIPAddress.matchFulfilled,
        (state, action) => {
          state.sites_by_ip_address = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.fetchRacksByIPAddress.matchFulfilled,
        (state, action) => {
          state.racks_by_ip_address = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.fetchBoardsByIPAddress.matchFulfilled,
        (state, action) => {
          state.boards_by_ip_address = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.fetchSubBoardsByIPAddress.matchFulfilled,
        (state, action) => {
          state.sub_boards_by_ip_address = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.fetchSFPsByIPAddress.matchFulfilled,
        (state, action) => {
          state.sfps_by_ip_address = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.fetchLicensesByIPAddress.matchFulfilled,
        (state, action) => {
          state.licenses_by_ip_address = action.payload;
        }
      );
  },
});

export default deviceSlice.reducer;
