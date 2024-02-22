import * as yup from "yup";
import { getTitle } from "../../../../../utils/helpers";
import { ALPHA_NUMERIC_REGEX_STARTING_WITH_ALPHABETS } from "../../../../../utils/constants/regex";
import { indexColumnNameConstants } from "./constants";

export const defaultSchema = yup.object().shape({
  [indexColumnNameConstants.ACCOUNT_LABEL]: yup
    .string()
    .required(`${getTitle(indexColumnNameConstants.ACCOUNT_LABEL)} is required`)
    .matches(ALPHA_NUMERIC_REGEX_STARTING_WITH_ALPHABETS, {
      message: "Invalid characters found",
      excludeEmptyString: true,
    }),
  [indexColumnNameConstants.ACCESS_KEY]: yup
    .string()
    .required(`${getTitle(indexColumnNameConstants.ACCESS_KEY)} is required`),
  [indexColumnNameConstants.SECRET_ACCESS_KEY]: yup
    .string()
    .required(
      `${getTitle(indexColumnNameConstants.SECRET_ACCESS_KEY)} is required`
    ),
});
