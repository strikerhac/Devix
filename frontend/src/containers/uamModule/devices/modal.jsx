import React, { useState } from "react";
import { useSelector } from "react-redux";
import {
  selectSitesByIPAddressData,
  selectRacksByIPAddressData,
  selectBoardsByIPAddressData,
  selectSubBoardsByIPAddressData,
  selectSFPsByIPAddressData,
  selectLicensesByIPAddressData,
} from "../../../store/features/uamModule/devices/selectors";
import {
  useFetchSitesByIPAddressQuery,
  useFetchRacksByIPAddressQuery,
  useFetchBoardsByIPAddressQuery,
  useFetchSubBoardsByIPAddressQuery,
  useFetchSFPsByIPAddressQuery,
  useFetchLicensesByIPAddressQuery,
} from "../../../store/features/uamModule/devices/apis";
import useErrorHandling, { TYPE_FETCH } from "../../../hooks/useErrorHandling";
import useButtonsConfiguration from "../../../hooks/useButtonsConfiguration";
import useColumnsGenerator from "../../../hooks/useColumnsGenerator";
import DefaultTableConfigurations from "../../../components/tableConfigurations";
import { DeviceDetailsDialogFooter } from "../../../components/dialogFooters";
import { PageTableSectionWithCustomPageHeader } from "../../../components/pageSections";
import DetailsModal from "../../../components/dialogs";
import DefaultSpinner from "../../../components/spinners";
import { useIndexTableColumnDefinitions as useSitesTableColumnDefinitions } from "../sites/columnDefinitions";
import { useIndexTableColumnDefinitions as useRacksTableColumnDefinitions } from "../racks/columnDefinitions";
import { useIndexTableColumnDefinitions as useBoardsTableColumnDefinitions } from "../boards/columnDefinitions";
import { useIndexTableColumnDefinitions as useSubBoardsTableColumnDefinitions } from "../subBoards/columnDefinitions";
import { useIndexTableColumnDefinitions as useSFPsTableColumnDefinitions } from "../sfps/columnDefinitions";
import { useIndexTableColumnDefinitions as useLicensesTableColumnDefinitions } from "../licenses/columnDefinitions";
import { TABLE_DATA_UNIQUE_ID as SITE_ID } from "../sites/constants";
import { CustomPageHeader } from "./customPageHeader";
import { indexColumnNameConstants } from "./constants";
import { ELEMENT_NAME } from "./constants";

const Index = ({ handleClose, open, record }) => {
  const parameters = {
    [indexColumnNameConstants.IP_ADDRESS]:
      record[indexColumnNameConstants.IP_ADDRESS],
  };

  // hooks
  const { plainColumnDefinitions: plainSitesColumnDefinitions } =
    useSitesTableColumnDefinitions();
  const { plainColumnDefinitions: plainRacksColumnDefinitions } =
    useRacksTableColumnDefinitions();
  const { plainColumnDefinitions: plainBoardsColumnDefinitions } =
    useBoardsTableColumnDefinitions();
  const { plainColumnDefinitions: plainSubBoardsColumnDefinitions } =
    useSubBoardsTableColumnDefinitions();
  const { plainColumnDefinitions: plainSFPsColumnDefinitions } =
    useSFPsTableColumnDefinitions();
  const { plainColumnDefinitions: plainLicensesColumnDefinitions } =
    useLicensesTableColumnDefinitions();

  const generatedSitesColumns = useColumnsGenerator({
    columnDefinitions: plainSitesColumnDefinitions,
  });
  const generatedRacksColumns = useColumnsGenerator({
    columnDefinitions: plainRacksColumnDefinitions,
  });
  const generatedBoardsColumns = useColumnsGenerator({
    columnDefinitions: plainBoardsColumnDefinitions,
  });
  const generatedSubBoardsColumns = useColumnsGenerator({
    columnDefinitions: plainSubBoardsColumnDefinitions,
  });
  const generatedSFPsColumns = useColumnsGenerator({
    columnDefinitions: plainSFPsColumnDefinitions,
  });
  const generatedLicensesColumns = useColumnsGenerator({
    columnDefinitions: plainLicensesColumnDefinitions,
  });

  const { buttonsConfigurationObject } = useButtonsConfiguration({
    configure_table: { handleClick: handleTableConfigurationsOpen },
  });

  // fetch apis
  const {
    data: fetchSitesByIPAddressRecordsData,
    isSuccess: isFetchSitesByIPAddressRecordsSuccess,
    isLoading: isFetchSitesByIPAddressRecordsLoading,
    isError: isFetchSitesByIPAddressRecordsError,
    error: fetchSitesByIPAddressRecordsError,
  } = useFetchSitesByIPAddressQuery(parameters);

  const {
    data: fetchRacksByIPAddressRecordsData,
    isSuccess: isFetchRacksByIPAddressRecordsSuccess,
    isLoading: isFetchRacksByIPAddressRecordsLoading,
    isError: isFetchRacksByIPAddressRecordsError,
    error: fetchRacksByIPAddressRecordsError,
  } = useFetchRacksByIPAddressQuery(parameters);

  const {
    data: fetchBoardsByIPAddressRecordsData,
    isSuccess: isFetchBoardsByIPAddressRecordsSuccess,
    isLoading: isFetchBoardsByIPAddressRecordsLoading,
    isError: isFetchBoardsByIPAddressRecordsError,
    error: fetchBoardsByIPAddressRecordsError,
  } = useFetchBoardsByIPAddressQuery(parameters);

  const {
    data: fetchSubBoardsByIPAddressRecordsData,
    isSuccess: isFetchSubBoardsByIPAddressRecordsSuccess,
    isLoading: isFetchSubBoardsByIPAddressRecordsLoading,
    isError: isFetchSubBoardsByIPAddressRecordsError,
    error: fetchSubBoardsByIPAddressRecordsError,
  } = useFetchSubBoardsByIPAddressQuery(parameters);

  const {
    data: fetchSFPsByIPAddressRecordsData,
    isSuccess: isFetchSFPsByIPAddressRecordsSuccess,
    isLoading: isFetchSFPsByIPAddressRecordsLoading,
    isError: isFetchSFPsByIPAddressRecordsError,
    error: fetchSFPsByIPAddressRecordsError,
  } = useFetchSFPsByIPAddressQuery(parameters);

  const {
    data: fetchLicensesByIPAddressRecordsData,
    isSuccess: isFetchLicensesByIPAddressRecordsSuccess,
    isLoading: isFetchLicensesByIPAddressRecordsLoading,
    isError: isFetchLicensesByIPAddressRecordsError,
    error: fetchLicensesByIPAddressRecordsError,
  } = useFetchLicensesByIPAddressQuery(parameters);

  // error handling custom hooks
  useErrorHandling({
    data: fetchSitesByIPAddressRecordsData,
    isSuccess: isFetchSitesByIPAddressRecordsSuccess,
    isError: isFetchSitesByIPAddressRecordsError,
    error: fetchSitesByIPAddressRecordsError,
    type: TYPE_FETCH,
  });

  useErrorHandling({
    data: fetchRacksByIPAddressRecordsData,
    isSuccess: isFetchRacksByIPAddressRecordsSuccess,
    isError: isFetchRacksByIPAddressRecordsError,
    error: fetchRacksByIPAddressRecordsError,
    type: TYPE_FETCH,
  });

  useErrorHandling({
    data: fetchBoardsByIPAddressRecordsData,
    isSuccess: isFetchBoardsByIPAddressRecordsSuccess,
    isError: isFetchBoardsByIPAddressRecordsError,
    error: fetchBoardsByIPAddressRecordsError,
    type: TYPE_FETCH,
  });

  useErrorHandling({
    data: fetchSubBoardsByIPAddressRecordsData,
    isSuccess: isFetchSubBoardsByIPAddressRecordsSuccess,
    isError: isFetchSubBoardsByIPAddressRecordsError,
    error: fetchSubBoardsByIPAddressRecordsError,
    type: TYPE_FETCH,
  });

  useErrorHandling({
    data: fetchSFPsByIPAddressRecordsData,
    isSuccess: isFetchSFPsByIPAddressRecordsSuccess,
    isError: isFetchSFPsByIPAddressRecordsError,
    error: fetchSFPsByIPAddressRecordsError,
    type: TYPE_FETCH,
  });

  useErrorHandling({
    data: fetchLicensesByIPAddressRecordsData,
    isSuccess: isFetchLicensesByIPAddressRecordsSuccess,
    isError: isFetchLicensesByIPAddressRecordsError,
    error: fetchLicensesByIPAddressRecordsError,
    type: TYPE_FETCH,
  });

  // getting tables data from the store
  const sitesByIPAddressData = useSelector(selectSitesByIPAddressData);
  const racksByIPAddressData = useSelector(selectRacksByIPAddressData);
  const boardsByIPAddressData = useSelector(selectBoardsByIPAddressData);
  const subBoardsByIPAddressData = useSelector(selectSubBoardsByIPAddressData);
  const sfpsByIPAddressData = useSelector(selectSFPsByIPAddressData);
  const licensesByIPAddressData = useSelector(selectLicensesByIPAddressData);

  // states
  const [selectedTableId, setSelectedTableId] = useState(SITE_ID);
  const [selectedTableData, setSelectedTableData] =
    useState(sitesByIPAddressData);
  const [tableConfigurationsOpen, setTableConfigurationsOpen] = useState(false);
  const [columns, setColumns] = useState(generatedSitesColumns);
  const [availableColumns, setAvailableColumns] = useState([]);
  const [displayColumns, setDisplayColumns] = useState(generatedSitesColumns);

  // handlers
  function handleTableConfigurationsOpen() {
    setTableConfigurationsOpen(true);
  }

  return (
    <DetailsModal title={`${ELEMENT_NAME} Details`} open={open}>
      <DefaultSpinner
        spinning={
          isFetchSitesByIPAddressRecordsLoading ||
          isFetchRacksByIPAddressRecordsLoading ||
          isFetchBoardsByIPAddressRecordsLoading ||
          isFetchSubBoardsByIPAddressRecordsLoading ||
          isFetchSFPsByIPAddressRecordsLoading ||
          isFetchLicensesByIPAddressRecordsLoading
        }
      >
        {tableConfigurationsOpen ? (
          <DefaultTableConfigurations
            columns={columns}
            availableColumns={availableColumns}
            setAvailableColumns={setAvailableColumns}
            displayColumns={displayColumns}
            setDisplayColumns={setDisplayColumns}
            setColumns={setColumns}
            open={tableConfigurationsOpen}
            setOpen={setTableConfigurationsOpen}
          />
        ) : null}

        <PageTableSectionWithCustomPageHeader
          customPageHeader={
            <CustomPageHeader
              selectedTableId={selectedTableId}
              setSelectedTableId={setSelectedTableId}
              setSelectedTableData={setSelectedTableData}
              setColumns={setColumns}
              setAvailableColumns={setAvailableColumns}
              setDisplayColumns={setDisplayColumns}
              buttons={buttonsConfigurationObject}
              sitesByIPAddressData={sitesByIPAddressData}
              generatedSitesColumns={generatedSitesColumns}
              racksByIPAddressData={racksByIPAddressData}
              generatedRacksColumns={generatedRacksColumns}
              boardsByIPAddressData={boardsByIPAddressData}
              generatedBoardsColumns={generatedBoardsColumns}
              subBoardsByIPAddressData={subBoardsByIPAddressData}
              generatedSubBoardsColumns={generatedSubBoardsColumns}
              sfpsByIPAddressData={sfpsByIPAddressData}
              generatedSFPsColumns={generatedSFPsColumns}
              licensesByIPAddressData={licensesByIPAddressData}
              generatedLicensesColumns={generatedLicensesColumns}
            />
          }
          TABLE_DATA_UNIQUE_ID={selectedTableId}
          displayColumns={displayColumns}
          dataSource={selectedTableData}
        />
        <br />
        <DeviceDetailsDialogFooter handleClose={handleClose} />
      </DefaultSpinner>
    </DetailsModal>
  );
};

export default Index;
