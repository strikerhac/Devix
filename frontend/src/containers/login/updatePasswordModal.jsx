import React from "react";
import { useForm } from "react-hook-form";
import Grid from "@mui/material/Grid";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import { useVerifyOtpAndUpdateUserPasswordMutation } from "../../store/features/login/apis";
import { getTitle } from "../../utils/helpers";
import useErrorHandling, { TYPE_SINGLE } from "../../hooks/useErrorHandling";
import DefaultFormUnit from "../../components/formUnits";
import { UpdateSubmitDialogFooter } from "../../components/dialogFooters";
import DefaultSpinner from "../../components/spinners";
import { indexColumnNameConstants, updatePasswordConstants } from "./constants";
import FormModal from "../../components/dialogs";

const schema = yup.object().shape({
  [updatePasswordConstants.OTP]: yup
    .string()
    .required(`${getTitle(updatePasswordConstants.OTP)} is required`),
  [updatePasswordConstants.NEW_PASSWORD]: yup
    .string()
    .required(`${getTitle(updatePasswordConstants.NEW_PASSWORD)} is required`),
});

const Index = ({ open, handleClose, userName }) => {
  // hooks
  const { handleSubmit, control } = useForm({
    resolver: yupResolver(schema),
  });

  // apis
  const [
    verifyOtpAndUpdateUserPassword,
    {
      data: verifyOtpAndUpdateUserPasswordData,
      isSuccess: isVerifyOtpAndUpdateUserPasswordSuccess,
      isLoading: isVerifyOtpAndUpdateUserPasswordLoading,
      isError: isVerifyOtpAndUpdateUserPasswordError,
      error: verifyOtpAndUpdateUserPasswordError,
    },
  ] = useVerifyOtpAndUpdateUserPasswordMutation();

  // error handling custom hooks
  useErrorHandling({
    data: verifyOtpAndUpdateUserPasswordData,
    isSuccess: isVerifyOtpAndUpdateUserPasswordSuccess,
    isError: isVerifyOtpAndUpdateUserPasswordError,
    error: verifyOtpAndUpdateUserPasswordError,
    type: TYPE_SINGLE,
  });

  // on form submit
  const onSubmit = (data) => {
    data[indexColumnNameConstants.USER_NAME] = userName;
    verifyOtpAndUpdateUserPassword(data);
  };

  return (
    <FormModal
      title={`Update ${indexColumnNameConstants.PASSWORD}`}
      open={open}
    >
      <DefaultSpinner spinning={isVerifyOtpAndUpdateUserPasswordLoading}>
        <form onSubmit={handleSubmit(onSubmit)}>
          <Grid container spacing={5}>
            <Grid item xs={12}>
              <DefaultFormUnit
                control={control}
                dataKey={updatePasswordConstants.OTP}
                required
              />
              <DefaultFormUnit
                control={control}
                dataKey={updatePasswordConstants.NEW_PASSWORD}
                required
              />
            </Grid>
            <Grid item xs={12}>
              <UpdateSubmitDialogFooter handleCancel={handleClose} />
            </Grid>
          </Grid>
        </form>
      </DefaultSpinner>
    </FormModal>
  );
};

export default Index;
