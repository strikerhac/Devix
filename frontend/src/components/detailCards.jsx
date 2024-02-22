import React from "react";
import { useTheme } from "@mui/material/styles";
import DefaultCard from "./cards";
import { getTitle } from "../utils/helpers";
import { Icon } from "@iconify/react";

export default function DefaultDetailCards({ data, icons = [], ...rest }) {
  const theme = useTheme();

  return (
    <DefaultCard
      sx={{
        marginBottom: "10px",
      }}
      {...rest}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          padding: "10px",
          height: "90px",
        }}
      >
        {Object.keys(data)?.map((key, index) => {
          // increase the space factor to increase the space between cards
          const spaceFactor = 3;
          const length = Object.keys(data).length;
          const widthToBeDivided = 100 - (length * spaceFactor) / 5;
          const width = widthToBeDivided / length;
          return (
            <div
              style={{
                borderRadius: "7px",
                width: `${width}%`,
                backgroundColor: "#F6F6F6",
              }}
            >
              <div
                style={{
                  margin: "16px",
                  display: "flex",
                  justifyContent: "space-between",
                  height: "57px",
                }}
              >
                <div>
                  <div
                    style={{
                      fontSize: "14px",
                    }}
                  >
                    {getTitle(key)}
                  </div>
                  <div
                    style={{
                      color: "green",
                      fontWeight: "bolder",
                      fontSize: "17px",
                      marginTop: "10px",
                    }}
                  >
                    {data[key]}
                  </div>
                </div>
                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center",
                  }}
                >
                  <div
                    style={{
                      padding: "6px 6px 2px 6px",
                      borderRadius: "5px",
                      backgroundColor: "white",
                    }}
                  >
                    <Icon
                      style={{ color: "green" }}
                      fontSize={"30px"}
                      icon={icons[index] ? icons[index] : null}
                    />
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </DefaultCard>
  );
}
