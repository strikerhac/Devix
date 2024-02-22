import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import Grid from "@mui/material/Grid";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import { useSelector } from "react-redux";
import { selectPasswordGroupTypeNames } from "../../../store/features/dropDowns/selectors";
import {
  useFetchPasswordGroupNamesQuery,
  useFetchPasswordGroupTypeNamesQuery,
} from "../../../store/features/dropDowns/apis";
import {
  useUpdateRecordMutation,
  useAddRecordMutation,
} from "../../../store/features/atomModule/passwordGroups/apis";
import { formSetter, getTitle } from "../../../utils/helpers";
import useErrorHandling, {
  TYPE_FETCH,
  TYPE_SINGLE,
} from "../../../hooks/useErrorHandling";
import FormModal from "../../../components/dialogs";
import DefaultFormUnit from "../../../components/formUnits";
import { SelectFormUnit } from "../../../components/formUnits";
import {
  AddSubmitDialogFooter,
  UpdateSubmitDialogFooter,
} from "../../../components/dialogFooters";
import DefaultSpinner from "../../../components/spinners";
import { ELEMENT_NAME, TELNET } from "./constants";
import { indexColumnNameConstants, TABLE_DATA_UNIQUE_ID } from "./constants";
import { defaultSchema as schema } from "./schemas";

const Index = ({ handleClose, open, recordToEdit }) => {
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
  const { refetch: refetchPasswordGroupNames } =
    useFetchPasswordGroupNamesQuery(undefined, {
      skip: !isAddRecordSuccess && !isUpdateRecordSuccess,
    });

  const {
    data: passwordGroupTypeNamesData,
    isSuccess: isPasswordGroupTypeNamesSuccess,
    isLoading: isPasswordGroupTypeNamesLoading,
    isError: isPasswordGroupTypeNamesError,
    error: passwordGroupTypeNamesError,
  } = useFetchPasswordGroupTypeNamesQuery();

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
    data: passwordGroupTypeNamesData,
    isSuccess: isPasswordGroupTypeNamesSuccess,
    isError: isPasswordGroupTypeNamesError,
    error: passwordGroupTypeNamesError,
    type: TYPE_FETCH,
  });

  // getting dropdowns data from the store
  const passwordGroupTypeNames = useSelector(selectPasswordGroupTypeNames);

  // effects
  useEffect(() => {
    if (isAddRecordSuccess || isUpdateRecordSuccess) {
      refetchPasswordGroupNames();
    }
  }, [isAddRecordSuccess, isUpdateRecordSuccess]);

  // on form submit
  const onSubmit = (data) => {
    if (recordToEdit) {
      data[TABLE_DATA_UNIQUE_ID] = recordToEdit[TABLE_DATA_UNIQUE_ID];
      updateRecord(data);
    } else {
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
            <Grid item xs={12}>
              <DefaultFormUnit
                control={control}
                dataKey={indexColumnNameConstants.PASSWORD_GROUP}
                disabled={recordToEdit !== null}
                required
              />
              <DefaultFormUnit
                control={control}
                dataKey={indexColumnNameConstants.USER_NAME}
                required
              />
              <SelectFormUnit
                control={control}
                dataKey={indexColumnNameConstants.PASSWORD_GROUP_TYPE}
                options={passwordGroupTypeNames ? passwordGroupTypeNames : []}
                spinning={isPasswordGroupTypeNamesLoading}
                required
              />
              <DefaultFormUnit
                type="password"
                control={control}
                dataKey={indexColumnNameConstants.PASSWORD}
                required
              />
              <DefaultFormUnit
                type="password"
                control={control}
                dataKey={indexColumnNameConstants.SECRET_PASSWORD}
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
