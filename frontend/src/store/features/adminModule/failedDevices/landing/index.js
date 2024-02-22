import { extendedApi } from "./apis";
import { createSlice } from "@reduxjs/toolkit";
import { ELEMENT_NAME } from "../../../../../containers/adminModule/failedDevicesLanding/ipam/constants";

const initialState = {
  failed_devices_counts: null,
};

const defaultSlice = createSlice({
  name: ELEMENT_NAME,
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder.addMatcher(
      extendedApi.endpoints.getFailedDevicesCounts.matchFulfilled,
      (state, action) => {
        state.failed_devices_counts = action.payload;
      }
    );
  },
});

export default defaultSlice.reducer;
