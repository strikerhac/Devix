import { monetxApi } from "../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    //table apis
    fetchHwLifeCycle: builder.query({
      query: () => "/api/v1/uam/uam_sntc/get_all_sntc",
    }),

    addHwLifeCycles: builder.mutation({
      query: (data) => ({
        url: "/api/v1/uam/uam_sntc/add_sntc",
        method: "POST",
        body: data,
      }),
      keepUnusedDataFor: 0,
    }),

    syncFromInventory: builder.query({
      query: () => "/api/v1/uam/uam_sntc/sync_from_inventory",
    }),

    syncToInventory: builder.query({
      query: () => "/api/v1/uam/uam_sntc/sync_to_inventory",
    }),

    deleteHwLifeCycle: builder.mutation({
      query: (data) => ({
        url: "/api/v1/uam/uam_sntc/delete_pn_code",
        method: "POST",
        body: data,
      }),
    }),

    updateHwLifeCycle: builder.mutation({
      query: (data) => ({
        url: "/api/v1/uam/uam_sntc/edit_sntc",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const {
  useFetchHwLifeCycleQuery: useFetchRecordsQuery,
  useAddHwLifeCyclesMutation: useAddRecordsMutation,
  useDeleteHwLifeCycleMutation: useDeleteRecordsMutation,
  useUpdateHwLifeCycleMutation: useUpdateRecordMutation,
} = extendedApi;

export const useSyncFromInventoryLazyQuery =
  extendedApi.endpoints.syncFromInventory.useLazyQuery;

export const useSyncToInventoryLazyQuery =
  extendedApi.endpoints.syncToInventory.useLazyQuery;
