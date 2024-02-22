import * as yup from "yup";
import { getTitle, transformDateTimeToDate } from "../../../utils/helpers";
import { indexColumnNameConstants } from "./constants";
import { ALPHA_NUMERIC_REGEX_STARTING_WITH_ALPHABETS } from "../../../utils/constants/regex";

export const defaultSchema = yup.object().shape({
  [indexColumnNameConstants.PN_CODE]: yup
    .string()
    .required(`${getTitle(indexColumnNameConstants.PN_CODE)} is required`)
    .matches(ALPHA_NUMERIC_REGEX_STARTING_WITH_ALPHABETS, {
      message: "Invalid characters found",
      excludeEmptyString: true,
    }),
  [indexColumnNameConstants.HW_EOS_DATE]: yup
    .string()
    .transform(transformDateTimeToDate),
  [indexColumnNameConstants.HW_EOL_DATE]: yup
    .string()
    .transform(transformDateTimeToDate),
  [indexColumnNameConstants.SW_EOS_DATE]: yup
    .string()
    .transform(transformDateTimeToDate),
  [indexColumnNameConstants.SW_EOL_DATE]: yup
    .string()
    .transform(transformDateTimeToDate),
  [indexColumnNameConstants.MANUFACTURE_DATE]: yup
    .string()
    .transform(transformDateTimeToDate),
});
