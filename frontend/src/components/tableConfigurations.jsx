import React, { useState } from "react";
import { Button, List, ListItem, Divider } from "@mui/material";
import DefaultDialog from "./dialogs";
import { TableConfigurationDialogFooter } from "./dialogFooters";
import { useTheme, styled } from "@mui/material/styles";
import DefaultScrollbar from "./scrollbar";
import DefaultButton from "./buttons";
import { Icon } from "@iconify/react";

export default function DefaultTableConfigurations({
  columns,
  availableColumns,
  setAvailableColumns,
  displayColumns,
  setDisplayColumns,
  open,
  setOpen,
  sx,
  children,
  ...rest
}) {
  const theme = useTheme();
  const [selectedColumn, setSelectedColumn] = useState(null);
  const [
    isSelectedColumnFromAvailableColumns,
    setIsSelectedColumnFromAvailableColumns,
  ] = useState(false);
  const [
    isSelectedColumnFromDisplayColumns,
    setIsSelectedColumnFromDisplayColumns,
  ] = useState(false);
  const [tempAvailableColumns, setTempAvailableColumns] =
    useState(availableColumns);
  const [tempDisplayColumns, setTempDisplayColumns] = useState(displayColumns);

  const StyledListItem = styled(ListItem)(({ theme, selectedItem }) => ({
    color: `${
      selectedItem
        ? theme?.palette?.default_table_Configurations?.item_select_text
        : theme?.palette?.default_table_Configurations?.primary_text
    }`,
    backgroundColor: `${
      selectedItem
        ? theme?.palette?.default_table_Configurations?.item_select_background
        : "transparent"
    }`,
    "&:hover": {
      color: "white",
      backgroundColor: "silver !important",
    },
  }));

  const handleCancel = () => {
    setTempAvailableColumns(availableColumns);
    setTempDisplayColumns(displayColumns);
    setOpen(false);
  };

  const handleReset = () => {
    setTempAvailableColumns([]);
    setTempDisplayColumns(columns);
  };

  const handleSave = () => {
    setAvailableColumns(tempAvailableColumns);
    setDisplayColumns(tempDisplayColumns);
    setOpen(false);
  };

  const handleAdd = () => {
    setTempAvailableColumns((prev) =>
      prev.filter((item) => item.dataIndex !== selectedColumn.dataIndex)
    );
    setTempDisplayColumns((prev) => [...prev, selectedColumn]);
    setSelectedColumn(null);
    setIsSelectedColumnFromDisplayColumns(false);
    setIsSelectedColumnFromAvailableColumns(false);
  };

  const handleRemove = () => {
    setTempDisplayColumns((prev) =>
      prev.filter((item) => item.dataIndex !== selectedColumn.dataIndex)
    );
    setTempAvailableColumns((prev) => [...prev, selectedColumn]);
    setIsSelectedColumnFromDisplayColumns(false);
    setIsSelectedColumnFromAvailableColumns(false);
  };

  const handleUp = () => {
    if (selectedColumn) {
      const index = tempDisplayColumns.indexOf(selectedColumn);
      if (index > 0) {
        const updatedDisplayColumns = [...tempDisplayColumns];
        [updatedDisplayColumns[index], updatedDisplayColumns[index - 1]] = [
          updatedDisplayColumns[index - 1],
          updatedDisplayColumns[index],
        ];
        setTempDisplayColumns(updatedDisplayColumns);
      }
    }
  };

  const handleDown = () => {
    if (selectedColumn) {
      const index = tempDisplayColumns.indexOf(selectedColumn);
      if (index < tempDisplayColumns.length - 1) {
        const updatedDisplayColumns = [...tempDisplayColumns];
        [updatedDisplayColumns[index], updatedDisplayColumns[index + 1]] = [
          updatedDisplayColumns[index + 1],
          updatedDisplayColumns[index],
        ];
        setTempDisplayColumns(updatedDisplayColumns);
      }
    }
  };

  const handleColumnClick = (column, type) => {
    setSelectedColumn(column);

    if (type === "display") {
      setIsSelectedColumnFromDisplayColumns(true);
      setIsSelectedColumnFromAvailableColumns(false);
    } else {
      setIsSelectedColumnFromDisplayColumns(false);
      setIsSelectedColumnFromAvailableColumns(true);
    }
  };

  return (
    <DefaultDialog title="Configure Table" open={open} sx={sx} {...rest}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          width: "700px",
        }}
      >
        <div style={{ textAlign: "center" }}>
          <p>
            <strong style={{ color: "grey" }}>Available Columns</strong>
          </p>
          <DefaultScrollbar
            sx={{
              height: "400px",
              width: "250px",
              overflow: "scroll",
            }}
          >
            <List>
              {tempAvailableColumns.map((column, index) => (
                <StyledListItem
                  key={index}
                  onClick={() => handleColumnClick(column, "available")}
                  selectedItem={
                    isSelectedColumnFromAvailableColumns &&
                    selectedColumn.dataIndex === column.dataIndex
                  }
                >
                  {column.title}
                </StyledListItem>
              ))}
            </List>
          </DefaultScrollbar>
        </div>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            height: "400px",
          }}
        >
          <div>
            <DefaultButton
              sx={{
                backgroundColor:
                  theme?.palette?.default_button?.right_background,
                color: theme?.palette?.default_button?.secondary_text,
                width: "100%",
                fontSize: "12px",
              }}
              handleClick={handleAdd}
              disabled={!isSelectedColumnFromAvailableColumns}
            >
              <Icon fontSize="16px" icon="icon-park-outline:right-two" />
              Add
            </DefaultButton>
            <br />
            <DefaultButton
              sx={{
                backgroundColor:
                  theme?.palette?.default_button?.left_background,
                color: theme?.palette?.default_button?.secondary_text,
                width: "100%",
                fontSize: "12px",
              }}
              handleClick={handleRemove}
              disabled={!isSelectedColumnFromDisplayColumns}
            >
              <Icon fontSize="16px" icon="icon-park-outline:left-two" />
              Remove
            </DefaultButton>
            <br />
            <DefaultButton
              sx={{
                backgroundColor: theme?.palette?.default_button?.up_background,
                color: theme?.palette?.default_button?.secondary_text,
                width: "100%",
                fontSize: "12px",
              }}
              handleClick={handleUp}
              disabled={!isSelectedColumnFromDisplayColumns}
            >
              <Icon fontSize="16px" icon="icon-park-outline:up-two" />
              Up
            </DefaultButton>
            <br />
            <DefaultButton
              sx={{
                backgroundColor:
                  theme?.palette?.default_button?.down_background,
                color: theme?.palette?.default_button?.secondary_text,
                width: "100%",
                fontSize: "12px",
              }}
              handleClick={handleDown}
              disabled={!isSelectedColumnFromDisplayColumns}
            >
              <Icon fontSize="16px" icon="icon-park-outline:down-two" />
              Down
            </DefaultButton>
          </div>
        </div>
        <div style={{ textAlign: "center" }}>
          <p>
            <strong style={{ color: "grey" }}>Display Columns</strong>
          </p>
          <DefaultScrollbar
            sx={{
              height: "400px",
              width: "250px",
              overflow: "scroll",
            }}
          >
            <List>
              {tempDisplayColumns.map((column, index) => {
                if (!column.hasOwnProperty("fixed"))
                  return (
                    <StyledListItem
                      key={index}
                      onClick={() => handleColumnClick(column, "display")}
                      selectedItem={
                        isSelectedColumnFromDisplayColumns &&
                        selectedColumn.dataIndex === column.dataIndex
                      }
                    >
                      {column.title}
                    </StyledListItem>
                  );
              })}
            </List>
          </DefaultScrollbar>
        </div>
      </div>
      <br />
      <TableConfigurationDialogFooter
        handleClose={handleCancel}
        handleReset={handleReset}
        handleSave={handleSave}
      />
    </DefaultDialog>
  );
}
