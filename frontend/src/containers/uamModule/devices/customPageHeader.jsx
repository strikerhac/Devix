import React from "react";
import { useTheme, styled } from "@mui/material/styles";
import useButtonGenerator from "../../../hooks/useButtonGenerator";
import { TABLE_DATA_UNIQUE_ID as SITE_ID } from "../sites/constants";
import { TABLE_DATA_UNIQUE_ID as RACK_ID } from "../racks/constants";
import { TABLE_DATA_UNIQUE_ID as BOARD_ID } from "../boards/constants";
import { TABLE_DATA_UNIQUE_ID as SUB_BOARD_ID } from "../subBoards/constants";
import { TABLE_DATA_UNIQUE_ID as SFP_ID } from "../sfps/constants";
import { TABLE_DATA_UNIQUE_ID as LICENSE_ID } from "../licenses/constants";

export function CustomPageHeader({
  selectedTableId,
  setSelectedTableId,
  setSelectedTableData,
  setColumns,
  setAvailableColumns,
  setDisplayColumns,
  buttons,
  sitesByIPAddressData,
  generatedSitesColumns,
  racksByIPAddressData,
  generatedRacksColumns,
  boardsByIPAddressData,
  generatedBoardsColumns,
  subBoardsByIPAddressData,
  generatedSubBoardsColumns,
  sfpsByIPAddressData,
  generatedSFPsColumns,
  licensesByIPAddressData,
  generatedLicensesColumns,
}) {
  const theme = useTheme();
  const buttonGenerator = useButtonGenerator();

  const StyledSpan = styled("span")(({ theme, sx = {}, id }) => ({
    cursor: "pointer",
    color: selectedTableId === id ? "green" : "black",
    textDecoration: selectedTableId === id ? "underline" : "none",
    "&:hover": {
      color: "green",
      textDecoration: "underline",
    },
    ...sx,
  }));

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        marginTop: "10px",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          width: "50%",
        }}
      >
        <StyledSpan
          id={SITE_ID}
          onClick={() => {
            setSelectedTableId(SITE_ID);
            setSelectedTableData(sitesByIPAddressData);
            setColumns(generatedSitesColumns);
            setAvailableColumns([]);
            setDisplayColumns(generatedSitesColumns);
          }}
        >
          Sites
        </StyledSpan>
        <StyledSpan
          id={RACK_ID}
          onClick={() => {
            setSelectedTableId(RACK_ID);
            setSelectedTableData(racksByIPAddressData);
            setColumns(generatedRacksColumns);
            setAvailableColumns([]);
            setDisplayColumns(generatedRacksColumns);
          }}
        >
          Racks
        </StyledSpan>
        <StyledSpan
          id={BOARD_ID}
          onClick={() => {
            setSelectedTableId(BOARD_ID);
            setSelectedTableData(boardsByIPAddressData);
            setColumns(generatedBoardsColumns);
            setAvailableColumns([]);
            setDisplayColumns(generatedBoardsColumns);
          }}
        >
          Boards
        </StyledSpan>
        <StyledSpan
          id={SUB_BOARD_ID}
          onClick={() => {
            setSelectedTableId(SUB_BOARD_ID);
            setSelectedTableData(subBoardsByIPAddressData);
            setColumns(generatedSubBoardsColumns);
            setAvailableColumns([]);
            setDisplayColumns(generatedSubBoardsColumns);
          }}
        >
          SubBoards
        </StyledSpan>
        <StyledSpan
          id={SFP_ID}
          onClick={() => {
            setSelectedTableId(SFP_ID);
            setSelectedTableData(sfpsByIPAddressData);
            setColumns(generatedSFPsColumns);
            setAvailableColumns([]);
            setDisplayColumns(generatedSFPsColumns);
          }}
        >
          SFPs
        </StyledSpan>
        <StyledSpan
          id={LICENSE_ID}
          onClick={() => {
            setSelectedTableId(LICENSE_ID);
            setSelectedTableData(licensesByIPAddressData);
            setColumns(generatedLicensesColumns);
            setAvailableColumns([]);
            setDisplayColumns(generatedLicensesColumns);
          }}
        >
          Licenses
        </StyledSpan>
      </div>
      <div>{buttonGenerator(buttons.configure_table)}</div>
    </div>
  );
}
