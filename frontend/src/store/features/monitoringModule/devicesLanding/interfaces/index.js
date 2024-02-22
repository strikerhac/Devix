import { extendedApi } from "./apis";
import { createSlice } from "@reduxjs/toolkit";
import {
  TABLE_DATA_UNIQUE_ID,
  ELEMENT_NAME,
} from "../../../../../containers/monitoringModule/devicesLanding/interfaces/constants";
import { persistReducer } from "redux-persist";
import persistConfig from "./persistConfig";

const initialState = {
  all_data: [],
  selected_interface: null,
};

const defaultSlice = createSlice({
  name: ELEMENT_NAME,
  initialState,
  reducers: {
    setSelectedInterface: (state, action) => {
      state.selected_interface = action.payload;
    },
  },
  extraReducers(builder) {
    builder.addMatcher(
      extendedApi.endpoints.getAllInterfacesByIpAddress.matchFulfilled,
      (state, action) => {
        state.all_data = action.payload;
      }
    );
  },
});

export const { setSelectedInterface } = defaultSlice.actions;

const persistedReducer = persistReducer(persistConfig, defaultSlice.reducer);
export default persistedReducer;
