import { monetxApi } from "../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getHeatMap: builder.query({           
      query: () => "/api/v1/monitoring/dashboard/get_monitoring_heatmap",
    }),

    getMemory: builder.query({           
      query: () => "/api/v1/monitoring/dashboard/get_memory_dashboard",
    }),
    getCpu: builder.query({           
      query: () => "/api/v1/monitoring/dashboard/get_cpu_dashboard",
    }),
    getTopInterfaces: builder.query({           
      query: () => "/api/v1/monitoring/dashboard/get_top_interfaces",
    }),
    getSnapshot: builder.query({           
      query: () => "/api/v1/monitoring/dashboard/get_snapshot",
    }),
    
    
  }),
});

export const {
  useGetHeatMapQuery, useGetMemoryQuery, useGetCpuQuery, useGetTopInterfacesQuery, useGetSnapshotQuery,
} = extendedApi;
