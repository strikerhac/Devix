import React from "react";
import * as yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";
import { useForm } from "react-hook-form";
import { useSelector } from "react-redux";
import { selectSubnetNames } from "../../../store/features/dropDowns/selectors";
import { useFetchSubnetNamesQuery } from "../../../store/features/dropDowns/apis";
import { getTitle } from "../../../utils/helpers";
import useErrorHandling, { TYPE_FETCH } from "../../../hooks/useErrorHandling";
import useButtonGenerator from "../../../hooks/useButtonGenerator";
import useButtonsConfiguration from "../../../hooks/useButtonsConfiguration";
import DefaultCard from "../../../components/cards";
import { SelectFormUnit } from "../../../components/formUnits";
import { ALL, indexColumnNameConstants } from "./constants";

const schema = yup.object().shape({
  [indexColumnNameConstants.SUBNET]: yup
    .string()
    .required(`${getTitle(indexColumnNameConstants.SUBNET)} is required`),
});

function Index({ handleChange }) {
  const generateButton = useButtonGenerator();

  const { handleSubmit, control } = useForm({
    resolver: yupResolver(schema),
  });

  // hooks
  const { buttonsConfigurationObject } = useButtonsConfiguration({
    start_scanning_devices: null,
  });

  // apis
  const {
    data: fetchSubnetNamesData,
    isSuccess: isFetchSubnetNamesSuccess,
    isLoading: isFetchSubnetNamesLoading,
    isError: isFetchSubnetNamesError,
    error: fetchSubnetNamesError,
  } = useFetchSubnetNamesQuery();

  // error handling custom hooks
  useErrorHandling({
    data: fetchSubnetNamesData,
    isSuccess: isFetchSubnetNamesSuccess,
    isError: isFetchSubnetNamesError,
    error: fetchSubnetNamesError,
    type: TYPE_FETCH,
  });

  // selectors
  const subnetNames = useSelector(selectSubnetNames);

  // on form submit
  const onSubmit = (data) => {
    handleChange(data);
  };

  return (
    <DefaultCard sx={{ marginBottom: "10px" }}>
      <form
        onSubmit={handleSubmit(onSubmit)}
        style={{
          display: "flex",
          justifyContent: "space-between",
        }}
      >
        <div style={{ width: "100%", padding: "5px 0px 0 10px" }}>
          <SelectFormUnit
            control={control}
            dataKey={indexColumnNameConstants.SUBNET}
            // options={subnetNames ? [ALL, ...subnetNames] : []}
            options={subnetNames ? subnetNames : []}
            spinning={isFetchSubnetNamesLoading}
            label={false}
            required
            showErrorMessage={false}
            showErrorBoundary={true}
          />
        </div>
        &nbsp; &nbsp;
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            paddingRight: "10px",
          }}
        >
          {generateButton(buttonsConfigurationObject.start_scanning_devices)}
        </div>
      </form>
    </DefaultCard>
  );
}

export default Index;
