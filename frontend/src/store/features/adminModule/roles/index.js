import { extendedApi } from "./apis";
import { createSlice } from "@reduxjs/toolkit";
import {
  TABLE_DATA_UNIQUE_ID,
  ELEMENT_NAME,
  indexColumnNameConstants,
} from "../../../../containers/adminModule/roles/constants";

const initialState = {
  all_data: [],
  selected_role: null,
  selected_role_for_comparison: null,
};

const defaultSlice = createSlice({
  name: ELEMENT_NAME,
  initialState,
  reducers: {
    setSelectedRole: (state, action) => {
      state.selected_role = action.payload;
      state.selected_role_for_comparison = action.payload;
    },

    toggleModuleView: (state, action) => {
      state.selected_role[indexColumnNameConstants.CONFIGURATION][
        action.payload
      ].view =
        !state.selected_role[indexColumnNameConstants.CONFIGURATION][
          action.payload
        ].view;
    },

    togglePageView: (state, action) => {
      const moduleKey = action.payload.moduleKey;
      const pageKey = action.payload.pageKey;

      state.selected_role[indexColumnNameConstants.CONFIGURATION][
        moduleKey
      ].pages[pageKey].view =
        !state.selected_role[indexColumnNameConstants.CONFIGURATION][moduleKey]
          .pages[pageKey].view;
    },

    togglePageReadOnly: (state, action) => {
      const moduleKey = action.payload.moduleKey;
      const pageKey = action.payload.pageKey;

      state.selected_role[indexColumnNameConstants.CONFIGURATION][
        moduleKey
      ].pages[pageKey].read_only =
        !state.selected_role[indexColumnNameConstants.CONFIGURATION][moduleKey]
          .pages[pageKey].read_only;
    },
  },
  extraReducers(builder) {
    builder
      .addMatcher(
        extendedApi.endpoints.getAdminAllUserRoles.matchFulfilled,
        (state, action) => {
          state.all_data = action.payload;
          let data = action.payload.length > 0 ? action.payload[0] : null;
          if (data) {
            data[indexColumnNameConstants.CONFIGURATION] = JSON.parse(
              data[indexColumnNameConstants.CONFIGURATION]
            );
            state.selected_role = data;
            state.selected_role_for_comparison = data;
          }
        }
      )
      .addMatcher(
        extendedApi.endpoints.addAdminUserRole.matchFulfilled,
        (state, action) => {
          state.all_data = [action.payload.data, ...state.all_data];
          let data = action.payload.data || null;
          if (data) {
            data[indexColumnNameConstants.CONFIGURATION] = JSON.parse(
              data[indexColumnNameConstants.CONFIGURATION]
            );
            state.selected_role = data;
            state.selected_role_for_comparison = data;
          }
        }
      )
      .addMatcher(
        extendedApi.endpoints.updateAdminUserRole.matchFulfilled,
        (state, action) => {
          let objectToReplace = action.payload.data;
          state.all_data = state.all_data.map((item) => {
            if (
              item[TABLE_DATA_UNIQUE_ID] ===
              objectToReplace[TABLE_DATA_UNIQUE_ID]
            ) {
              return { ...item, ...objectToReplace };
            } else {
              return item;
            }
          });
        }
      )
      .addMatcher(
        extendedApi.endpoints.updateAdminUserRoleConfiguration.matchFulfilled,
        (state, action) => {
          let objectToReplace = action.payload.data;
          state.all_data = state.all_data.map((item) => {
            if (
              item[TABLE_DATA_UNIQUE_ID] ===
              objectToReplace[TABLE_DATA_UNIQUE_ID]
            ) {
              return { ...item, ...objectToReplace };
            } else {
              return item;
            }
          });

          let data = action.payload.data || null;
          if (data) {
            data[indexColumnNameConstants.CONFIGURATION] = JSON.parse(
              data[indexColumnNameConstants.CONFIGURATION]
            );
            state.selected_role = data;
            state.selected_role_for_comparison = data;
          }
        }
      )
      .addMatcher(
        extendedApi.endpoints.deleteAdminUserRoles.matchFulfilled,
        (state, action) => {
          const deletedIds = action.payload?.data || [];
          if (deletedIds.length > 0) {
            state.all_data = state.all_data.filter((item) => {
              const shouldKeepItem = deletedIds.some((deletedId) => {
                return deletedId === item[TABLE_DATA_UNIQUE_ID];
              });
              return !shouldKeepItem;
            });
          }

          let data = state.all_data.length > 0 ? state.all_data[0] : null;
          if (data) {
            data[indexColumnNameConstants.CONFIGURATION] =
              typeof data[indexColumnNameConstants.CONFIGURATION] === "string"
                ? JSON.parse(data[indexColumnNameConstants.CONFIGURATION])
                : data[indexColumnNameConstants.CONFIGURATION];
            state.selected_role = data;
            state.selected_role_for_comparison = data;
          } else {
            state.selected_role = null;
            state.selected_role_for_comparison = null;
          }
        }
      );
  },
});

export const {
  setSelectedRole,
  toggleModuleView,
  togglePageView,
  togglePageReadOnly,
} = defaultSlice.actions;
export default defaultSlice.reducer;
