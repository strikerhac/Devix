import { monetxApi } from "../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    //table apis
    fetchSubBoards: builder.query({
      query: () => "/api/v1/uam/uam-module/get_all_sub_boards",
    }),
  }),
});
export const { useFetchSubBoardsQuery: useFetchRecordsQuery } = extendedApi;
