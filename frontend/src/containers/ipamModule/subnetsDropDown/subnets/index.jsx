import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { useSelector } from "react-redux";
import { selectTableData } from "../../../../store/features/ipamModule/subnetsDropDown/subnets/selectors";
import { setSelectedSubnet } from "../../../../store/features/ipamModule/subnetsDropDown/subnets";
import {
  useFetchRecordsQuery,
  useAddRecordsMutation,
  useDeleteRecordsMutation,
  useScanAllIpamSubnetsMutation,
  useScanIpamSubnetMutation,
} from "../../../../store/features/ipamModule/subnetsDropDown/subnets/apis";
import {
  jsonToExcel,
  convertToJson,
  handleFileChange,
  generateObject,
} from "../../../../utils/helpers";
import {
  DELETE_PROMPT,
  DELETE_SELECTION_PROMPT,
  SUCCESSFUL_FILE_EXPORT_MESSAGE,
} from "../../../../utils/constants";
import { useAuthorization } from "../../../../hooks/useAuth";
import useErrorHandling, {
  TYPE_FETCH,
  TYPE_BULK,
  TYPE_BULK_ADD_UPDATE,
  TYPE_BULK_DELETE,
  TYPE_BULK_SCAN,
} from "../../../../hooks/useErrorHandling";
import useSweetAlert from "../../../../hooks/useSweetAlert";
import useColumnsGenerator from "../../../../hooks/useColumnsGenerator";
import useButtonsConfiguration from "../../../../hooks/useButtonsConfiguration";
import DefaultPageTableSection from "../../../../components/pageSections";
import DefaultTableConfigurations from "../../../../components/tableConfigurations";
import DefaultSpinner from "../../../../components/spinners";
import { PAGE_PATH as PAGE_PATH_IP_DETAILS } from "../ipDetails/constants";
import { DROPDOWN_PATH } from "../../subnetsDropDown";
import { useIndexTableColumnDefinitions } from "./columnDefinitions";
import Modal from "./modal";
import {
  PAGE_NAME,
  ELEMENT_NAME,
  FILE_NAME_EXPORT_ALL_DATA,
  FILE_NAME_EXPORT_TEMPLATE,
  TABLE_DATA_UNIQUE_ID,
  indexColumnNameConstants,
  PORT_SCAN,
  DNS_SCAN,
  PAGE_PATH,
} from "./constants";
import { MODULE_PATH } from "../..";
import { MAIN_LAYOUT_PATH } from "../../../../layouts/mainLayout";

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
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { handleSuccessAlert, handleInfoAlert, handleCallbackAlert } =
    useSweetAlert();
  const { columnDefinitions, dataKeys } = useIndexTableColumnDefinitions({
    pageEditable,
    handleEdit,
    handleIpAddressClick,
  });
  const generatedColumns = useColumnsGenerator({ columnDefinitions });
  const { dropdownButtonOptionsConstants, buttonsConfigurationList } =
    useButtonsConfiguration({
      configure_table: { handleClick: handleTableConfigurationsOpen },
      template_export: { handleClick: handleExport },
      bulk_scan: {
        handleClick: handleBulkScan,
        visible: pageEditable,
      },
      default_scan: {
        handleClick: handleDefaultScan,
        visible: selectedRowKeys.length > 0 && pageEditable,
      },
      default_delete: {
        handleClick: handleDelete,
        visible: selectedRowKeys.length > 0 && pageEditable,
      },
      default_add: {
        handleClick: handleDefaultAdd,
        namePostfix: ELEMENT_NAME,
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
    deleteRecords,
    {
      data: deleteRecordsData,
      isSuccess: isDeleteRecordsSuccess,
      isLoading: isDeleteRecordsLoading,
      isError: isDeleteRecordsError,
      error: deleteRecordsError,
    },
  ] = useDeleteRecordsMutation();

  const [
    scanAllIpamSubnets,
    {
      data: scanAllIpamSubnetsData,
      isSuccess: isScanAllIpamSubnetsSuccess,
      isLoading: isScanAllIpamSubnetsLoading,
      isError: isScanAllIpamSubnetsError,
      error: scanAllIpamSubnetsError,
    },
  ] = useScanAllIpamSubnetsMutation();

  const [
    scanIpamSubnet,
    {
      data: scanIpamSubnetData,
      isSuccess: isScanIpamSubnetSuccess,
      isLoading: isScanIpamSubnetLoading,
      isError: isScanIpamSubnetError,
      error: scanIpamSubnetError,
    },
  ] = useScanIpamSubnetMutation();

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
    callback: handleEmptySelectedRowKeys,
  });

  useErrorHandling({
    data: scanAllIpamSubnetsData,
    isSuccess: isScanAllIpamSubnetsSuccess,
    isError: isScanAllIpamSubnetsError,
    error: scanAllIpamSubnetsError,
    type: TYPE_BULK_SCAN,
  });

  useErrorHandling({
    data: scanIpamSubnetData,
    isSuccess: isScanIpamSubnetSuccess,
    isError: isScanIpamSubnetError,
    error: scanIpamSubnetError,
    type: TYPE_BULK_SCAN,
  });

  // effects

  // handlers
  function handleEmptySelectedRowKeys() {
    setSelectedRowKeys([]);
  }

  function handlePostSeed(data) {
    addRecords(data);
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

  function handleDefaultAdd() {
    setRecordToEdit(null);
    setOpen(true);
  }

  function handleInputClick() {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  }

  function handleDefaultScan() {
    scanIpamSubnet({
      [indexColumnNameConstants.SUBNET_ID]: selectedRowKeys,
      [PORT_SCAN]: true,
      [DNS_SCAN]: true,
    });
  }

  function handleBulkScan(data) {
    scanAllIpamSubnets(data);
  }

  function handleClose() {
    setRecordToEdit(null);
    setOpen(false);
  }

  function handleIpAddressClick(record) {
    dispatch(setSelectedSubnet(record));
    navigate(
      `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH}/${PAGE_PATH_IP_DETAILS}`
    );
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
        isScanAllIpamSubnetsLoading ||
        isScanIpamSubnetLoading
      }
    >
      <div>
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
      </div>
    </DefaultSpinner>
  );
};

export default Index;
