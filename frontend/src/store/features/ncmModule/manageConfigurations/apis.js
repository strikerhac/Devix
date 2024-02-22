import { monetxApi } from "../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllNcmDevices: builder.query({
      query: () => "/api/v1/ncm/ncm_device/get_all_ncm_devices",
    }),

    getAtomsToAddInNcmDevices: builder.query({
      query: () => "/api/v1/ncm/ncm_device/get_atom_in_ncm",
      // Disable caching by providing a function that always returns a unique tag
      providesTags: (result, error, id) => [{ type: "Data", id: "unique-id" }],
    }),

    addAtomsInNcmDevices: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ncm/ncm_device/add_ncm_from_atom",
        method: "POST",
        body: data,
      }),
    }),

    deleteNcmDevices: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ncm/ncm_device/delete_ncm_devices",
        method: "POST",
        body: data,
      }),
    }),
    getSeverity: builder.query({
      query: () => "/api/v1/ncm/ncm_device/sort_by_severity",
    }),
    getDeviceType: builder.query({
      query: () => "/api/v1/ncm/ncm_device/device_type_counting",
    }),
    // call this api on loop when bulk backup starts, end the loop when this api returns empty array
    getAllCompletedBackups: builder.query({
      query: () => "/api/v1/ncm/ncm_device/get_all_true_backup",
    }),

    bulkBackupNcmConfigurationsByDeviceIds: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ncm/ncm_device/bulk_backup_configuration",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const {
  useGetAllNcmDevicesQuery: useFetchRecordsQuery,
  useGetAtomsToAddInNcmDevicesQuery,
  useAddAtomsInNcmDevicesMutation,
  useDeleteNcmDevicesMutation: useDeleteRecordsMutation,
  // useGetAllCompletedBackupsQuery,
  useBulkBackupNcmConfigurationsByDeviceIdsMutation,
  useGetSeverityQuery,
  useGetDeviceTypeQuery,
} = extendedApi;

export const useGetAllCompletedBackupsLazyQuery =
  extendedApi.endpoints.getAllCompletedBackups.useLazyQuery;
