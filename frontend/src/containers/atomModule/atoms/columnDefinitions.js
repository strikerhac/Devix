import React from "react";
import { Icon } from "@iconify/react";
import Tooltip from "@mui/material/Tooltip";
import { useTheme } from "@mui/material/styles";
import DefaultSelect from "../../../components/selects";
import DefaultOption from "../../../components/options";
import { ATOM_ID, indexColumnNameConstants } from "./constants";
import { MONITORING_CREDENTIALS_ID } from "../../monitoringModule/devices/constants";
import { getTitle } from "../../../utils/helpers";

export function useIndexTableColumnDefinitions({
  pageEditable,
  handleEdit = null,
  dropDowns = null,
} = {}) {
  function getRequiredFieldsTitle(record) {
    let title = "";
    if (!record[indexColumnNameConstants.IP_ADDRESS]) {
      title += `${getTitle(indexColumnNameConstants.IP_ADDRESS)}, `;
    }
    if (!record[indexColumnNameConstants.FUNCTION]) {
      title += `${getTitle(indexColumnNameConstants.FUNCTION)}, `;
    }
    if (!record[indexColumnNameConstants.VENDOR]) {
      title += `${getTitle(indexColumnNameConstants.VENDOR)}, `;
    }
    if (!record[indexColumnNameConstants.PASSWORD_GROUP]) {
      title += `${getTitle(indexColumnNameConstants.PASSWORD_GROUP)}, `;
    }
    if (!record[indexColumnNameConstants.DEVICE_NAME]) {
      title += `${getTitle(indexColumnNameConstants.DEVICE_NAME)}`;
    }

    // Remove the last comma if it exists
    if (title.endsWith(", ")) {
      title = title.slice(0, -2); // Remove the last two characters (comma and space)
    }

    // Append period if title is not empty
    if (title !== "") {
      title += ".";
    }

    return title;
  }

  const theme = useTheme();

  const monitoringCredentialsOptions =
    dropDowns?.data[MONITORING_CREDENTIALS_ID];

  const columnDefinitions = [
    {
      data_key: indexColumnNameConstants.STATUS,
      search: false,
      width: "80px",
      align: "center",
      render: (text, record) => {
        const icon = record.atom_id ? (
          <Icon
            fontSize={"22px"}
            color={theme?.palette?.icon?.complete}
            icon="ep:success-filled"
          />
        ) : (
          <Tooltip
            title={`Following fields are required to complete the atom: ${getRequiredFieldsTitle(
              record
            )} `}
          >
            <Icon
              fontSize={"23px"}
              color={theme?.palette?.icon?.incomplete}
              icon="material-symbols:info"
              style={{ cursor: "pointer" }}
            />
          </Tooltip>
        );

        return <div style={{ textAlign: "center" }}>{icon}</div>;
      },
    },
    indexColumnNameConstants.IP_ADDRESS,
    indexColumnNameConstants.SITE_NAME,
    indexColumnNameConstants.RACK_NAME,
    indexColumnNameConstants.DEVICE_NAME,
    indexColumnNameConstants.DEVICE_RU,
    indexColumnNameConstants.DEPARTMENT,
    indexColumnNameConstants.DOMAIN,
    indexColumnNameConstants.SECTION,
    indexColumnNameConstants.FUNCTION,
    indexColumnNameConstants.VIRTUAL,
    indexColumnNameConstants.DEVICE_TYPE,
    indexColumnNameConstants.VENDOR,
    indexColumnNameConstants.CRITICALITY,
    indexColumnNameConstants.PASSWORD_GROUP,
    {
      data_key: indexColumnNameConstants.ONBOARD_STATUS,
      title: "Board",
      fixed: "right",
      align: "center",
      width: 80,
      render: (text, record) => (
        <div
          style={{
            textAlign: "center",
          }}
        >
          {record.onboard_status === true ? (
            <span
              style={{
                display: "inline-block",
                borderRadius: "10px",
                backgroundColor: "#c2dfbf",
                color: "#3D9E47",
                padding: "1px 15px",
              }}
            >
              True
            </span>
          ) : record.onboard_status === false ? (
            <div
              style={{
                display: "inline-block",
                borderRadius: "10px",
                backgroundColor: "#ffe2dd",
                color: "#E34444",
                padding: "1px 15px",
              }}
            >
              False
            </div>
          ) : null}
        </div>
      ),
    },
    {
      data_key: indexColumnNameConstants.ACTIONS,
      search: false,
      fixed: "right",
      align: "center",
      width: 100,
      render: (text, record) => (
        <div
          style={{
            display: "flex",
            gap: "10px",
            justifyContent: "center",
          }}
        >
          <Icon
            fontSize={"15px"}
            onClick={() => handleEdit(record)}
            icon="bx:edit"
            style={{ cursor: "pointer" }}
          />
        </div>
      ),
    },
  ].filter((item) => {
    if (typeof item === "object") {
      if (pageEditable) {
        return true;
      } else {
        return item.data_key !== indexColumnNameConstants.ACTIONS;
      }
    } else {
      return true;
    }
  });

  const columnDefinitionsForIpamDevices = [
    indexColumnNameConstants.IP_ADDRESS,
    indexColumnNameConstants.DEVICE_NAME,
    indexColumnNameConstants.FUNCTION,
    indexColumnNameConstants.VENDOR,
  ];

  const columnDefinitionsForNcmDevices = [
    indexColumnNameConstants.IP_ADDRESS,
    indexColumnNameConstants.DEVICE_NAME,
    indexColumnNameConstants.FUNCTION,
    indexColumnNameConstants.VENDOR,
  ];

  const columnDefinitionsForMonitoringDevices = [
    indexColumnNameConstants.IP_ADDRESS,
    indexColumnNameConstants.DEVICE_NAME,
    indexColumnNameConstants.DEVICE_TYPE,
    indexColumnNameConstants.VENDOR,
    {
      data_key: MONITORING_CREDENTIALS_ID,
      title: "Credentials",
      search: false,
      fixed: "right",
      align: "center",
      width: 200,
      render: (text, record) => (
        <DefaultSelect
          onChange={(event) =>
            dropDowns.handler(
              MONITORING_CREDENTIALS_ID,
              record[ATOM_ID],
              event.target.value
            )
          }
        >
          {monitoringCredentialsOptions.map((item) => (
            <DefaultOption key={item.value} value={item.value}>
              {item.name}
            </DefaultOption>
          ))}
        </DefaultSelect>
      ),
    },
  ];

  const dataKeys = columnDefinitions
    .map((item) => {
      if (typeof item === "object") {
        return item.data_key;
      } else {
        return item;
      }
    })
    .filter(
      (item) =>
        item !== indexColumnNameConstants.STATUS &&
        item !== indexColumnNameConstants.ACTIONS &&
        item !== indexColumnNameConstants.ONBOARD_STATUS
    );

  return {
    columnDefinitions,
    columnDefinitionsForIpamDevices,
    columnDefinitionsForNcmDevices,
    columnDefinitionsForMonitoringDevices,
    dataKeys,
  };
}
