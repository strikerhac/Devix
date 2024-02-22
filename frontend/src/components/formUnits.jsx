import React from "react";
import DefaultWrapper from "./wrappers";
import DefaultLabel from "./labels";
import { InputWrapper } from "./wrappers";
import DefaultInput, { PasswordInput } from "./inputs";
import DefaultSelect, { AddableSelect } from "./selects";
import DefaultOption from "./options";
import { Controller } from "react-hook-form";
import { getTitle, isFirstLetterVowel } from "../utils/helpers";
import { useTheme } from "@mui/material/styles";
import DefaultDate from "./dates";
import DefaultSpinner from "./spinners";

export default function DefaultFormUnit({
  control,
  dataKey,
  type = "text",
  required = false,
  label = true,
  sx,
  spinning = false,
  showErrorMessage = true,
  showErrorBoundary = false,
  ...rest
}) {
  const theme = useTheme();
  const title = getTitle(dataKey);
  return (
    <Controller
      name={dataKey}
      control={control}
      render={({ field, fieldState }) => {
        return (
          <DefaultWrapper sx={{ marginBottom: "10px" }}>
            {label ? (
              <DefaultLabel htmlFor={dataKey} required={required}>
                {title}:
              </DefaultLabel>
            ) : null}
            <DefaultSpinner spinning={spinning}>
              <InputWrapper>
                {type !== "password" ? (
                  <DefaultInput
                    field={field}
                    name={dataKey}
                    id={dataKey}
                    placeholder={title}
                    type={type}
                    sx={
                      fieldState.error && showErrorBoundary
                        ? { border: "2px solid #E34444", ...sx }
                        : { ...sx }
                    }
                    {...rest}
                  />
                ) : null}

                {type === "password" ? (
                  <PasswordInput
                    field={field}
                    name={dataKey}
                    id={dataKey}
                    placeholder={title}
                    type={type}
                    sx={sx}
                    {...rest}
                  />
                ) : null}
              </InputWrapper>
            </DefaultSpinner>
            {showErrorMessage ? (
              <div
                style={{
                  color: theme?.palette?.form_unit?.error_text,
                  fontSize: "12px",
                }}
              >
                {fieldState.error && fieldState.error.message}
              </div>
            ) : null}
          </DefaultWrapper>
        );
      }}
    />
  );
}

export function SelectFormUnit({
  control,
  dataKey,
  options,
  required = false,
  label = true,
  spinning = false,
  showErrorMessage = true,
  showErrorBoundary = false,
  ...rest
}) {
  const theme = useTheme();
  const title = getTitle(dataKey);
  return (
    <Controller
      name={dataKey}
      control={control}
      render={({ field, fieldState }) => {
        return (
          <DefaultWrapper sx={{ marginBottom: "10px" }}>
            {label ? (
              <DefaultLabel htmlFor={dataKey} required={required}>
                {title}:
              </DefaultLabel>
            ) : null}
            <DefaultSpinner spinning={spinning}>
              <InputWrapper>
                <DefaultSelect
                  field={field}
                  sx={
                    fieldState.error && showErrorBoundary
                      ? { border: "2px solid #E34444" }
                      : null
                  }
                  id={dataKey}
                  {...rest}
                >
                  <DefaultOption
                    value=""
                    sx={{
                      color: theme.palette.default_select.place_holder,
                    }}
                  >
                    Select {isFirstLetterVowel(title) ? "an" : "a"} {title}
                  </DefaultOption>
                  {options?.map((value) => (
                    <DefaultOption value={value}>{value}</DefaultOption>
                  ))}
                </DefaultSelect>
              </InputWrapper>
            </DefaultSpinner>
            {showErrorMessage ? (
              <div
                style={{
                  color: theme?.palette?.form_unit?.error_text,
                  fontSize: "12px",
                }}
              >
                {fieldState.error && fieldState.error.message}
              </div>
            ) : null}
          </DefaultWrapper>
        );
      }}
    />
  );
}

export function SelectFormUnitWithHiddenValues({
  control,
  dataKey,
  options,
  required = false,
  label = true,
  spinning = false,
  optionalTitle = null,
  ...rest
}) {
  const theme = useTheme();
  const title = getTitle(optionalTitle ? optionalTitle : dataKey);
  return (
    <Controller
      name={dataKey}
      control={control}
      render={({ field, fieldState }) => {
        return (
          <DefaultWrapper sx={{ marginBottom: "10px" }}>
            {label ? (
              <DefaultLabel htmlFor={dataKey} required={required}>
                {title}:
              </DefaultLabel>
            ) : null}
            <DefaultSpinner spinning={spinning}>
              <InputWrapper>
                <DefaultSelect
                  field={field}
                  sx={{ outline: "none" }}
                  id={dataKey}
                  {...rest}
                >
                  <DefaultOption
                    value=""
                    sx={{
                      color: theme.palette.default_select.place_holder,
                    }}
                  >
                    Select a {title}
                  </DefaultOption>
                  {options?.map((item) => (
                    <DefaultOption value={item.value}>
                      {item.name}
                    </DefaultOption>
                  ))}
                </DefaultSelect>
              </InputWrapper>
            </DefaultSpinner>

            <div
              style={{
                color: theme?.palette?.form_unit?.error_text,
                fontSize: "12px",
              }}
            >
              {fieldState.error && fieldState.error.message}
            </div>
          </DefaultWrapper>
        );
      }}
    />
  );
}

export function AddableSelectFormUnit({
  control,
  dataKey,
  options,
  required = false,
  label = true,
  spinning = false,
  ...rest
}) {
  const theme = useTheme();
  const title = getTitle(dataKey);
  return (
    <Controller
      name={dataKey}
      control={control}
      render={({ field, fieldState }) => {
        return (
          <DefaultWrapper sx={{ marginBottom: "10px" }}>
            {label ? (
              <DefaultLabel htmlFor={dataKey} required={required}>
                {title}:
              </DefaultLabel>
            ) : null}
            <DefaultSpinner spinning={spinning}>
              <InputWrapper>
                <AddableSelect
                  field={field}
                  sx={{ outline: "none" }}
                  id={dataKey}
                  {...rest}
                >
                  <DefaultOption
                    value=""
                    sx={{
                      color: theme.palette.default_select.place_holder,
                    }}
                  >
                    Select a {title}
                  </DefaultOption>
                  {options?.map((value) => (
                    <DefaultOption value={value}>{value}</DefaultOption>
                  ))}
                </AddableSelect>
              </InputWrapper>
            </DefaultSpinner>

            <div
              style={{
                color: theme?.palette?.form_unit?.error_text,
                fontSize: "12px",
              }}
            >
              {fieldState.error && fieldState.error.message}
            </div>
          </DefaultWrapper>
        );
      }}
    />
  );
}

export function DateFormUnit({
  control,
  dataKey,
  options,
  required = false,
  label = true,
  spinning = false,
  ...rest
}) {
  const theme = useTheme();
  const title = getTitle(dataKey);
  return (
    <Controller
      name={dataKey}
      control={control}
      render={({ field, fieldState }) => {
        return (
          <DefaultWrapper sx={{ marginBottom: "10px" }}>
            {label ? (
              <DefaultLabel htmlFor={dataKey} required={required}>
                {title}:
              </DefaultLabel>
            ) : null}
            <DefaultSpinner spinning={spinning}>
              <InputWrapper>
                <DefaultDate
                  field={field}
                  sx={{ outline: "none" }}
                  id={dataKey}
                  {...rest}
                />
              </InputWrapper>
            </DefaultSpinner>

            <div
              style={{
                color: theme?.palette?.form_unit?.error_text,
                fontSize: "12px",
              }}
            >
              {fieldState.error && fieldState.error.message}
            </div>
          </DefaultWrapper>
        );
      }}
    />
  );
}
