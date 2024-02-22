export const selectHeatMap = (state) =>
  state.dashboard_dashboard?.heat_map_data;
export const selectMemory = (state) => state.dashboard_dashboard?.memory_data;
export const selectCpu = (state) => state.dashboard_dashboard?.cpu_data;
export const selectTopInterfaces = (state) =>
  state.dashboard_dashboard?.top_interfaces_data;
export const selectSnapshot = (state) =>
  state.dashboard_dashboard?.snapshot_data;
