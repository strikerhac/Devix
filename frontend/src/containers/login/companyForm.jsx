import React, { useEffect } from "react";
import { useDispatch } from "react-redux";
import { useForm } from "react-hook-form";
import Grid from "@mui/material/Grid";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import { formSetter, getTitle } from "../../utils/helpers";
import DefaultFormUnit, { DateFormUnit } from "../../components/formUnits";
import { CompanyDialogFooter } from "../../components/dialogFooters";
import DefaultSpinner from "../../components/spinners";
import { LOGIN, USER, companyConstants } from "./constants";
import { setCompanyDetails } from "../../store/features/login";
import { selectCompanyDetails } from "../../store/features/login/selectors";
import { useSelector } from "react-redux/es/hooks/useSelector";

const schema = yup.object().shape({
  [companyConstants.COMPANY_NAME]: yup
    .string()
    .required(`${getTitle(companyConstants.COMPANY_NAME)} is required`),
  [companyConstants.PO_BOX]: yup
    .string()
    .required(`${getTitle(companyConstants.PO_BOX)} is required`),
  [companyConstants.ADDRESS]: yup
    .string()
    .required(`${getTitle(companyConstants.ADDRESS)} is required`),
  [companyConstants.STREET_NAME]: yup
    .string()
    .required(`${getTitle(companyConstants.STREET_NAME)} is required`),
  [companyConstants.CITY]: yup
    .string()
    .required(`${getTitle(companyConstants.CITY)} is required`),
  [companyConstants.COUNTRY]: yup
    .string()
    .required(`${getTitle(companyConstants.COUNTRY)} is required`),
  [companyConstants.CONTACT_PERSON]: yup
    .string()
    .required(`${getTitle(companyConstants.CONTACT_PERSON)} is required`),
  [companyConstants.CONTACT_NUMBER]: yup
    .string()
    .required(`${getTitle(companyConstants.CONTACT_NUMBER)} is required`),
  [companyConstants.EMAIL]: yup
    .string()
    .required(`${getTitle(companyConstants.EMAIL)} is required`),
  [companyConstants.DOMAIN_NAME]: yup
    .string()
    .required(`${getTitle(companyConstants.DOMAIN_NAME)} is required`),
  [companyConstants.INDUSTRY_TYPE]: yup
    .string()
    .required(`${getTitle(companyConstants.INDUSTRY_TYPE)} is required`),
  [companyConstants.LICENSE_START_DATE]: yup
    .string()
    .required(`${getTitle(companyConstants.LICENSE_START_DATE)} is required`),
  [companyConstants.LICENSE_END_DATE]: yup
    .string()
    .required(`${getTitle(companyConstants.LICENSE_END_DATE)} is required`),
  [companyConstants.DEVICE_ONBOARD_LIMIT]: yup
    .string()
    .required(`${getTitle(companyConstants.DEVICE_ONBOARD_LIMIT)} is required`),
});

const Index = ({ setCurrentForm }) => {
  // selectors
  const companyDetails = useSelector(selectCompanyDetails);

  // hooks
  const dispatch = useDispatch();
  const { handleSubmit, control, setValue, getValues } = useForm({
    resolver: yupResolver(schema),
  });

  // effects
  useEffect(() => {
    formSetter(companyDetails, setValue);
  }, []);

  // handlers
  function handleBack() {
    dispatch(setCompanyDetails(getValues()));
    setCurrentForm(LOGIN);
  }

  // on form submit
  const onSubmit = (data) => {
    dispatch(setCompanyDetails(data));
    setCurrentForm(USER);
  };

  return (
    <DefaultSpinner spinning={false}>
      <div style={{ display: "flex", marginBottom: "15px" }}>
        <div style={{ whiteSpace: "nowrap" }}>
          Company Details &nbsp;&nbsp;&nbsp;
        </div>
        <div
          style={{
            width: "100%",
            height: "2px",
            marginTop: "12px",
            backgroundColor: "#F6F6F6",
          }}
        ></div>
      </div>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Grid container spacing={5}>
          <Grid item xs={4}>
            <DefaultFormUnit
              control={control}
              dataKey={companyConstants.COMPANY_NAME}
              required
            />
            <DefaultFormUnit
              control={control}
              dataKey={companyConstants.PO_BOX}
              required
            />
            <DefaultFormUnit
              control={control}
              dataKey={companyConstants.ADDRESS}
              required
            />
            <DefaultFormUnit
              control={control}
              dataKey={companyConstants.STREET_NAME}
              required
            />
            <DefaultFormUnit
              control={control}
              dataKey={companyConstants.CITY}
              required
            />
          </Grid>
          <Grid item xs={4}>
            <DefaultFormUnit
              control={control}
              dataKey={companyConstants.COUNTRY}
              required
            />
            <DefaultFormUnit
              control={control}
              dataKey={companyConstants.CONTACT_PERSON}
              required
            />

            <DefaultFormUnit
              control={control}
              dataKey={companyConstants.CONTACT_NUMBER}
              required
            />
            <DefaultFormUnit
              type="email"
              control={control}
              dataKey={companyConstants.EMAIL}
              required
            />
            <DefaultFormUnit
              control={control}
              dataKey={companyConstants.DOMAIN_NAME}
              required
            />
          </Grid>
          <Grid item xs={4}>
            <DefaultFormUnit
              control={control}
              dataKey={companyConstants.INDUSTRY_TYPE}
              required
            />
            <DateFormUnit
              control={control}
              dataKey={companyConstants.LICENSE_START_DATE}
              required
            />
            <DateFormUnit
              control={control}
              dataKey={companyConstants.LICENSE_END_DATE}
              required
            />
            <DefaultFormUnit
              control={control}
              dataKey={companyConstants.DEVICE_ONBOARD_LIMIT}
              required
            />
          </Grid>
          <Grid item xs={12}>
            <CompanyDialogFooter handleBack={handleBack} />
          </Grid>
        </Grid>
      </form>
    </DefaultSpinner>
  );
};

export default Index;
