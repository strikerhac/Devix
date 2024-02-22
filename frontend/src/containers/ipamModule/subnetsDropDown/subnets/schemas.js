import * as yup from "yup";
import { getTitle, isValidSubnet } from "../../../../utils/helpers";
import {
  ALPHA_NUMERIC_REGEX,
  ALPHA_NUMERIC_REGEX_STARTING_WITH_ALPHABETS,
} from "../../../../utils/constants/regex";
import { indexColumnNameConstants } from "./constants";

export const defaultSchema = yup.object().shape({
  [indexColumnNameConstants.SUBNET_ADDRESS]: yup
    .string()
    .required(
      `${getTitle(indexColumnNameConstants.SUBNET_ADDRESS)} is required`
    )
    .test(
      `valid ${indexColumnNameConstants.SUBNET_ADDRESS}`,
      `Invalid ${getTitle(indexColumnNameConstants.SUBNET_ADDRESS)}`,
      (value) => isValidSubnet(value)
    ),
  [indexColumnNameConstants.SUBNET_NAME]: yup
    .string()
    .required(`${getTitle(indexColumnNameConstants.SUBNET_NAME)} is required`)
    .matches(
      ALPHA_NUMERIC_REGEX_STARTING_WITH_ALPHABETS,
      "Invalid characters found"
    ),
  [indexColumnNameConstants.SUBNET_MASK]: yup
    .string()
    .required(`${getTitle(indexColumnNameConstants.SUBNET_MASK)} is required`)
    .matches(
      /^(255|254|252|248|240|224|192|128|0)\.(0|128|192|224|240|248|252|254|255)\.(0|128|192|224|240|248|252|254|255)\.(0|128|192|224|240|248|252|254|255)$/,
      `Invalid ${getTitle(indexColumnNameConstants.SUBNET_MASK)} format`
    ),
  [indexColumnNameConstants.SUBNET_LOCATION]: yup
    .string()
    .nullable()
    .matches(ALPHA_NUMERIC_REGEX_STARTING_WITH_ALPHABETS, {
      message: "Invalid characters found",
      excludeEmptyString: true,
    }),
});
