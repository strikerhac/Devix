import React, { useState } from "react";
import { useSelector } from "react-redux";
import { selectTableData } from "../../../store/features/uamModule/devices/selectors";
import {
  useFetchRecordsQuery,
  useDismantleRecordsMutation,
} from "../../../store/features/uamModule/devices/apis";
import { jsonToExcel } from "../../../utils/helpers";
import {
  DISMANTLE_PROMPT,
  DISMANTLE_SELECTION_PROMPT,
  SUCCESSFUL_FILE_EXPORT_MESSAGE,
} from "../../../utils/constants";
import { useAuthorization } from "../../../hooks/useAuth";
import useErrorHandling, {
  TYPE_FETCH,
  TYPE_BULK,
  TYPE_BULK_DISMANTLE,
} from "../../../hooks/useErrorHandling";
import useSweetAlert from "../../../hooks/useSweetAlert";
import useColumnsGenerator from "../../../hooks/useColumnsGenerator";
import useButtonsConfiguration from "../../../hooks/useButtonsConfiguration";
import DefaultTableConfigurations from "../../../components/tableConfigurations";
import DefaultPageTableSection from "../../../components/pageSections";
import DefaultSpinner from "../../../components/spinners";
import DetailsByIPAdressModal from "./modal";
import { useIndexTableColumnDefinitions } from "./columnDefinitions";
import {
  PAGE_NAME,
  PAGE_PATH,
  FILE_NAME_EXPORT_ALL_DATA,
  TABLE_DATA_UNIQUE_ID,
} from "./constants";
import { MODULE_PATH } from "..";

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
  const [selectedRowKeys, setSelectedRowKeys] = useState([]);

  // hooks
  const { handleCallbackAlert, handleSuccessAlert, handleInfoAlert } =
    useSweetAlert();
  const { columnDefinitions } = useIndexTableColumnDefinitions({
    handleIpAddressClick,
  });
  const generatedColumns = useColumnsGenerator({ columnDefinitions });
  const { buttonsConfigurationList } = useButtonsConfiguration({
    configure_table: { handleClick: handleTableConfigurationsOpen },
    default_export: { handleClick: handleDefaultExport },
    default_dismantle: {
      handleClick: handleDismantle,
      visible: selectedRowKeys.length > 0 && pageEditable,
    },
  });

  // states
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [openDetailsByIPAddressModal, setOpenDetailsByIPAddressModal] =
    useState(false);
  const [tableConfigurationsOpen, setTableConfigurationsOpen] = useState(false);
  const [columns, setColumns] = useState(generatedColumns);
  const [availableColumns, setAvailableColumns] = useState([]);
  const [displayColumns, setDisplayColumns] = useState(generatedColumns);

  // selectors
  const dataSource = useSelector(selectTableData);

  // apis
  const {
    data: fetchRecordsData,
    isSuccess: isFetchRecordsSuccess,
    isLoading: isFetchRecordsLoading,
    isError: isFetchRecordsError,
    error: fetchRecordsError,
  } = useFetchRecordsQuery();

  const [
    dismantleRecords,
    {
      data: dismantleRecordsData,
      isSuccess: isDismantleRecordsSuccess,
      isLoading: isDismantleRecordsLoading,
      isError: isDismantleRecordsError,
      error: dismantleRecordsError,
    },
  ] = useDismantleRecordsMutation();

  // error handling custom hooks
  useErrorHandling({
    data: fetchRecordsData,
    isSuccess: isFetchRecordsSuccess,
    isError: isFetchRecordsError,
    error: fetchRecordsError,
    type: TYPE_FETCH,
  });

  useErrorHandling({
    data: dismantleRecordsData,
    isSuccess: isDismantleRecordsSuccess,
    isError: isDismantleRecordsError,
    error: dismantleRecordsError,
    type: TYPE_BULK_DISMANTLE,
    callback: handleEmptySelectedRowKeys,
  });

  // handlers
  function handleIpAddressClick(record) {
    setSelectedRecord(record);
    setOpenDetailsByIPAddressModal(true);
  }

  function handleDetailsByIPAddressModalClose() {
    setOpenDetailsByIPAddressModal(false);
  }

  function handleEmptySelectedRowKeys() {
    setSelectedRowKeys([]);
  }

  function dismantleData(allowed) {
    if (allowed) {
      dismantleRecords(selectedRowKeys);
    } else {
      setSelectedRowKeys([]);
    }
  }

  function handleDismantle() {
    if (selectedRowKeys.length > 0) {
      handleCallbackAlert(DISMANTLE_PROMPT, dismantleData);
    } else {
      handleInfoAlert(DISMANTLE_SELECTION_PROMPT);
    }
  }

  function handleDefaultExport() {
    if (dataSource?.length > 0) {
      jsonToExcel(dataSource, FILE_NAME_EXPORT_ALL_DATA);
      handleSuccessAlert(SUCCESSFUL_FILE_EXPORT_MESSAGE);
    } else {
      handleInfoAlert("No data to export.");
    }
  }

  function handleTableConfigurationsOpen() {
    setTableConfigurationsOpen(true);
  }

  return (
    <DefaultSpinner spinning={isFetchRecordsLoading}>
      {openDetailsByIPAddressModal ? (
        <DetailsByIPAdressModal
          handleClose={handleDetailsByIPAddressModalClose}
          open={openDetailsByIPAddressModal}
          record={selectedRecord}
        />
      ) : null}

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

      <DefaultPageTableSection
        PAGE_NAME={PAGE_NAME}
        TABLE_DATA_UNIQUE_ID={TABLE_DATA_UNIQUE_ID}
        buttonsConfigurationList={buttonsConfigurationList}
        displayColumns={displayColumns}
        dataSource={dataSource}
        selectedRowKeys={pageEditable ? selectedRowKeys : null}
        setSelectedRowKeys={setSelectedRowKeys}
      />
    </DefaultSpinner>
  );
};

export default Index;
