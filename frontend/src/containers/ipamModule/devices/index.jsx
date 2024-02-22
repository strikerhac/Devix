import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { selectTableData } from "../../../store/features/ipamModule/devices/selectors";
import { useFetchIpamDevicesFetchDatesLazyQuery } from "../../../store/features/dropDowns/apis";
import {
  useFetchRecordsQuery,
  useFetchIpamDevicesLazyQuery,
  useGetIpamDevicesByFetchDateMutation,
  useDeleteRecordsMutation,
} from "../../../store/features/ipamModule/devices/apis";
import { jsonToExcel } from "../../../utils/helpers";
import {
  DELETE_PROMPT,
  DELETE_SELECTION_PROMPT,
  SUCCESSFUL_FILE_EXPORT_MESSAGE,
} from "../../../utils/constants";
import { useAuthorization } from "../../../hooks/useAuth";
import useErrorHandling, {
  TYPE_FETCH,
  TYPE_BULK_FETCH,
  TYPE_BULK_DELETE,
} from "../../../hooks/useErrorHandling";
import useButtonsConfiguration from "../../../hooks/useButtonsConfiguration";
import useSweetAlert from "../../../hooks/useSweetAlert";
import useColumnsGenerator from "../../../hooks/useColumnsGenerator";
import { PageTableSectionWithCustomPageHeader } from "../../../components/pageSections";
import DefaultTableConfigurations from "../../../components/tableConfigurations";
import DefaultSpinner from "../../../components/spinners";
import Modal from "./modal";
import { useIndexTableColumnDefinitions } from "./columnDefinitions";
import CustomPageHeader from "./customPageHeader";
import {
  PAGE_NAME,
  ELEMENT_NAME,
  FILE_NAME_EXPORT_ALL_DATA,
  TABLE_DATA_UNIQUE_ID,
  PAGE_PATH,
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
  const { handleSuccessAlert, handleInfoAlert, handleCallbackAlert } =
    useSweetAlert();
  const { columnDefinitions } = useIndexTableColumnDefinitions();
  const generatedColumns = useColumnsGenerator({ columnDefinitions });
  const { buttonsConfigurationList } = useButtonsConfiguration({
    configure_table: { handleClick: handleTableConfigurationsOpen },
    default_export: { handleClick: handleDefaultExport },
    default_delete: {
      handleClick: handleDelete,
      visible: selectedRowKeys.length > 0 && pageEditable,
    },
    default_fetch: { handleClick: handleFetch, visible: pageEditable },
    default_add: {
      handleClick: handleAdd,
      namePostfix: ELEMENT_NAME,
      visible: pageEditable,
    },
  });

  // states
  const [open, setOpen] = useState(false);
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
    fetchIpamDevices,
    {
      data: fetchIpamDevicesData,
      isSuccess: isFetchIpamDevicesSuccess,
      isLoading: isFetchIpamDevicesLoading,
      isError: isFetchIpamDevicesError,
      error: fetchIpamDevicesError,
    },
  ] = useFetchIpamDevicesLazyQuery();

  const [
    getIpamDevicesFetchDates,
    {
      data: getIpamDevicesFetchDatesData,
      isSuccess: isGetIpamDevicesFetchDatesSuccess,
      isLoading: isGetIpamDevicesFetchDatesLoading,
      isError: isGetIpamDevicesFetchDatesError,
      error: getIpamDevicesFetchDatesError,
    },
  ] = useFetchIpamDevicesFetchDatesLazyQuery();

  const [
    getIpamDevicesByFetchDate,
    {
      data: getIpamDevicesByFetchDateData,
      isSuccess: isGetIpamDevicesByFetchDateSuccess,
      isLoading: isGetIpamDevicesByFetchDateLoading,
      isError: isGetIpamDevicesByFetchDateError,
      error: getIpamDevicesByFetchDateError,
    },
  ] = useGetIpamDevicesByFetchDateMutation();

  const [
    deleteRecords,
    {
      data: deleteRecordsData,
      isSuccess: isDeleteRecordsSuccess,
      isLoading: isDeleteRecordsLoading,
      isError: isDeleteRecordsError,
      error: deleteRecordsError,
    },
  ] = useDeleteRecordsMutation();

  // error handling custom hooks
  useErrorHandling({
    data: fetchRecordsData,
    isSuccess: isFetchRecordsSuccess,
    isError: isFetchRecordsError,
    error: fetchRecordsError,
    type: TYPE_FETCH,
  });

  useErrorHandling({
    data: fetchIpamDevicesData,
    isSuccess: isFetchIpamDevicesSuccess,
    isError: isFetchIpamDevicesError,
    error: fetchIpamDevicesError,
    type: TYPE_BULK_FETCH,
  });

  useErrorHandling({
    data: getIpamDevicesFetchDatesData,
    isSuccess: isGetIpamDevicesFetchDatesSuccess,
    isError: isGetIpamDevicesFetchDatesError,
    error: getIpamDevicesFetchDatesError,
    type: TYPE_FETCH,
  });

  useErrorHandling({
    data: getIpamDevicesByFetchDateData,
    isSuccess: isGetIpamDevicesByFetchDateSuccess,
    isError: isGetIpamDevicesByFetchDateError,
    error: getIpamDevicesByFetchDateError,
    type: TYPE_BULK_FETCH,
  });

  useErrorHandling({
    data: deleteRecordsData,
    isSuccess: isDeleteRecordsSuccess,
    isError: isDeleteRecordsError,
    error: deleteRecordsError,
    type: TYPE_BULK_DELETE,
    callback: handleEmptySelectedRowKeys,
  });

  // effects
  useEffect(() => {
    getIpamDevicesFetchDates();
  }, [isFetchIpamDevicesSuccess]);

  // handlers
  function handleEmptySelectedRowKeys() {
    setSelectedRowKeys([]);
  }

  function deleteData(allowed) {
    if (allowed) {
      deleteRecords(selectedRowKeys);
    } else {
      setSelectedRowKeys([]);
    }
  }

  function handleDelete() {
    if (selectedRowKeys.length > 0) {
      handleCallbackAlert(DELETE_PROMPT, deleteData);
    } else {
      handleInfoAlert(DELETE_SELECTION_PROMPT);
    }
  }

  function handleFetch() {
    fetchIpamDevices();
  }

  function handleAdd() {
    setOpen(true);
  }

  function handleClose() {
    setOpen(false);
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

  function handleDateChange(date) {
    getIpamDevicesByFetchDate({ date });
  }

  return (
    <DefaultSpinner
      spinning={
        isFetchRecordsLoading ||
        isFetchIpamDevicesLoading ||
        isGetIpamDevicesFetchDatesLoading ||
        isGetIpamDevicesByFetchDateLoading
      }
    >
      {open ? <Modal handleClose={handleClose} open={open} /> : null}

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
            pageName={PAGE_NAME}
            buttonsConfigurationList={buttonsConfigurationList}
            handleDateChange={handleDateChange}
          />
        }
        TABLE_DATA_UNIQUE_ID={TABLE_DATA_UNIQUE_ID}
        displayColumns={displayColumns}
        dataSource={dataSource}
        selectedRowKeys={pageEditable ? selectedRowKeys : null}
        setSelectedRowKeys={setSelectedRowKeys}
      />
    </DefaultSpinner>
  );
};

export default Index;
