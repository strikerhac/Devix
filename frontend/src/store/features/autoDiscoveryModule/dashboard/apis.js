import { monetxApi } from "../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    getSnmpStatus: builder.query({           
      query: () => "/api/v1/auto_discovery_dashboard/get_snmp_status_graph",
    }),


    
    getCredentialsSummary: builder.query({
      query: () => "/api/v1/auto_discovery_dashboard/get_credentials_graph",
      
    }),
    getTopVendorForDiscovery: builder.query({
        query: () => "/api/v1/auto_discovery_dashboard/get_top_vendors_for_discovery",
        
      }),
      getTopOs: builder.query({
        query: () => "/api/v1/auto_discovery_dashboard/get_top_os_for_discovery",
        
      }),
   
      getCountPerFunction: builder.query({
        query: () => "/api/v1/auto_discovery_dashboard/get_top_functions_for_discovery",
        
      }),

  }),
});

export const {
  useGetSnmpStatusQuery, useGetCredentialsSummaryQuery, useGetTopVendorForDiscoveryQuery, useGetTopOsQuery, useGetCountPerFunctionQuery
} = extendedApi;
