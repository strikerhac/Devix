import React, { useState, useRef } from "react";
import { useSelector } from "react-redux";
import { selectTableData } from "../../../store/features/uamModule/hwLifeCycles/selectors";
import {
  useFetchRecordsQuery,
  useAddRecordsMutation,
  useDeleteRecordsMutation,
  useSyncFromInventoryLazyQuery,
  useSyncToInventoryLazyQuery,
} from "../../../store/features/uamModule/hwLifeCycles/apis";
import {
  jsonToExcel,
  convertToJson,
  handleFileChange,
  generateObject,
} from "../../../utils/helpers";
import {
  DELETE_PROMPT,
  DELETE_SELECTION_PROMPT,
  SUCCESSFUL_FILE_EXPORT_MESSAGE,
} from "../../../utils/constants";
import { useAuthorization } from "../../../hooks/useAuth";
import useErrorHandling, {
  TYPE_FETCH,
  TYPE_BULK,
  TYPE_BULK_ADD_UPDATE,
  TYPE_BULK_DELETE,
  TYPE_BULK_SYNC,
} from "../../../hooks/useErrorHandling";
import useSweetAlert from "../../../hooks/useSweetAlert";
import useColumnsGenerator from "../../../hooks/useColumnsGenerator";
import useButtonsConfiguration from "../../../hooks/useButtonsConfiguration";
import DefaultPageTableSection from "../../../components/pageSections";
import DefaultTableConfigurations from "../../../components/tableConfigurations";
import DefaultSpinner from "../../../components/spinners";
import Modal from "./modal";
import { useIndexTableColumnDefinitions } from "./columnDefinitions";
import {
  PAGE_NAME,
  PAGE_PATH,
  FILE_NAME_EXPORT_ALL_DATA,
  FILE_NAME_EXPORT_TEMPLATE,
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
  const { handleSuccessAlert, handleInfoAlert, handleCallbackAlert } =
    useSweetAlert();
  const { columnDefinitions, dataKeys } = useIndexTableColumnDefinitions({
    pageEditable,
    handleEdit,
  });
  const generatedColumns = useColumnsGenerator({ columnDefinitions });
  const { dropdownButtonOptionsConstants, buttonsConfigurationList } =
    useButtonsConfiguration({
      configure_table: { handleClick: handleTableConfigurationsOpen },
      template_export: { handleClick: handleExport },
      default_delete: {
        handleClick: handleDelete,
        visible: selectedRowKeys.length > 0 && pageEditable,
      },
      inventory_sync: {
        handleClick: handleSync,
        namePostfix: PAGE_NAME,
        visible: pageEditable,
      },
      default_import: { handleClick: handleInputClick, visible: pageEditable },
    });

  // refs
  const fileInputRef = useRef(null);

  // states
  const [recordToEdit, setRecordToEdit] = useState(null);
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
    addRecords,
    {
      data: addRecordsData,
      isSuccess: isAddRecordsSuccess,
      isLoading: isAddRecordsLoading,
      isError: isAddRecordsError,
      error: addRecordsError,
    },
  ] = useAddRecordsMutation();

  const [
    syncFromInventory,
    {
      data: syncFromInventoryData,
      isSuccess: isSyncFromInventorySuccess,
      isLoading: isSyncFromInventoryLoading,
      isError: isSyncFromInventoryError,
      error: syncFromInventoryError,
    },
  ] = useSyncFromInventoryLazyQuery();

  const [
    syncToInventory,
    {
      data: syncToInventoryData,
      isSuccess: isSyncToInventorySuccess,
      isLoading: isSyncToInventoryLoading,
      isError: isSyncToInventoryError,
      error: syncToInventoryError,
    },
  ] = useSyncToInventoryLazyQuery();

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
    data: addRecordsData,
    isSuccess: isAddRecordsSuccess,
    isError: isAddRecordsError,
    error: addRecordsError,
    type: TYPE_BULK_ADD_UPDATE,
  });

  useErrorHandling({
    data: deleteRecordsData,
    isSuccess: isDeleteRecordsSuccess,
    isError: isDeleteRecordsError,
    error: deleteRecordsError,
    type: TYPE_BULK_DELETE,
  });

  useErrorHandling({
    data: syncFromInventoryData,
    isSuccess: isSyncFromInventorySuccess,
    isError: isSyncFromInventoryError,
    error: syncFromInventoryError,
    type: TYPE_BULK_SYNC,
  });

  useErrorHandling({
    data: syncToInventoryData,
    isSuccess: isSyncToInventorySuccess,
    isError: isSyncToInventoryError,
    error: syncToInventoryError,
    type: TYPE_BULK_SYNC,
  });

  // handlers
  function handlePostSeed(data) {
    addRecords(data);
  }

  function handleInputClick() {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
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

  function handleEdit(record) {
    setRecordToEdit(record);
    setOpen(true);
  }

  function handleSync(optionType) {
    const { SYNC_FROM_INVENTORY, SYNC_TO_INVENTORY } =
      dropdownButtonOptionsConstants.inventory_sync;
    if (optionType === SYNC_FROM_INVENTORY) {
      syncFromInventory();
    } else if (optionType === SYNC_TO_INVENTORY) {
      syncToInventory();
    }
  }

  function handleClose() {
    setRecordToEdit(null);
    setOpen(false);
  }

  function handleExport(optionType) {
    const { ALL_DATA, TEMPLATE } =
      dropdownButtonOptionsConstants.template_export;
    if (dataSource?.length > 0) {
      if (optionType === ALL_DATA) {
        jsonToExcel(dataSource, FILE_NAME_EXPORT_ALL_DATA);
      }
      handleSuccessAlert(SUCCESSFUL_FILE_EXPORT_MESSAGE);
    } else if (optionType === TEMPLATE) {
      jsonToExcel([generateObject(dataKeys)], FILE_NAME_EXPORT_TEMPLATE);
      handleSuccessAlert(SUCCESSFUL_FILE_EXPORT_MESSAGE);
    } else {
      handleInfoAlert("No data to export.");
    }
  }

  function handleTableConfigurationsOpen() {
    setTableConfigurationsOpen(true);
  }

  return (
    <DefaultSpinner
      spinning={
        isFetchRecordsLoading ||
        isAddRecordsLoading ||
        isDeleteRecordsLoading ||
        isSyncFromInventoryLoading ||
        isSyncToInventoryLoading
      }
    >
      <input
        type="file"
        ref={fileInputRef}
        style={{ display: "none" }}
        onChange={(e) => handleFileChange(e, convertToJson, handlePostSeed)}
      />
      {open ? (
        <Modal
          handleClose={handleClose}
          open={open}
          recordToEdit={recordToEdit}
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
