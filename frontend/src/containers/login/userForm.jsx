import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { useForm } from "react-hook-form";
import Grid from "@mui/material/Grid";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import { useRegisterMutation } from "../../store/features/login/apis";
import { formSetter, getTitle } from "../../utils/helpers";
import useErrorHandling, { TYPE_SINGLE } from "../../hooks/useErrorHandling";
import DefaultFormUnit from "../../components/formUnits";
import { UserDialogFooter } from "../../components/dialogFooters";
import DefaultSpinner from "../../components/spinners";
import { COMPANY, USER, userConstants } from "./constants";
import { MAIN_LAYOUT_PATH } from "../../layouts/mainLayout";
import { useSelector } from "react-redux/es/hooks/useSelector";
import {
  selectCompanyDetails,
  selectUserDetails,
} from "../../store/features/login/selectors";
import { setCompanyDetails, setUserDetails } from "../../store/features/login";

const schema = yup.object().shape({
  [userConstants.USER_NAME]: yup
    .string()
    .required(`${getTitle(userConstants.USER_NAME)} is required`),
  [userConstants.EMAIL_ADDRESS]: yup
    .string()
    .required(`${getTitle(userConstants.EMAIL_ADDRESS)} is required`),
  [userConstants.PASSWORD]: yup
    .string()
    .required(`${getTitle(userConstants.PASSWORD)} is required`),
  [userConstants.STATUS]: yup
    .string()
    .required(`${getTitle(userConstants.STATUS)} is required`),
  [userConstants.TEAM]: yup
    .string()
    .required(`${getTitle(userConstants.TEAM)} is required`),
  [userConstants.ACCOUNT_TYPE]: yup
    .string()
    .required(`${getTitle(userConstants.ACCOUNT_TYPE)} is required`),
  [userConstants.ROLE]: yup
    .string()
    .required(`${getTitle(userConstants.ROLE)} is required`),
  [userConstants.NAME]: yup
    .string()
    .required(`${getTitle(userConstants.NAME)} is required`),
});

const Index = ({ setCurrentForm }) => {
  // selectors
  const companyDetails = useSelector(selectCompanyDetails);
  const userDetails = useSelector(selectUserDetails);

  // hooks
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { handleSubmit, control, setValue, getValues } = useForm({
    resolver: yupResolver(schema),
  });

  // effects
  useEffect(() => {
    formSetter(userDetails, setValue);
  }, []);

  // post api for the form
  const [
    register,
    {
      data: registerData,
      isSuccess: isRegisterSuccess,
      isLoading: isRegisterLoading,
      isError: isRegisterError,
      error: registerError,
    },
  ] = useRegisterMutation();

  // error handling custom hooks
  useErrorHandling({
    data: registerData,
    isSuccess: isRegisterSuccess,
    isError: isRegisterError,
    error: registerError,
    type: TYPE_SINGLE,
  });

  // effects
  useEffect(() => {
    if (isRegisterSuccess) {
      dispatch(setUserDetails(null));
      dispatch(setCompanyDetails(null));

      navigate(`/${MAIN_LAYOUT_PATH}`);
    }
  }, [navigate, isRegisterSuccess]);

  // handlers
  function handleBack() {
    dispatch(setUserDetails(getValues()));
    setCurrentForm(COMPANY);
  }

  // on form submit
  const onSubmit = (data) => {
    register({ [COMPANY]: companyDetails, [USER]: data });
  };

  return (
    <DefaultSpinner spinning={isRegisterLoading}>
      <div style={{ display: "flex", marginBottom: "15px" }}>
        <div style={{ whiteSpace: "nowrap" }}>
          User Details &nbsp;&nbsp;&nbsp;
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
          <Grid item xs={6}>
            <DefaultFormUnit
              control={control}
              dataKey={userConstants.USER_NAME}
              required
            />
            <DefaultFormUnit
              type="email"
              control={control}
              dataKey={userConstants.EMAIL_ADDRESS}
              required
            />
            <DefaultFormUnit
              type="password"
              control={control}
              dataKey={userConstants.PASSWORD}
              required
            />
            <DefaultFormUnit
              control={control}
              dataKey={userConstants.NAME}
              required
            />
          </Grid>
          <Grid item xs={6}>
            <DefaultFormUnit
              control={control}
              dataKey={userConstants.ROLE}
              required
            />
            <DefaultFormUnit
              control={control}
              dataKey={userConstants.STATUS}
              required
            />
            <DefaultFormUnit
              control={control}
              dataKey={userConstants.TEAM}
              required
            />
            <DefaultFormUnit
              control={control}
              dataKey={userConstants.ACCOUNT_TYPE}
              required
            />
          </Grid>
          <Grid item xs={12}>
            <UserDialogFooter handleBack={handleBack} />
          </Grid>
        </Grid>
      </form>
    </DefaultSpinner>
  );
};

export default Index;
