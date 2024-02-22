import { extendedApi } from "./apis";
import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  all_data: [],
  alert_history_details: [],
};

const alertSlice = createSlice({
  name: "alert",
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder
      .addMatcher(
        extendedApi.endpoints.getAllAlerts.matchFulfilled,
        (state, action) => {
          state.all_data = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.getAlertsHistoryByIpAddress.matchFulfilled,
        (state, action) => {
          state.alert_history_details = action.payload;
        }
      );
  },
});

export default alertSlice.reducer;
