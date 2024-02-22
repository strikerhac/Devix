import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import Grid from "@mui/material/Grid";
import { useUpdateRecordMutation } from "../../../store/features/uamModule/hwLifeCycles/apis";
import { formSetter } from "../../../utils/helpers";
import useErrorHandling, { TYPE_SINGLE } from "../../../hooks/useErrorHandling";
import FormModal from "../../../components/dialogs";
import DefaultFormUnit, { DateFormUnit } from "../../../components/formUnits";
import {
  AddSubmitDialogFooter,
  UpdateSubmitDialogFooter,
} from "../../../components/dialogFooters";
import DefaultSpinner from "../../../components/spinners";
import {
  indexColumnNameConstants,
  TABLE_DATA_UNIQUE_ID,
  ELEMENT_NAME,
} from "./constants";
import { defaultSchema as schema } from "./schemas";

const Index = ({ handleClose, open, recordToEdit }) => {
  // useForm hook
  const { handleSubmit, control, setValue } = useForm({
    resolver: yupResolver(schema),
  });

  // effects
  useEffect(() => {
    formSetter(recordToEdit, setValue, {
      dates: [
        indexColumnNameConstants.HW_EOS_DATE,
        indexColumnNameConstants.HW_EOL_DATE,
        indexColumnNameConstants.SW_EOS_DATE,
        indexColumnNameConstants.SW_EOL_DATE,
        indexColumnNameConstants.MANUFACTURE_DATE,
      ],
    });
  }, []);

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

  useErrorHandling({
    data: updateRecordData,
    isSuccess: isUpdateRecordSuccess,
    isError: isUpdateRecordError,
    error: updateRecordError,
    type: TYPE_SINGLE,
  });

  // on form submit
  const onSubmit = (data) => {
    if (recordToEdit) {
      data[TABLE_DATA_UNIQUE_ID] = recordToEdit[TABLE_DATA_UNIQUE_ID];
      updateRecord(data);
    }
  };

  return (
    <FormModal
      title={`${recordToEdit ? "Edit" : "Add"} ${ELEMENT_NAME}`}
      open={open}
    >
      <DefaultSpinner spinning={isUpdateRecordLoading}>
        <form onSubmit={handleSubmit(onSubmit)}>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <DefaultFormUnit
                control={control}
                dataKey={indexColumnNameConstants.PN_CODE}
                disabled={true}
                required
              />
              <DateFormUnit
                control={control}
                dataKey={indexColumnNameConstants.HW_EOS_DATE}
              />
              <DateFormUnit
                control={control}
                dataKey={indexColumnNameConstants.HW_EOL_DATE}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <DateFormUnit
                control={control}
                dataKey={indexColumnNameConstants.SW_EOS_DATE}
              />
              <DateFormUnit
                control={control}
                dataKey={indexColumnNameConstants.SW_EOL_DATE}
              />
              <DateFormUnit
                control={control}
                dataKey={indexColumnNameConstants.MANUFACTURE_DATE}
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
