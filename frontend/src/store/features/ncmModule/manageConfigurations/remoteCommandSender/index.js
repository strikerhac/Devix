import { extendedApi } from "./apis";
import { createSlice } from "@reduxjs/toolkit";
import {
  TABLE_DATA_UNIQUE_ID,
  ELEMENT_NAME,
} from "../../../../../containers/ncmModule/manageConfigurationsLanding/remoteCommandSender/constants";

const initialState = {
  command_output: null,
};

const defaultSlice = createSlice({
  name: ELEMENT_NAME,
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder.addMatcher(
      extendedApi.endpoints.sendNcmRemoteCommandByNcmDeviceId.matchFulfilled,
      (state, action) => {
        state.command_output = action.payload.data;
      }
    );
  },
});

export default defaultSlice.reducer;
