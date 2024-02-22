import React, { useEffect } from "react";
import Grid from "@mui/material/Grid";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import { useSelector } from "react-redux";
import { selectActiveStatusNames } from "../../../store/features/dropDowns/selectors";
import { useFetchActiveStatusNamesQuery } from "../../../store/features/dropDowns/apis";
import {
  useUpdateRecordMutation,
  useAddRecordMutation,
} from "../../../store/features/autoDiscoveryModule/manageNetworks/apis";
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
import { ELEMENT_NAME } from "./constants";
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
  const {
    data: fetchActiveStatusNamesData,
    isSuccess: isFetchActiveStatusNamesSuccess,
    isLoading: isFetchActiveStatusNamesLoading,
    isError: isFetchActiveStatusNamesError,
    error: fetchActiveStatusNamesError,
  } = useFetchActiveStatusNamesQuery();

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
    data: fetchActiveStatusNamesData,
    isSuccess: isFetchActiveStatusNamesSuccess,
    isError: isFetchActiveStatusNamesError,
    error: fetchActiveStatusNamesError,
    type: TYPE_FETCH,
  });

  // getting dropdowns data from the store
  const activeStatusNames = useSelector(selectActiveStatusNames);

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
                dataKey={indexColumnNameConstants.NETWORK_NAME}
                required
              />
              <DefaultFormUnit
                control={control}
                dataKey={indexColumnNameConstants.SUBNET}
                required
              />
              <SelectFormUnit
                control={control}
                dataKey={indexColumnNameConstants.SCAN_STATUS}
                options={activeStatusNames ? activeStatusNames : []}
                spinning={isFetchActiveStatusNamesLoading}
                required
              />
              <DefaultFormUnit
                control={control}
                dataKey={indexColumnNameConstants.EXCLUDED_IP_RANGE}
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
