import React, { useEffect, useState } from "react";
import { Grid } from "@mui/material";
import { useSelector } from "react-redux";
import { selectTableData } from "../../../../store/features/ncmModule/manageConfigurations/configurationBackups/selectors";
import { selectSelectedDevice } from "../../../../store/features/ncmModule/manageConfigurations/selectors";
import {
  useFetchRecordsMutation,
  useBackupSingleNcmConfigurationByNcmDeviceIdMutation,
} from "../../../../store/features/ncmModule/manageConfigurations/configurationBackups/apis";
import { useAuthorization } from "../../../../hooks/useAuth";
import useErrorHandling, {
  TYPE_SINGLE,
  TYPE_FETCH,
} from "../../../../hooks/useErrorHandling";
import useColumnsGenerator from "../../../../hooks/useColumnsGenerator";
import useButtonsConfiguration from "../../../../hooks/useButtonsConfiguration";
import DefaultPageTableSection from "../../../../components/pageSections";
import DefaultTableConfigurations from "../../../../components/tableConfigurations";
import DefaultSpinner from "../../../../components/spinners";
import { TABLE_DATA_UNIQUE_ID as MANAGE_CONFIGURATIONS_TABLE_DATA_UNIQUE_ID } from "../../manageConfigurations/constants";
import CompareModal from "./compareModal";
import RestoreModal from "./restoreModal";
import BackupDetails from "./backupDetails";
import { useIndexTableColumnDefinitions } from "./columnDefinitions";
import { PAGE_NAME, PAGE_PATH, TABLE_DATA_UNIQUE_ID } from "./constants";
import { MODULE_PATH } from "../..";

const Index = () => {
  // hooks
  const { getUserInfoFromAccessToken, isPageEditable } = useAuthorization();

  // user information
  const userInfo = getUserInfoFromAccessToken();
  const roleConfigurations = userInfo?.configuration;

  // states
  const [pageEditable, setPageEditable] = useState(
    isPageEditable(roleConfigurations, MODULE_PATH, PAGE_PATH)
  );

  // hooks
  const { columnDefinitions } = useIndexTableColumnDefinitions();
  const generatedColumns = useColumnsGenerator({ columnDefinitions });
  const { buttonsConfigurationList } = useButtonsConfiguration({
    configure_table: { handleClick: handleTableConfigurationsOpen },
    default_restore: {
      handleClick: handleRestoreModalOpen,
    },
    default_backup: { handleClick: handleSingleBackup, visible: pageEditable },
    default_compare: { handleClick: handleCompareModalOpen },
  });

  // states
  const [compareModalOpen, setCompareModalOpen] = useState(false);
  const [restoreModalOpen, setRestoreModalOpen] = useState(false);
  const [tableConfigurationsOpen, setTableConfigurationsOpen] = useState(false);
  const [columns, setColumns] = useState(generatedColumns);
  const [availableColumns, setAvailableColumns] = useState([]);
  const [displayColumns, setDisplayColumns] = useState(generatedColumns);
  const [selectedRowKey, setSelectedRowKey] = useState(null);

  // selectors
  const dataSource = useSelector(selectTableData);
  const selectedDevice = useSelector(selectSelectedDevice);

  // apis
  const [
    fetchRecords,
    {
      data: fetchRecordsData,
      isSuccess: isFetchRecordsSuccess,
      isLoading: isFetchRecordsLoading,
      isError: isFetchRecordsError,
      error: fetchRecordsError,
    },
  ] = useFetchRecordsMutation();

  const [
    singleBackup,
    {
      data: singleBackupData,
      isSuccess: isSingleBackupSuccess,
      isLoading: isSingleBackupLoading,
      isError: isSingleBackupError,
      error: singleBackupError,
    },
  ] = useBackupSingleNcmConfigurationByNcmDeviceIdMutation();

  // error handling custom hooks
  useErrorHandling({
    data: fetchRecordsData,
    isSuccess: isFetchRecordsSuccess,
    isError: isFetchRecordsError,
    error: fetchRecordsError,
    type: TYPE_FETCH,
  });

  useErrorHandling({
    data: singleBackupData,
    isSuccess: isSingleBackupSuccess,
    isError: isSingleBackupError,
    error: singleBackupError,
    type: TYPE_SINGLE,
  });

  // effects
  useEffect(() => {
    if (selectedDevice) {
      fetchRecords({
        [MANAGE_CONFIGURATIONS_TABLE_DATA_UNIQUE_ID]:
          selectedDevice[MANAGE_CONFIGURATIONS_TABLE_DATA_UNIQUE_ID],
      });
    }
  }, []);

  // handlers
  function handleSingleBackup() {
    singleBackup({
      [MANAGE_CONFIGURATIONS_TABLE_DATA_UNIQUE_ID]:
        selectedDevice[MANAGE_CONFIGURATIONS_TABLE_DATA_UNIQUE_ID],
    });
  }

  function handleTableConfigurationsOpen() {
    setTableConfigurationsOpen(true);
  }

  function handleCompareModalOpen() {
    setCompareModalOpen(true);
  }

  function handleCompareModalClose() {
    setCompareModalOpen(false);
  }

  function handleRestoreModalOpen() {
    setRestoreModalOpen(true);
  }

  function handleRestoreModalClose() {
    setRestoreModalOpen(false);
  }

  return (
    <DefaultSpinner spinning={isFetchRecordsLoading || isSingleBackupLoading}>
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

      {compareModalOpen ? (
        <CompareModal
          handleClose={handleCompareModalClose}
          open={compareModalOpen}
          ncmDeviceId={selectedDevice?.ncm_device_id}
        />
      ) : null}

      {restoreModalOpen ? (
        <RestoreModal
          handleClose={handleRestoreModalClose}
          open={restoreModalOpen}
          ncmDeviceId={selectedDevice?.ncm_device_id}
          pageEditable={pageEditable}
        />
      ) : null}

      <Grid container spacing={1}>
        <Grid item xs={12}>
          <DefaultPageTableSection
            PAGE_NAME={PAGE_NAME}
            TABLE_DATA_UNIQUE_ID={TABLE_DATA_UNIQUE_ID}
            buttonsConfigurationList={buttonsConfigurationList}
            displayColumns={displayColumns}
            dataSource={dataSource}
            rowClickable={true}
            selectedRowKey={pageEditable ? selectedRowKey : null}
            setSelectedRowKey={setSelectedRowKey}
            dynamicWidth={false}
            scroll={false}
          />
        </Grid>
        <Grid item xs={12}>
          <BackupDetails
            ncmHistoryId={selectedRowKey}
            pageEditable={pageEditable}
          />
        </Grid>
      </Grid>
      <br />
    </DefaultSpinner>
  );
};

export default Index;
