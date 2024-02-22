import * as XLSX from "xlsx";
import dayjs from "dayjs";

// Function to validate if a string is a valid IP address
export function isValidSubnet(value) {
  if (!value) return false; // Return false if value is empty
  const subnetRegex = /^(?:\d{1,3}\.){3}\d{1,3}\/\d{1,2}$/;
  if (!subnetRegex.test(value)) return false; // Check if subnet matches the format

  const [ip, mask] = value.split("/");

  if (!isValidIPAddress(ip)) {
    return false;
  }

  const maskValue = +mask;
  if (maskValue < 0 || maskValue > 32) return false; // Check if subnet mask is valid

  return true; // Return true if all checks pass
}

export function isValidIPAddress(ip) {
  // Valid Zero IP
  if (ip === "0.0.0.0") return true;

  // Loopback Address
  if (ip === "127.0.0.1") return true;
  const ipRegex = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;
  if (!ipRegex.test(ip)) return false;
  const parts = ip.split(".").map(Number);
  return parts.every((part) => part >= 0 && part <= 255);
}

export function isFirstLetterVowel(str) {
  // Convert the string to lowercase to handle both uppercase and lowercase vowels
  const firstLetter = str.charAt(0).toLowerCase();

  // Check if the first letter is a vowel
  return ["a", "e", "i", "o", "u"].includes(firstLetter);
}

export function getDefaultPagePath(MODULE_PATH, menuItems) {
  let pagePath = getPathAllSegments();
  if (pagePath.length === 3 && pagePath[2] === MODULE_PATH) {
    pagePath = [menuItems.length > 0 ? menuItems[0].path : ""];
  } else pagePath = pagePath.splice(3);
  return pagePath;
}

export function getPathLastSegment() {
  const path = window.location.pathname;
  const segments = path.split("/");
  return segments[segments.length - 1];
}

export function getPathSegment(position) {
  const path = window.location.pathname;
  const segments = path.split("/");
  return segments[position - 1];
}

export function getPathAllSegments() {
  const path = window.location.pathname;
  const segments = path.split("/");
  return segments;
}

export function getTitle(dataKey) {
  return dataKey
    ?.split("_")
    ?.map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    ?.join(" ");
}

export function convertToJson(headers, fileData) {
  let rows = [];
  fileData.forEach((row) => {
    const rowData = {};
    headers.forEach((element, index) => {
      if (row[index]) {
        rowData[element] = row[index];
      } else {
        rowData[element] = "";
      }
    });
    rows.push(rowData);
  });
  rows = rows.filter((value) => JSON.stringify(value) !== "{}");
  return rows;
}

// Function to handle file selection
export function handleFileChange(event, convertToJson, handlePostSeed) {
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.readAsBinaryString(file);
  reader.onload = (e) => {
    const bstr = e.target.result;
    const workbook = XLSX.read(bstr, { type: "binary" });
    const workSheetName = workbook.SheetNames[0];
    const workSheet = workbook.Sheets[workSheetName];
    const fileData = XLSX.utils.sheet_to_json(workSheet, {
      header: 1,
      raw: false,
    });
    const headers = fileData[0];
    fileData.splice(0, 1);
    let data = convertToJson(headers, fileData);
    data = data.filter(
      (obj) => !Object.values(obj).every((value) => value === "")
    );
    handlePostSeed(data);
  };
  event.target.value = null;
}

export function columnGenerator(dataKeys, getColumnSearchProps, getTitle) {
  return dataKeys.map((dataKey) => {
    return {
      title: getTitle(dataKey),
      dataIndex: dataKey,
      key: dataKey,
      ellipsis: true,
      ...getColumnSearchProps(dataKey),
    };
  });
}

export function jsonToExcel(jsonData, fileName) {
  let wb = XLSX.utils.book_new();
  let binarySeedData = XLSX.utils.json_to_sheet(jsonData);
  XLSX.utils.book_append_sheet(wb, binarySeedData, fileName);
  XLSX.writeFile(wb, `${fileName}.xlsx`);
}

export function formSetter(data, setValue, keyTypes = { dates: [] }) {
  if (data) {
    Object.keys(data).forEach((key) => {
      if (keyTypes.dates.includes(key)) {
        setValue(key, dayjs(data[key], "YYYY-MM-DD"));
      } else {
        setValue(key, data[key]);
      }
    });
  }
}

export function generateNumbersArray(upToValue) {
  return Array.from({ length: upToValue + 1 }, (_, index) => index);
}

export function generateObject(dataKeys) {
  return Object.fromEntries(dataKeys.map((key) => [key, ""]));
}

export function getTableScrollWidth(columns) {
  return columns.length * 210;
}

export function convertToAsterisks(inputString) {
  return "*".repeat(inputString?.length);
}

export function transformDateTimeToDate(originalValue, originalObject) {
  const date = new Date(originalValue);
  return date instanceof Date && !isNaN(date)
    ? new Date(date.getTime() - date.getTimezoneOffset() * 60000)
        .toISOString()
        .split("T")[0]
    : originalValue;
}

export function deepEqual(obj1, obj2) {
  // Check if both objects are objects
  if (obj1 !== null && obj2 !== null) {
    if (typeof obj1 !== "object" || typeof obj2 !== "object") {
      return false;
    }

    // Check if both objects have the same keys
    const keys1 = Object.keys(obj1);
    const keys2 = Object.keys(obj2);

    if (
      keys1.length !== keys2.length ||
      !keys1.every((key) => keys2.includes(key))
    ) {
      return false;
    }

    // Check the values of each property
    for (const key of keys1) {
      const val1 = obj1[key];
      const val2 = obj2[key];

      if (typeof val1 === "object" && typeof val2 === "object") {
        // Recursively check nested objects
        if (!deepEqual(val1, val2)) {
          return false;
        }
      } else if (val1 !== val2) {
        // Check primitive values
        return false;
      }
    }
    // If all checks pass, the objects are deeply equal
    return true;
  } else {
    return true;
  }
}
