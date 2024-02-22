import * as yup from "yup";
import { getTitle } from "../../../utils/helpers";
import { indexColumnNameConstants } from "./constants";
import {
  ALPHA_NUMERIC_REGEX_STARTING_WITH_ALPHABETS,
  ALPHA_NUMERIC_WITH_FOUR_EXTRA_CHARACTERS_REGEX_STARTING_WITH_ALPHABETS,
  ONLY_ALPHABETS,
} from "../../../utils/constants/regex";

export const defaultSchema = yup.object().shape({
  [indexColumnNameConstants.USER_NAME]: yup
    .string()
    .required(`${getTitle(indexColumnNameConstants.USER_NAME)} is required`)
    .matches(
      ALPHA_NUMERIC_WITH_FOUR_EXTRA_CHARACTERS_REGEX_STARTING_WITH_ALPHABETS,
      {
        message: "Invalid characters found",
        excludeEmptyString: true,
      }
    ),
  [indexColumnNameConstants.PASSWORD]: yup
    .string()
    .required(`${getTitle(indexColumnNameConstants.PASSWORD)} is required`),
  [indexColumnNameConstants.EMAIL]: yup
    .string()
    .required(`${getTitle(indexColumnNameConstants.EMAIL)} is required`),
  [indexColumnNameConstants.NAME]: yup
    .string()
    .required(`${getTitle(indexColumnNameConstants.NAME)} is required`)
    .matches(ONLY_ALPHABETS, {
      message: "Invalid characters found",
      excludeEmptyString: true,
    }),
  [indexColumnNameConstants.ROLE]: yup
    .string()
    .required(`${getTitle(indexColumnNameConstants.ROLE)} is required`),
  [indexColumnNameConstants.STATUS]: yup
    .string()
    .required(`${getTitle(indexColumnNameConstants.STATUS)} is required`),
  [indexColumnNameConstants.ACCOUNT_TYPE]: yup
    .string()
    .required(`${getTitle(indexColumnNameConstants.ACCOUNT_TYPE)} is required`),
  [indexColumnNameConstants.TEAM]: yup
    .string()
    .matches(ALPHA_NUMERIC_REGEX_STARTING_WITH_ALPHABETS, {
      message: "Invalid characters found",
      excludeEmptyString: true,
    }),
});
