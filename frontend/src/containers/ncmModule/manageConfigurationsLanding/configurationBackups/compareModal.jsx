import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import ReactHtmlParser from "react-html-parser";
import Grid from "@mui/material/Grid";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import { useSelector } from "react-redux";
import { selectTableData } from "../../../../store/features/ncmModule/manageConfigurations/configurationBackups/selectors";
import { useCompareNcmConfigurationBackupsMutation } from "../../../../store/features/ncmModule/manageConfigurations/configurationBackups/apis";
import { getTitle } from "../../../../utils/helpers";
import useErrorHandling, {
  TYPE_SINGLE,
} from "../../../../hooks/useErrorHandling";
import FormModal from "../../../../components/dialogs";
import { SelectFormUnitWithHiddenValues } from "../../../../components/formUnits";
import { CompareDialogFooter } from "../../../../components/dialogFooters";
import DefaultSpinner from "../../../../components/spinners";
import { ELEMENT_NAME, compareModalConstants } from "./constants";

const schema = yup.object().shape({
  [compareModalConstants.CONFIGURATION_TO_BE_COMPARED]: yup
    .string()
    .required(
      `${getTitle(
        compareModalConstants.CONFIGURATION_TO_BE_COMPARED
      )} is required`
    ),
  [compareModalConstants.COMPARE_TO]: yup
    .string()
    .required(`${getTitle(compareModalConstants.COMPARE_TO)} is required`),
});

const Index = ({ handleClose, open }) => {
  // useForm hook
  const { handleSubmit, control } = useForm({
    resolver: yupResolver(schema),
  });

  // apis
  const [
    compareBackups,
    {
      data: compareBackupsData,
      isSuccess: isCompareBackupsSuccess,
      isLoading: isCompareBackupsLoading,
      isError: isCompareBackupsError,
      error: compareBackupsError,
    },
  ] = useCompareNcmConfigurationBackupsMutation();

  // error handling custom hooks
  useErrorHandling({
    data: compareBackupsData,
    isSuccess: isCompareBackupsSuccess,
    isError: isCompareBackupsError,
    error: compareBackupsError,
    type: TYPE_SINGLE,
  });

  // getting data from the store
  const dataSource = useSelector(selectTableData);
  const derivedOptions = dataSource?.map((item) => ({
    name: `${item.file_name}-${item.date}`,
    value: item.ncm_history_id,
  }));

  // on form submit
  const onSubmit = (data) => {
    compareBackups({
      ncm_history_id_1:
        data[compareModalConstants.CONFIGURATION_TO_BE_COMPARED],
      ncm_history_id_2: data[compareModalConstants.COMPARE_TO],
    });
  };

  useEffect(() => {
    // console.log("compareBackupsData", compareBackupsData);
  }, [compareBackupsData]);

  const sampleHTML = "<div><p>Hello, World!</p></div>";

  return (
    <FormModal title={`${"Compare"} ${ELEMENT_NAME}`} open={open}>
      <DefaultSpinner spinning={isCompareBackupsLoading}>
        <form onSubmit={handleSubmit(onSubmit)}>
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <SelectFormUnitWithHiddenValues
                control={control}
                dataKey={compareModalConstants.CONFIGURATION_TO_BE_COMPARED}
                options={derivedOptions ? derivedOptions : []}
                required
              />
            </Grid>
            <Grid item xs={6}>
              <SelectFormUnitWithHiddenValues
                control={control}
                dataKey={compareModalConstants.COMPARE_TO}
                options={derivedOptions ? derivedOptions : []}
                required
              />
            </Grid>
            <Grid item xs={12}>
              {compareBackupsData ? (
                <div
                  style={{
                    margin: "8px",
                    borderRadius: "12px",
                    backgroundColor: "#fcfcfc",
                    boxShadow: "rgba(0, 0, 0, 0.05) 0px 0px 0px 1px",
                  }}
                >
                  <div
                    style={{
                      width: "100%",
                      overflowX: "auto",
                      scrollBehavior: "smooth",
                    }}
                  >
                    <div
                      dangerouslySetInnerHTML={{
                        __html: compareBackupsData.data,
                      }}
                    />
                    {/* {ReactHtmlParser(compareBackupsData)} */}
                  </div>
                </div>
              ) : null}
            </Grid>
            <Grid item xs={12}>
              <CompareDialogFooter handleClose={handleClose} />
            </Grid>
          </Grid>
        </form>
      </DefaultSpinner>
    </FormModal>
  );
};

export default Index;
