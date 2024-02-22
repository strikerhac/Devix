import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import Grid from "@mui/material/Grid";
import { useSelector } from "react-redux";
import { selectProductionStatusNames } from "../../../store/features/dropDowns/selectors";
import {
  useUpdateRecordMutation,
  useAddRecordMutation,
} from "../../../store/features/uamModule/sites/apis";
import {
  useFetchSiteNamesQuery,
  useFetchProductionStatusNamesQuery,
} from "../../../store/features/dropDowns/apis";
import { formSetter, getTitle } from "../../../utils/helpers";
import { ALPHA_NUMERIC_REGEX } from "../../../utils/constants/regex";
import useErrorHandling, { TYPE_FETCH } from "../../../hooks/useErrorHandling";
import { TYPE_SINGLE } from "../../../hooks/useErrorHandling";
import FormModal from "../../../components/dialogs";
import DefaultFormUnit from "../../../components/formUnits";
import { SelectFormUnit } from "../../../components/formUnits";
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
  const { refetch: refetchSiteNames } = useFetchSiteNamesQuery(undefined, {
    skip: !isAddRecordSuccess && !isUpdateRecordSuccess,
  });

  const {
    data: fetchProductionStatusNamesData,
    isSuccess: isFetchProductionStatusNamesSuccess,
    isLoading: isFetchProductionStatusNamesLoading,
    isError: isFetchProductionStatusNamesError,
    error: fetchProductionStatusNamesError,
  } = useFetchProductionStatusNamesQuery();

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
    data: fetchProductionStatusNamesData,
    isSuccess: isFetchProductionStatusNamesSuccess,
    isError: isFetchProductionStatusNamesError,
    error: fetchProductionStatusNamesError,
    type: TYPE_FETCH,
  });

  // getting dropdowns data from the store
  const productionStatusNames = useSelector(selectProductionStatusNames);

  // effects
  useEffect(() => {
    if (isAddRecordSuccess || isUpdateRecordSuccess) {
      refetchSiteNames();
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
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <DefaultFormUnit
                control={control}
                dataKey={indexColumnNameConstants.SITE_NAME}
                disabled={recordToEdit !== null}
                required
              />
              <DefaultFormUnit
                control={control}
                dataKey={indexColumnNameConstants.REGION_NAME}
              />
              <DefaultFormUnit
                control={control}
                dataKey={indexColumnNameConstants.CITY}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <SelectFormUnit
                control={control}
                dataKey={indexColumnNameConstants.STATUS}
                options={productionStatusNames ? productionStatusNames : []}
                spinning={isFetchProductionStatusNamesLoading}
                required
              />
              <DefaultFormUnit
                control={control}
                dataKey={indexColumnNameConstants.LATITUDE}
              />
              <DefaultFormUnit
                control={control}
                dataKey={indexColumnNameConstants.LONGITUDE}
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
