import { extendedApi } from "./apis";
import { createSlice } from "@reduxjs/toolkit";
import {
  TABLE_DATA_UNIQUE_ID,
  ELEMENT_NAME,
} from "../../../../containers/dashboardModule/dashboard/constants";
import {
  useGetCredentialsSummaryQuery,
  useGetSnmpStatusQuery,
  useGetTopVendorForDiscoveryQuery,
} from "../../dashboardModule/dashboard/apis";

import { useSelector } from "react-redux";

const initialState = {
  configuration_by_time_data: [],
};

const defaultSlice = createSlice({
  name: ELEMENT_NAME,
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder
      .addMatcher(
        extendedApi.endpoints.getConfigurationByTime.matchFulfilled,
        (state, action) => {
          state.configuration_by_time_data = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.getDeviceStatusOverview.matchFulfilled,
        (state, action) => {
          state.device_status_overview_data = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.getUnusedSfps.matchFulfilled,
        (state, action) => {
          state.unused_sfps_data = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.getEol.matchFulfilled,
        (state, action) => {
          state.eol_data = action.payload;
        }
      );
  },
});

export default defaultSlice.reducer;
