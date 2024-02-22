import { monetxApi } from "../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getAllMonitoringDevices: builder.query({
      query: () => "/api/v1/monitoring/devices/get_all_monitoring_devices",
    }),

    startMonitoring: builder.query({
      query: () => "/api/v1/monitoring/monitoring_scheduler/run_active",
    }),

    getAtomsToAddInMonitoringDevices: builder.query({
      query: () => "/api/v1/monitoring/devices/get_atom_in_monitoring",
    }),

    addAtomsInMonitoringDevices: builder.mutation({
      query: (data) => ({
        url: "/api/v1/monitoring/devices/add_atom_in_monitoring",
        method: "POST",
        body: data,
      }),
    }),

    deleteMonitoringDevices: builder.mutation({
      query: (data) => ({
        url: "/api/v1/monitoring/devices/delete_monitoring_devices",
        method: "POST",
        body: data,
      }),
    }),

    updateMonitoringDevice: builder.mutation({
      query: (data) => ({
        url: "/api/v1/monitoring/devices/add_monitoring_device",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const {
  useGetAllMonitoringDevicesQuery: useFetchRecordsQuery,
  useUpdateMonitoringDeviceMutation: useUpdateRecordMutation,
  useDeleteMonitoringDevicesMutation: useDeleteRecordsMutation,
  useGetAtomsToAddInMonitoringDevicesQuery,
  useAddAtomsInMonitoringDevicesMutation,
} = extendedApi;

export const useStartMonitoringLazyQuery =
  extendedApi.endpoints.startMonitoring.useLazyQuery;
