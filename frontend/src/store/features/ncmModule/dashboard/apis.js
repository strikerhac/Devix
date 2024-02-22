import { monetxApi } from "../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({


    getConfigurationBackupSummary: builder.query({
      query: () => "/api/v1/ncm/ncm_dashboard/ncm_backup_summery_dashboard",
      
    }),
  
    getConfigurationChangeByDevice: builder.query({           
      query: () => "/api/v1/ncm/ncm_dashboard/ncm_change_summery_by_device",
    }),
    getRecentRcmAlarms: builder.query({           
      query: () => "/api/v1/ncm/ncm_dashboard/ncm_alarm_summery",
    }),
    getRecentRcmAlarmsCount: builder.query({           
      query: () => "/api/v1/ncm/ncm_dashboard/get_ncm_alarm_by_category_graph",
    }),
    getNcmDeviceSummaryTable: builder.query({           
      query: () => "/api/v1/ncm/ncm_dashboard/ncm_device_summary_by_fucntion",
    }),
    getNcmChangeByVendor: builder.query({           
      query: () => "/api/v1/ncm/ncm_dashboard/get_vendors_in_ncm",
    }),
    getConfigurationChangeByVendor: builder.query({           
      query: () => "/api/v1/ncm/ncm_dashboard/get_vendors_in_ncm",
    }),

    
  


  }),
});

export const {
  useGetConfigurationBackupSummaryQuery, useGetConfigurationChangeByDeviceQuery, useGetRecentRcmAlarmsQuery, useGetRecentRcmAlarmsCountQuery, useGetNcmDeviceSummaryTableQuery, useGetConfigurationChangeByVendorQuery, useGetNcmChangeByVendorQuery

} = extendedApi;
