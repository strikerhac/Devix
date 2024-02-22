import * as yup from "yup";
import { getTitle, isValidIPAddress } from "../../../utils/helpers";
import { indexColumnNameConstants } from "./constants";
import {
  ALPHA_NUMERIC_REGEX,
  ALPHA_NUMERIC_REGEX_STARTING_WITH_ALPHABETS,
} from "../../../utils/constants/regex";

export const defaultSchema = yup.object().shape({
  [indexColumnNameConstants.IP_ADDRESS]: yup
    .string()
    .required(`${getTitle(indexColumnNameConstants.IP_ADDRESS)} is required`)
    .test(
      `valid ${indexColumnNameConstants.IP_ADDRESS}`,
      `Invalid ${getTitle(indexColumnNameConstants.IP_ADDRESS)}`,
      (value) => isValidIPAddress(value)
    ),
  [indexColumnNameConstants.SECTION]: yup
    .string()
    .nullable()
    .matches(ALPHA_NUMERIC_REGEX, {
      message: "Invalid characters found",
      excludeEmptyString: true,
    }),
  [indexColumnNameConstants.DEPARTMENT]: yup
    .string()
    .nullable()
    .matches(ALPHA_NUMERIC_REGEX_STARTING_WITH_ALPHABETS, {
      message: "Invalid characters found",
      excludeEmptyString: true,
    }),
  [indexColumnNameConstants.DOMAIN]: yup
    .string()
    .nullable()
    .matches(ALPHA_NUMERIC_REGEX_STARTING_WITH_ALPHABETS, {
      message: "Invalid characters found",
      excludeEmptyString: true,
    }),
});
