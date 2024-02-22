import * as yup from "yup";
import {
  getTitle,
  isValidIPAddress,
  isValidSubnet,
} from "../../../utils/helpers";
import { indexColumnNameConstants } from "./constants";
import { ALPHA_NUMERIC_REGEX_STARTING_WITH_ALPHABETS } from "../../../utils/constants/regex";

export const defaultSchema = yup.object().shape({
  [indexColumnNameConstants.NETWORK_NAME]: yup
    .string()
    .required(`${getTitle(indexColumnNameConstants.NETWORK_NAME)} is required`)
    .matches(
      ALPHA_NUMERIC_REGEX_STARTING_WITH_ALPHABETS,
      "Invalid characters found"
    ),

  [indexColumnNameConstants.SUBNET]: yup
    .string()
    .required(`${getTitle(indexColumnNameConstants.SUBNET)} is required`)
    .test(
      `valid ${indexColumnNameConstants.SUBNET}`,
      `Invalid ${getTitle(indexColumnNameConstants.SUBNET)} format`,
      (value) => isValidSubnet(value)
    ),
  [indexColumnNameConstants.SCAN_STATUS]: yup
    .string()
    .required(`${getTitle(indexColumnNameConstants.SCAN_STATUS)} is required`),
  [indexColumnNameConstants.EXCLUDED_IP_RANGE]: yup
    .string()
    .test(
      `valid ${indexColumnNameConstants.EXCLUDED_IP_RANGE}`,
      `Invalid ${getTitle(indexColumnNameConstants.EXCLUDED_IP_RANGE)} format`,
      (value) => {
        if (!value) return true; // Return false if value is empty

        // Split the input string by comma to get individual IP ranges
        const ipRanges = value.split(",");

        // Define a regex pattern to match the IP range format
        const ipRangeRegex =
          /^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})-(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$/;

        // Iterate through each IP range and validate
        for (let ipRange of ipRanges) {
          // Check if the IP range matches the regex pattern
          if (!ipRangeRegex.test(ipRange)) return false;

          // Extract start and end IPs from the range
          const [startIP, endIP] = ipRange.split("-");

          // Check if start and end IPs are valid IP addresses
          if (!isValidIPAddress(startIP) || !isValidIPAddress(endIP))
            return false;

          // Convert start and end IPs to arrays of parts
          const startParts = startIP.split(".").map(Number);
          const endParts = endIP.split(".").map(Number);

          // Check if each part of start and end IPs are valid numbers between 0 and 255
          if (
            startParts.some((part) => isNaN(part) || part < 0 || part > 255) ||
            endParts.some((part) => isNaN(part) || part < 0 || part > 255)
          ) {
            return false;
          }

          // Check if start IP is less than or equal to end IP
          for (let i = 0; i < 4; i++) {
            if (startParts[i] > endParts[i]) return false;
          }
        }

        return true; // Return true if all checks pass
      }
    ),
});
