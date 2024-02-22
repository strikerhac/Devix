import { extendedApi } from "./apis";
import { createSlice } from "@reduxjs/toolkit";
import { ELEMENT_NAME } from "../../../../../containers/ipamModule/dnsServerDropDown/dnsZones/constants";
import { persistReducer } from "redux-persist";
import persistConfig from "./persistConfig";

const initialState = {
  all_data: [],
  selected_dns_zone: null,
};

const defaultSlice = createSlice({
  name: ELEMENT_NAME,
  initialState,
  reducers: {
    setSelectedDnsZone: (state, action) => {
      state.selected_dns_zone = action.payload;
    },
  },
  extraReducers(builder) {
    builder
      .addMatcher(
        extendedApi.endpoints.getAllIpamDnsZones.matchFulfilled,
        (state, action) => {
          state.all_data = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.getIpamDnsZonesByServerId.matchFulfilled,
        (state, action) => {
          state.all_data = action.payload;
        }
      );
  },
});

export const { setSelectedDnsZone } = defaultSlice.actions;

const persistedReducer = persistReducer(persistConfig, defaultSlice.reducer);
export default persistedReducer;
