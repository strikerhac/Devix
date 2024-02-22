import { API_ENDPOINT_URL } from "../../utils/constants";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const monetxApi = createApi({
  reducerPath: "monetxApi",
  keepUnusedDataFor: 0,
  baseQuery: fetchBaseQuery({ baseUrl: API_ENDPOINT_URL }),
  endpoints: (build) => ({}),
});
