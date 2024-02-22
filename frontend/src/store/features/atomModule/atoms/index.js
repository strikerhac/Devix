import { extendedApi } from "./apis";
import { createSlice, isAnyOf } from "@reduxjs/toolkit";
import { v4 as uuidv4 } from "uuid";
import {
  ATOM_ID,
  ATOM_TRANSITION_ID,
  TABLE_DATA_UNIQUE_ID,
  ELEMENT_NAME,
} from "../../../../containers/atomModule/atoms/constants";

const initialState = {
  all_data: [],
  atom_devices_from_discovery: [],
};

const defaultSlice = createSlice({
  name: ELEMENT_NAME,
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder
      .addMatcher(
        extendedApi.endpoints.fetchAtoms.matchFulfilled,
        (state, action) => {
          state.all_data = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.getAtomsDevicesFromDiscovery.matchFulfilled,
        (state, action) => {
          state.atom_devices_from_discovery = action.payload;
        }
      )
      .addMatcher(
        extendedApi.endpoints.addAtoms.matchFulfilled,
        (state, action) => {
          action.payload.data.forEach((responseItem) => {
            const indexToUpdate = state.all_data.findIndex((tableItem) => {
              let atomId = responseItem[ATOM_ID];
              let atomTransitionId = responseItem[ATOM_TRANSITION_ID];

              if (atomId) {
                return tableItem[ATOM_ID] === atomId;
              } else {
                return tableItem[ATOM_TRANSITION_ID] === atomTransitionId;
              }
            });

            // Generate a unique identifier using uuid
            const uniqueId = uuidv4();

            if (indexToUpdate !== -1) {
              responseItem[TABLE_DATA_UNIQUE_ID] = uniqueId;
              state.all_data[indexToUpdate] = responseItem;
            } else {
              responseItem[TABLE_DATA_UNIQUE_ID] = uniqueId;
              state.all_data = [responseItem, ...state.all_data];
            }
          });
        }
      )
      .addMatcher(
        extendedApi.endpoints.addAtomsDevicesFromDiscovery.matchFulfilled,
        (state, action) => {
          action.payload.data.forEach((responseItem) => {
            const indexToUpdate = state.all_data.findIndex((tableItem) => {
              let atomId = responseItem[ATOM_ID];
              let atomTransitionId = responseItem[ATOM_TRANSITION_ID];

              if (atomId) {
                return tableItem[ATOM_ID] === atomId;
              } else {
                return tableItem[ATOM_TRANSITION_ID] === atomTransitionId;
              }
            });

            // Generate a unique identifier using uuid
            const uniqueId = uuidv4();

            if (indexToUpdate !== -1) {
              responseItem[TABLE_DATA_UNIQUE_ID] = uniqueId;
              state.all_data[indexToUpdate] = responseItem;
            } else {
              responseItem[TABLE_DATA_UNIQUE_ID] = uniqueId;
              state.all_data = [responseItem, ...state.all_data];
            }
          });
        }
      )

      .addMatcher(
        extendedApi.endpoints.deleteAtoms.matchFulfilled,
        (state, action) => {
          const deletedIds = action.payload?.data || [];
          if (deletedIds.length > 0) {
            state.all_data = state.all_data.filter((item) => {
              const atomId = item[ATOM_ID];
              const transitionId = item[ATOM_TRANSITION_ID];
              const shouldKeepItem = deletedIds.some((id) => {
                if (atomId) {
                  return id[ATOM_ID] === atomId;
                } else {
                  return id[ATOM_TRANSITION_ID] === transitionId;
                }
              });
              return !shouldKeepItem;
            });
          }
        }
      )
      .addMatcher(
        extendedApi.endpoints.onBoardAtoms.matchFulfilled,
        (state, action) => {
          action.payload.data.forEach((responseItem) => {
            const indexToUpdate = state.all_data.findIndex((tableItem) => {
              let atomId = responseItem[ATOM_ID];

              if (atomId) {
                return tableItem[ATOM_ID] === atomId;
              } else return false;
            });

            if (indexToUpdate !== -1) {
              state.all_data[indexToUpdate] = {
                ...state.all_data[indexToUpdate],
                ...responseItem,
              };
            }
          });
        }
      )
      .addMatcher(
        extendedApi.endpoints.addAtom.matchFulfilled,
        (state, action) => {
          // Generate a unique identifier using uuid
          const uniqueId = uuidv4();

          action.payload.data[TABLE_DATA_UNIQUE_ID] = uniqueId;
          state.all_data = [action.payload.data, ...state.all_data];
        }
      )
      // .addMatcher(
      //   extendedApi.endpoints.updateAtom.matchFulfilled,
      //   (state, action) => {
      //     let objectToReplace = action.payload.data;
      //     state.all_data = state.all_data.map((item) => {
      //       const atomId = item[ATOM_ID];
      //       const transitionId = item[ATOM_TRANSITION_ID];
      //       if (atomId && atomId === objectToReplace[ATOM_ID]) {
      //         return { ...item, ...objectToReplace };
      //       } else if (
      //         transitionId &&
      //         transitionId === objectToReplace[ATOM_TRANSITION_ID]
      //       ) {
      //         return { ...item, ...objectToReplace };
      //       } else {
      //         return item;
      //       }
      //     });
      //   }
      // )
      .addMatcher(
        extendedApi.endpoints.updateAtom.matchFulfilled,
        (state, action) => {
          let storedAtomTransitionId = localStorage.getItem(ATOM_TRANSITION_ID);
          let objectToReplace = action.payload.data;
          if (storedAtomTransitionId && objectToReplace[ATOM_ID]) {
            const uniqueId = uuidv4();
            objectToReplace[TABLE_DATA_UNIQUE_ID] = uniqueId;
            state.all_data = [objectToReplace, ...state.all_data];
            state.all_data = state.all_data.filter((item) => {
              const transitionId = item[ATOM_TRANSITION_ID];
              if (transitionId && transitionId == storedAtomTransitionId) {
                return false;
              } else {
                return true;
              }
            });
            localStorage.removeItem(ATOM_TRANSITION_ID);
          } else {
            state.all_data = state.all_data.map((item) => {
              const atomId = item[ATOM_ID];
              const transitionId = item[ATOM_TRANSITION_ID];
              if (atomId && atomId === objectToReplace[ATOM_ID]) {
                return { ...item, ...objectToReplace };
              } else if (
                transitionId &&
                transitionId === objectToReplace[ATOM_TRANSITION_ID]
              ) {
                return { ...item, ...objectToReplace };
              } else {
                return item;
              }
            });
          }
        }
      );
  },
});

// export const { setNextPage, initiateItem } = atomSlice.actions;
export default defaultSlice.reducer;
