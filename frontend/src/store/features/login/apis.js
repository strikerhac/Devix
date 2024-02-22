import { monetxApi } from "../apiSlice";

export const extendedApi = monetxApi.injectEndpoints({
  endpoints: (builder) => ({
    login: builder.mutation({
      query: (data) => ({
        url: "/api/v1/users/auth/sign_in",
        method: "POST",
        body: data,
      }),
    }),
    register: builder.mutation({
      query: (data) => ({
        url: "/api/v1/users/auth/sign_up",
        method: "POST",
        body: data,
      }),
    }),
    validateToken: builder.mutation({
      query: (data) => ({
        url: "/api/v1/users/auth/validate_sign_in_token",
        method: "POST",
        body: data,
      }),
    }),
    checkIsAnyCompanyRegistered: builder.query({
      query: () => "/api/v1/users/user/check_end_user_existence",
    }),
    forgotPassword: builder.mutation({
      query: (data) => ({
        url: "/api/v1/users/user/forgot_password",
        method: "POST",
        body: data,
      }),
    }),
    verifyOtpAndUpdateUserPassword: builder.mutation({
      query: (data) => ({
        url: "/api/v1/users/user/verify_otp_and_update_user_password",
        method: "POST",
        body: data,
      }),
    }),
  }),
});

export const {
  useLoginMutation,
  useRegisterMutation,
  useValidateTokenMutation,
  useCheckIsAnyCompanyRegisteredQuery,
  useForgotPasswordMutation,
  useVerifyOtpAndUpdateUserPasswordMutation,
} = extendedApi;
