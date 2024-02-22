import { extendedApi } from "./apis";
import { createSlice } from "@reduxjs/toolkit";
import {
  TABLE_DATA_UNIQUE_ID,
  ELEMENT_NAME,
} from "../../../../containers/monitoringModule/dashboard/constants";

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
        extendedApi.endpoints.getHeatMap.matchFulfilled,
        (state, action) => {
          state.heat_map_data = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.getMemory.matchFulfilled,
        (state, action) => {
          state.memory_data = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.getCpu.matchFulfilled,
        (state, action) => {
          state.cpu_data = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.getTopInterfaces.matchFulfilled,
        (state, action) => {
          state.top_interfaces_data = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.getSnapshot.matchFulfilled,
        (state, action) => {
          state.snapshot_data = action.payload;
        }
      );
  },
});

export default defaultSlice.reducer;
