import * as yup from "yup";
import { getTitle, isValidIPAddress } from "../../../utils/helpers";
import { ALPHA_NUMERIC_REGEX } from "../../../utils/constants/regex";
import { indexColumnNameConstants } from "./constants";

export const defaultSchema = yup.object().shape({});
