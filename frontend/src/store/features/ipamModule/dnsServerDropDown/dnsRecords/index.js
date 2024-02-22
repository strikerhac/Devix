import { extendedApi } from "./apis";
import { createSlice } from "@reduxjs/toolkit";
import { ELEMENT_NAME } from "../../../../../containers/ipamModule/dnsServerDropDown/dnsRecords/constants";

const initialState = {
  all_data: [],
};

const defaultSlice = createSlice({
  name: ELEMENT_NAME,
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder
      .addMatcher(
        extendedApi.endpoints.getAllIpamDnsRecords.matchFulfilled,
        (state, action) => {
          state.all_data = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.getIpamDnsRecordsByZoneId.matchFulfilled,
        (state, action) => {
          state.all_data = action.payload;
        }
      );
  },
});

export default defaultSlice.reducer;
