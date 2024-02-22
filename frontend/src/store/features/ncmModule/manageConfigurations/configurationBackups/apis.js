import { monetxApi } from "../../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllNcmConfigurationBackupsByNcmDeviceId: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ncm/ncm_device/get_all_device_configurations_by_id",
        method: "POST",
        body: data,
      }),
    }),

    deleteSingleNcmConfigurationBackupByNcmHistoryId: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ncm/ncm_device/delete_configuration",
        method: "POST",
        body: data,
      }),
    }),

    getNcmConfigurationBackupDetailsByNcmHistoryId: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ncm/ncm_device/get_device_configuration",
        method: "POST",
        body: data,
      }),
    }),

    getAllDeletedNcmConfigurationBackupsByNcmDeviceId: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ncm/ncm_device/get_configuration_to_restore",
        method: "POST",
        body: data,
      }),
    }),

    restoreNcmConfigurationBackupsByNcmHistoryIds: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ncm/ncm_device/restore_configuration",
        method: "POST",
        body: data,
      }),
    }),

    backupSingleNcmConfigurationByNcmDeviceId: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ncm/ncm_device/get_configuration_backup",
        method: "POST",
        body: data,
      }),
    }),

    compareNcmConfigurationBackups: builder.mutation({
      query: (data) => ({
        url: "/api/v1/ncm/ncm_device/configuration_comparison",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const {
  useGetAllNcmConfigurationBackupsByNcmDeviceIdMutation:
    useFetchRecordsMutation,
  useDeleteSingleNcmConfigurationBackupByNcmHistoryIdMutation:
    useDeleteRecordsMutation,
  useGetNcmConfigurationBackupDetailsByNcmHistoryIdMutation,
  useGetAllDeletedNcmConfigurationBackupsByNcmDeviceIdMutation,
  useRestoreNcmConfigurationBackupsByNcmHistoryIdsMutation,
  useBackupSingleNcmConfigurationByNcmDeviceIdMutation,
  useCompareNcmConfigurationBackupsMutation,
} = extendedApi;
