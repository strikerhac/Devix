import React from "react";
import * as yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";
import { useForm } from "react-hook-form";
import { getTitle } from "../../../../utils/helpers";
import useButtonGenerator from "../../../../hooks/useButtonGenerator";
import useButtonsConfiguration from "../../../../hooks/useButtonsConfiguration";
import DefaultCard from "../../../../components/cards";
import DefaultFormUnit from "../../../../components/formUnits";
import { REMOTE_COMMAND } from "./constants";

const schema = yup.object().shape({
  [REMOTE_COMMAND]: yup
    .string()
    .required(`${getTitle(REMOTE_COMMAND)} is required`),
});

function Index({ onSubmit }) {
  const generateButton = useButtonGenerator();

  const { handleSubmit, control } = useForm({
    resolver: yupResolver(schema),
  });

  // hooks
  const { buttonsConfigurationObject } = useButtonsConfiguration({
    default_submit: null,
  });

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
          <DefaultFormUnit
            control={control}
            dataKey={REMOTE_COMMAND}
            required
            label={false}
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
          {generateButton(buttonsConfigurationObject.default_submit)}
        </div>
      </form>
    </DefaultCard>
  );
}

export default Index;
