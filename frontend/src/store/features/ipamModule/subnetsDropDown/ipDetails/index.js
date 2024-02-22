import { extendedApi } from "./apis";
import { createSlice } from "@reduxjs/toolkit";
import { ELEMENT_NAME } from "../../../../../containers/ipamModule/subnetsDropDown/ipDetails/constants";
import { persistReducer } from "redux-persist";
import persistConfig from "./persistConfig";

const initialState = {
  all_data: [],
  selected_ip_detail: null,
};

const defaultSlice = createSlice({
  name: ELEMENT_NAME,
  initialState,
  reducers: {
    setSelectedIpDetail: (state, action) => {
      state.selected_ip_detail = action.payload;
    },
  },
  extraReducers(builder) {
    builder
      .addMatcher(
        extendedApi.endpoints.getAllIpamIPDetails.matchFulfilled,
        (state, action) => {
          state.all_data = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.getIpDetailsBySubnetAddress.matchFulfilled,
        (state, action) => {
          state.all_data = action.payload;
        }
      );
  },
});

export const { setSelectedIpDetail } = defaultSlice.actions;

const persistedReducer = persistReducer(persistConfig, defaultSlice.reducer);
export default persistedReducer;
