import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import * as yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";
import Grid from "@mui/material/Grid";
import { useSelector } from "react-redux";
import {
  useFetchAccountTypeNamesQuery,
  useFetchActiveStatusNamesQuery,
  useFetchUserRoleNamesQuery,
} from "../../../store/features/dropDowns/apis";
import {
  selectAccountTypeNames,
  selectActiveStatusNames,
  selectUserRoleNames,
} from "../../../store/features/dropDowns/selectors";
import {
  useUpdateRecordMutation,
  useAddRecordMutation,
} from "../../../store/features/adminModule/members/apis";
import { formSetter, getTitle } from "../../../utils/helpers";
import { useAuthorization } from "../../../hooks/useAuth";
import useErrorHandling, {
  TYPE_FETCH,
  TYPE_SINGLE,
} from "../../../hooks/useErrorHandling";
import FormModal from "../../../components/dialogs";
import DefaultFormUnit, { SelectFormUnit } from "../../../components/formUnits";
import {
  AddSubmitDialogFooter,
  UpdateSubmitDialogFooter,
} from "../../../components/dialogFooters";
import DefaultSpinner from "../../../components/spinners";
import {
  ELEMENT_NAME,
  TABLE_DATA_UNIQUE_ID,
  indexColumnNameConstants,
} from "./constants";
import { defaultSchema as baseSchema } from "./schemas";

const Index = ({ handleClose, open, recordToEdit }) => {
  // schema
  const schema = recordToEdit
    ? baseSchema
    : baseSchema.concat(
        yup.object().shape({
          [indexColumnNameConstants.PASSWORD]: yup
            .string()
            .required(
              `${getTitle(indexColumnNameConstants.PASSWORD)} is required`
            ),
        })
      );

  // hooks
  const { getUserInfoFromAccessToken } = useAuthorization();

  // user information
  const userInfo = getUserInfoFromAccessToken();

  // useForm hook
  const { handleSubmit, control, setValue } = useForm({
    resolver: yupResolver(schema),
  });

  // effects
  useEffect(() => {
    formSetter(recordToEdit, setValue);
  }, []);

  // post api for the form
  const [
    addRecord,
    {
      data: addRecordData,
      isSuccess: isAddRecordSuccess,
      isLoading: isAddRecordLoading,
      isError: isAddRecordError,
      error: addRecordError,
    },
  ] = useAddRecordMutation();

  const [
    updateRecord,
    {
      data: updateRecordData,
      isSuccess: isUpdateRecordSuccess,
      isLoading: isUpdateRecordLoading,
      isError: isUpdateRecordError,
      error: updateRecordError,
    },
  ] = useUpdateRecordMutation();

  // fetching dropdowns data from backend using apis
  const {
    data: fetchAccountTypeNamesData,
    isSuccess: isFetchAccountTypeNamesSuccess,
    isLoading: isFetchAccountTypeNamesLoading,
    isError: isFetchAccountTypeNamesError,
    error: fetchAccountTypeNamesError,
  } = useFetchAccountTypeNamesQuery();

  const {
    data: fetchActiveStatusNamesData,
    isSuccess: isFetchActiveStatusNamesSuccess,
    isLoading: isFetchActiveStatusNamesLoading,
    isError: isFetchActiveStatusNamesError,
    error: fetchActiveStatusNamesError,
  } = useFetchActiveStatusNamesQuery();

  const {
    data: fetchUserRoleNamesData,
    isSuccess: isFetchUserRoleNamesSuccess,
    isLoading: isFetchUserRoleNamesLoading,
    isError: isFetchUserRoleNamesError,
    error: fetchUserRoleNamesError,
  } = useFetchUserRoleNamesQuery();

  // error handling custom hooks
  useErrorHandling({
    data: addRecordData,
    isSuccess: isAddRecordSuccess,
    isError: isAddRecordError,
    error: addRecordError,
    type: TYPE_SINGLE,
    callback: handleClose,
  });

  useErrorHandling({
    data: updateRecordData,
    isSuccess: isUpdateRecordSuccess,
    isError: isUpdateRecordError,
    error: updateRecordError,
    type: TYPE_SINGLE,
    callback: handleClose,
  });

  useErrorHandling({
    data: fetchAccountTypeNamesData,
    isSuccess: isFetchAccountTypeNamesSuccess,
    isError: isFetchAccountTypeNamesError,
    error: fetchAccountTypeNamesError,
    type: TYPE_FETCH,
  });

  useErrorHandling({
    data: fetchActiveStatusNamesData,
    isSuccess: isFetchActiveStatusNamesSuccess,
    isError: isFetchActiveStatusNamesError,
    error: fetchActiveStatusNamesError,
    type: TYPE_FETCH,
  });

  useErrorHandling({
    data: fetchUserRoleNamesData,
    isSuccess: isFetchUserRoleNamesSuccess,
    isError: isFetchUserRoleNamesError,
    error: fetchUserRoleNamesError,
    type: TYPE_FETCH,
  });

  // getting dropdowns data from the store
  const accountTypeNames = useSelector(selectAccountTypeNames);
  const activeStatusNames = useSelector(selectActiveStatusNames);
  const userRoleNames = useSelector(selectUserRoleNames);

  // on form submit
  const onSubmit = (data) => {
    if (recordToEdit) {
      data[TABLE_DATA_UNIQUE_ID] = recordToEdit[TABLE_DATA_UNIQUE_ID];
      updateRecord(data);
    } else {
      data[indexColumnNameConstants.END_USER_ID] =
        userInfo[indexColumnNameConstants.END_USER_ID];
      addRecord(data);
    }
  };

  return (
    <FormModal
      title={`${recordToEdit ? "Edit" : "Add"} ${ELEMENT_NAME}`}
      open={open}
    >
      <DefaultSpinner spinning={isAddRecordLoading || isUpdateRecordLoading}>
        <form onSubmit={handleSubmit(onSubmit)}>
          <Grid container spacing={5}>
            <Grid item xs={6}>
              <DefaultFormUnit
                control={control}
                dataKey={indexColumnNameConstants.USER_NAME}
                required
              />
              <DefaultFormUnit
                type="email"
                control={control}
                dataKey={indexColumnNameConstants.EMAIL}
                required
              />
              {recordToEdit ? null : (
                <DefaultFormUnit
                  type="password"
                  control={control}
                  dataKey={indexColumnNameConstants.PASSWORD}
                  required
                />
              )}
              <DefaultFormUnit
                control={control}
                dataKey={indexColumnNameConstants.NAME}
                required
              />
            </Grid>
            <Grid item xs={6}>
              <SelectFormUnit
                control={control}
                dataKey={indexColumnNameConstants.STATUS}
                options={activeStatusNames}
                spinning={isFetchActiveStatusNamesLoading}
                required
              />
              <SelectFormUnit
                control={control}
                dataKey={indexColumnNameConstants.ROLE}
                options={userRoleNames}
                spinning={isFetchUserRoleNamesLoading}
                required
              />
              <SelectFormUnit
                control={control}
                dataKey={indexColumnNameConstants.ACCOUNT_TYPE}
                options={accountTypeNames}
                spinning={isFetchAccountTypeNamesLoading}
                required
              />
              <DefaultFormUnit
                control={control}
                dataKey={indexColumnNameConstants.TEAM}
              />
            </Grid>
            <Grid item xs={12}>
              {recordToEdit ? (
                <UpdateSubmitDialogFooter handleCancel={handleClose} />
              ) : (
                <AddSubmitDialogFooter handleCancel={handleClose} />
              )}
            </Grid>
          </Grid>
        </form>
      </DefaultSpinner>
    </FormModal>
  );
};

export default Index;
