import * as yup from "yup";
import { getTitle } from "../../../utils/helpers";
import { indexColumnNameConstants } from "./constants";
import { ALPHA_NUMERIC_REGEX_STARTING_WITH_ALPHABETS } from "../../../utils/constants/regex";

export const defaultSchema = yup.object().shape({
  [indexColumnNameConstants.ROLE]: yup
    .string()
    .required(`${getTitle(indexColumnNameConstants.ROLE)} is required`)
    .matches(ALPHA_NUMERIC_REGEX_STARTING_WITH_ALPHABETS, {
      message: "Invalid characters found",
      excludeEmptyString: true,
    }),
});
