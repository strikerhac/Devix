import { monetxApi } from "../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getConfigurationByTime: builder.query({           
      query: () => "/api/v1/main_dashboard/main_change-configuration-by-time",
    }),
    getDeviceStatusOverview: builder.query({           
        query: () => "/api/v1/main_dashboard/main_device_status",
      }),

      getUnusedSfps: builder.query({           
        query: () => "/api/v1/uam/uam_sfp/get_devices_most_unused_sfps",
      }),
      getEol: builder.query({           
        query: () => "/api/v1/uam/uam_sfp/get_EOL_Summary",
      }),
      

  }),
});

export const {
  useGetConfigurationByTimeQuery,useGetDeviceStatusOverviewQuery, useGetUnusedSfpsQuery,useGetEolQuery,
} = extendedApi;
