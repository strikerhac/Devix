import React from "react";
import { useTheme } from "@mui/material/styles";
import { Icon } from "@iconify/react";
import Tooltip from "@mui/material/Tooltip";

export const ACTIONS = "actions";

export default function useTableActions({ actions, ...rest }) {
  const theme = useTheme();
  const width = 90 + (actions.length - 1) * 20;
  return {
    data_key: ACTIONS,
    search: false,
    fixed: "right",
    align: "center",
    width,
    render: (text, record) => (
      <div
        style={{
          display: "flex",
          gap: "10px",
          justifyContent: "center",
        }}
      >
        {actions.map((item) => {
          const { title, icon, handler } = item;
          return (
            <Tooltip title={title}>
              <Icon
                icon={icon}
                fontSize={"15px"}
                style={{ cursor: "pointer" }}
                onClick={() => handler(record)}
              />
            </Tooltip>
          );
        })}
      </div>
    ),
    ...rest,
  };
}
