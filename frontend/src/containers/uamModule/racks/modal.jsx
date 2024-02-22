import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import FormModal from "../../../components/dialogs";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import Grid from "@mui/material/Grid";
import { useSelector } from "react-redux";
import { selectSiteNames } from "../../../store/features/dropDowns/selectors";
import { selectProductionStatusNames } from "../../../store/features/dropDowns/selectors";
import {
  useUpdateRecordMutation,
  useAddRecordMutation,
} from "../../../store/features/uamModule/racks/apis";
import {
  useFetchRackNamesQuery,
  useFetchSiteNamesQuery,
  useFetchProductionStatusNamesQuery,
} from "../../../store/features/dropDowns/apis";
import {
  formSetter,
  getTitle,
  transformDateTimeToDate,
} from "../../../utils/helpers";
import { ALPHA_NUMERIC_REGEX } from "../../../utils/constants/regex";
import useErrorHandling, {
  TYPE_FETCH,
  TYPE_SINGLE,
} from "../../../hooks/useErrorHandling";
import {
  SelectFormUnit,
  AddableSelectFormUnit,
  DateFormUnit,
} from "../../../components/formUnits";
import DefaultFormUnit from "../../../components/formUnits";
import {
  AddSubmitDialogFooter,
  UpdateSubmitDialogFooter,
} from "../../../components/dialogFooters";
import DefaultSpinner from "../../../components/spinners";
import { ELEMENT_NAME, TABLE_DATA_UNIQUE_ID } from "./constants";
import { indexColumnNameConstants } from "./constants";
import { defaultSchema as schema } from "./schemas";

const Index = ({
  handleClose,
  open,
  recordToEdit,
  handleOpenSiteModal,
  nested = false,
}) => {
  // useForm hook
  const { handleSubmit, control, setValue, watch } = useForm({
    resolver: yupResolver(schema),
  });

  // effects
  useEffect(() => {
    formSetter(recordToEdit, setValue, {
      dates: [
        indexColumnNameConstants.MANUFACTURE_DATE,
        indexColumnNameConstants.RFS_DATE,
      ],
    });
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
  const { refetch: refetchRackNames } = useFetchRackNamesQuery(
    {
      site_name: watch(indexColumnNameConstants.SITE_NAME, ""),
    },
    {
      skip: !isAddRecordSuccess && !isUpdateRecordSuccess,
    }
  );
  const {
    data: fetchSiteNamesData,
    isSuccess: isFetchSiteNamesSuccess,
    isLoading: isFetchSiteNamesLoading,
    isError: isFetchSiteNamesError,
    error: fetchSiteNamesError,
  } = useFetchSiteNamesQuery();

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
    data: fetchSiteNamesData,
    isSuccess: isFetchSiteNamesSuccess,
    isError: isFetchSiteNamesError,
    error: fetchSiteNamesError,
    type: TYPE_FETCH,
  });

  useErrorHandling({
    data: fetchProductionStatusNamesData,
    isSuccess: isFetchProductionStatusNamesSuccess,
    isError: isFetchProductionStatusNamesError,
    error: fetchProductionStatusNamesError,
    type: TYPE_FETCH,
  });

  // ///getting dropdowns data from the store
  const siteNames = useSelector(selectSiteNames);
  const productionStatusNames = useSelector(selectProductionStatusNames);

  // effects
  useEffect(() => {
    if (isAddRecordSuccess || isUpdateRecordSuccess) {
      refetchRackNames();
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
          <Grid container spacing={3}>
            <Grid item xs={12} sm={4}>
              <DefaultFormUnit
                control={control}
                dataKey={indexColumnNameConstants.RACK_NAME}
                disabled={recordToEdit !== null}
                required
              />
              <DefaultFormUnit
                control={control}
                dataKey={indexColumnNameConstants.SERIAL_NUMBER}
              />
              <DateFormUnit
                control={control}
                dataKey={indexColumnNameConstants.MANUFACTURE_DATE}
              />
              <DefaultFormUnit
                control={control}
                dataKey={indexColumnNameConstants.PN_CODE}
              />
              <DefaultFormUnit
                control={control}
                dataKey={indexColumnNameConstants.UNIT_POSITION}
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              {nested ? (
                <SelectFormUnit
                  control={control}
                  dataKey={indexColumnNameConstants.SITE_NAME}
                  options={siteNames ? siteNames : []}
                  required
                />
              ) : (
                <AddableSelectFormUnit
                  control={control}
                  dataKey={indexColumnNameConstants.SITE_NAME}
                  options={siteNames ? siteNames : []}
                  onAddClick={handleOpenSiteModal}
                  spinning={isFetchSiteNamesLoading}
                  required
                />
              )}
              <DefaultFormUnit
                type="number"
                control={control}
                dataKey={indexColumnNameConstants.HEIGHT}
              />
              <DefaultFormUnit
                type="number"
                control={control}
                dataKey={indexColumnNameConstants.WIDTH}
              />
              <DefaultFormUnit
                type="number"
                control={control}
                dataKey={indexColumnNameConstants.DEPTH}
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <SelectFormUnit
                control={control}
                dataKey={indexColumnNameConstants.STATUS}
                options={productionStatusNames ? productionStatusNames : []}
                spinning={isFetchProductionStatusNamesLoading}
                required
              />
              <DefaultFormUnit
                type="number"
                control={control}
                dataKey={indexColumnNameConstants.RU}
              />
              <DateFormUnit
                control={control}
                dataKey={indexColumnNameConstants.RFS_DATE}
              />
              <DefaultFormUnit
                control={control}
                dataKey={indexColumnNameConstants.RACK_MODEL}
              />
              <DefaultFormUnit
                type="number"
                control={control}
                dataKey={indexColumnNameConstants.FLOOR}
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
