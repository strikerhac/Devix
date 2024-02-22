import { monetxApi } from "../../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    //table apis
    fetchBoards: builder.query({
      query: () => "/api/v1/uam/uam-module/get_all_boards",
    }),
  }),
});
export const { useFetchBoardsQuery: useFetchRecordsQuery } = extendedApi;
