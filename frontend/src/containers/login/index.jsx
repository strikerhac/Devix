import React, { useState } from "react";
import LoginPageLeftImage from "../../resources/svgs/loginPageLeftImage.svg";
import { useSelector } from "react-redux/es/hooks/useSelector";
import { selectIsAnyCompanyRegistered } from "../../store/features/login/selectors";
import { useCheckIsAnyCompanyRegisteredQuery } from "../../store/features/login/apis";
import useErrorHandling, { TYPE_SINGLE } from "../../hooks/useErrorHandling";
import Form from "./form";
import CompanyForm from "./companyForm";
import UserForm from "./userForm";
import DefaultCard from "../../components/cards";
import { LOGIN, COMPANY, USER } from "./constants";

function Index(props) {
  const [currentForm, setCurrentForm] = useState(LOGIN);

  // selectors
  const isAnyCompanyRegistered = useSelector(selectIsAnyCompanyRegistered);

  // apis
  const {
    data: checkIsAnyCompanyRegisteredData,
    isSuccess: isCheckIsAnyCompanyRegisteredSuccess,
    isLoading: isCheckIsAnyCompanyRegisteredLoading,
    isError: isCheckIsAnyCompanyRegisteredError,
    error: checkIsAnyCompanyRegisteredError,
  } = useCheckIsAnyCompanyRegisteredQuery();

  // error handling custom hooks
  useErrorHandling({
    data: checkIsAnyCompanyRegisteredData,
    isSuccess: isCheckIsAnyCompanyRegisteredSuccess,
    isError: isCheckIsAnyCompanyRegisteredError,
    error: checkIsAnyCompanyRegisteredError,
    type: TYPE_SINGLE,
    showMessage: false,
  });

  return (
    <div style={{ backgroundColor: "white" }}>
      {currentForm === COMPANY || currentForm === USER ? (
        <div
          style={{
            padding: "5%",
            backgroundColor: "#F7F7F7",
            minHeight: "79vh",
          }}
        >
          <DefaultCard sx={{ padding: "20px" }}>
            <div style={{ marginBottom: "15px" }}>
              Please add your details to first time setup the Monetx platform.
            </div>
            {currentForm === COMPANY ? (
              <CompanyForm setCurrentForm={setCurrentForm} />
            ) : null}
            {currentForm === USER ? (
              <UserForm setCurrentForm={setCurrentForm} />
            ) : null}
          </DefaultCard>
        </div>
      ) : null}
      {currentForm === LOGIN ? (
        <div style={{ height: "96vh", display: "flex", padding: "2vh" }}>
          <div style={{ position: "relative", width: "50%" }}>
            <img
              src={LoginPageLeftImage}
              alt="theme"
              height={"100%"}
              width={"100%"}
              style={{ objectFit: "cover", borderRadius: "7px" }}
            />
            <div
              style={{
                position: "absolute",
                top: "14%",
                left: "40%",
                transform: "translate(-50%, -50%)",
                color: "white",
                fontSize: "14px",
              }}
            >
              <div>
                <p>One Stop, Many Solutions</p>
                <p>
                  One Solution that Speed up your Device Reports and Make
                  Efficient way to organize your data.
                </p>
              </div>
            </div>
          </div>
          <div
            style={{
              width: "50%",
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "center",
              }}
            >
              <Form
                setCurrentForm={setCurrentForm}
                isAnyCompanyRegistered={isAnyCompanyRegistered}
                isCheckIsAnyCompanyRegisteredLoading={
                  isCheckIsAnyCompanyRegisteredLoading
                }
              />
            </div>
            <p
              style={{
                position: "absolute",
                bottom: "3px",
                right: "15px",
                padding: "5px",
                fontSize: "12px",
                color: "#949494",
              }}
            >
              &copy; 2023 All rights reserved
            </p>
          </div>
        </div>
      ) : null}
    </div>
  );
}

export default Index;
