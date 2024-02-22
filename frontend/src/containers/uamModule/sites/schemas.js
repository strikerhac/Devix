import * as yup from "yup";
import { getTitle } from "../../../utils/helpers";
import { indexColumnNameConstants } from "./constants";
import {
  ALPHA_NUMERIC_REGEX,
  ALPHA_NUMERIC_REGEX_STARTING_WITH_ALPHABETS,
} from "../../../utils/constants/regex";

export const defaultSchema = yup.object().shape({
  [indexColumnNameConstants.SITE_NAME]: yup
    .string()
    .required(`${getTitle(indexColumnNameConstants.SITE_NAME)} is required`)
    .matches(ALPHA_NUMERIC_REGEX_STARTING_WITH_ALPHABETS, {
      message: "Invalid characters found",
      excludeEmptyString: true,
    }),
  [indexColumnNameConstants.STATUS]: yup
    .string()
    .required(`${getTitle(indexColumnNameConstants.STATUS)} is required`),

  [indexColumnNameConstants.REGION_NAME]: yup
    .string()
    .nullable()
    .matches(ALPHA_NUMERIC_REGEX_STARTING_WITH_ALPHABETS, {
      message: "Invalid characters found",
      excludeEmptyString: true,
    }),
  [indexColumnNameConstants.CITY]: yup
    .string()
    .nullable()
    .matches(ALPHA_NUMERIC_REGEX_STARTING_WITH_ALPHABETS, {
      message: "Invalid characters found",
      excludeEmptyString: true,
    }),
  [indexColumnNameConstants.LATITUDE]: yup
    .string()
    .nullable()
    .matches(ALPHA_NUMERIC_REGEX, {
      message: "Invalid characters found",
      excludeEmptyString: true,
    }),
  [indexColumnNameConstants.LONGITUDE]: yup
    .string()
    .nullable()
    .matches(ALPHA_NUMERIC_REGEX, {
      message: "Invalid characters found",
      excludeEmptyString: true,
    }),
});
