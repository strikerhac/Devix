import React, { useState, useRef } from "react";
import { useSelector } from "react-redux";
import { selectTableData } from "../../../store/features/atomModule/atoms/selectors";
import {
  useFetchRecordsQuery,
  useAddRecordsMutation,
  useDeleteRecordsMutation,
  useOnBoardRecordsMutation,
} from "../../../store/features/atomModule/atoms/apis";
import {
  jsonToExcel,
  convertToJson,
  handleFileChange,
  generateObject,
} from "../../../utils/helpers";
import {
  DELETE_PROMPT,
  DELETE_SELECTION_PROMPT,
  ONBOARD_PROMPT,
  ONBOARD_SELECTION_PROMPT,
  SUCCESSFUL_FILE_EXPORT_MESSAGE,
} from "../../../utils/constants";
import useSweetAlert from "../../../hooks/useSweetAlert";
import useColumnsGenerator from "../../../hooks/useColumnsGenerator";
import useButtonsConfiguration from "../../../hooks/useButtonsConfiguration";
import useErrorHandling, {
  TYPE_FETCH,
  TYPE_BULK,
  TYPE_BULK_ADD_UPDATE,
  TYPE_BULK_DELETE,
  TYPE_BULK_ONBOARD,
} from "../../../hooks/useErrorHandling";
import { useAuthorization } from "../../../hooks/useAuth";
import DefaultTableConfigurations from "../../../components/tableConfigurations";
import DefaultPageTableSection from "../../../components/pageSections";
import DefaultSpinner from "../../../components/spinners";
import SiteModal from "../../uamModule/sites/modal";
import RackModal from "../../uamModule/racks/modal";
import PasswordGroupModal from "../passwordGroups/modal";
import Modal from "./modal";
import { useIndexTableColumnDefinitions } from "./columnDefinitions";
import AddFromAutoDiscoveryModal from "./addFromAutoDiscoveryModal";
import { MODULE_PATH } from "..";
import {
  PAGE_NAME,
  ELEMENT_NAME,
  FILE_NAME_EXPORT_ALL_DATA,
  FILE_NAME_EXPORT_COMPLETE_DATA,
  FILE_NAME_EXPORT_INCOMPLETE_DATA,
  FILE_NAME_EXPORT_TEMPLATE,
  TABLE_DATA_UNIQUE_ID,
  ATOM_ID,
  ATOM_TRANSITION_ID,
  PAGE_PATH,
} from "./constants";

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

  // selectors
  const dataSource = useSelector(selectTableData);

  // apis required in hooks
  const {
    data: fetchRecordsData,
    isSuccess: isFetchRecordsSuccess,
    isLoading: isFetchRecordsLoading,
    isError: isFetchRecordsError,
    error: fetchRecordsError,
  } = useFetchRecordsQuery();

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
      default_atom_export: {
        handleClick: handleExport,
        visible: !pageEditable,
      },
      atom_export: { handleClick: handleExport, visible: pageEditable },
      default_delete: {
        handleClick: handleDelete,
        visible: selectedRowKeys.length > 0 && pageEditable,
      },
      default_onboard: {
        handleClick: handleOnBoard,
        visible: shouldOnboardBeVisible() && pageEditable,
      },
      atom_add: {
        handleClick: handleAdd,
        namePostfix: ELEMENT_NAME,
        visible: pageEditable,
      },
      default_import: {
        handleClick: handleInputClick,
        visible: pageEditable,
      },
    });

  // refs
  const fileInputRef = useRef(null);

  // states
  const [recordToEdit, setRecordToEdit] = useState(null);
  const [open, setOpen] = useState(false);
  const [openAddFromAutoDiscoveryModal, setOpenAddFromAutoDiscoveryModal] =
    useState(false);
  const [siteModalOpen, setSiteModalOpen] = useState(false);
  const [rackModalOpen, setRackModalOpen] = useState(false);
  const [passwordGroupModalOpen, setPasswordGroupModalOpen] = useState(false);
  const [tableConfigurationsOpen, setTableConfigurationsOpen] = useState(false);
  const [columns, setColumns] = useState(generatedColumns);
  const [availableColumns, setAvailableColumns] = useState([]);
  const [displayColumns, setDisplayColumns] = useState(generatedColumns);

  // apis
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
    onBoardRecords,
    {
      data: OnBoardRecordsData,
      isSuccess: isOnBoardRecordsSuccess,
      isLoading: isOnBoardRecordsLoading,
      isError: isOnBoardRecordsError,
      error: OnBoardRecordsError,
    },
  ] = useOnBoardRecordsMutation();

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
    data: OnBoardRecordsData,
    isSuccess: isOnBoardRecordsSuccess,
    isError: isOnBoardRecordsError,
    error: OnBoardRecordsError,
    type: TYPE_BULK_ONBOARD,
    callback: handleEmptySelectedRowKeys,
  });

  // handlers
  function handleEmptySelectedRowKeys() {
    setSelectedRowKeys([]);
  }

  function shouldOnboardBeVisible() {
    if (selectedRowKeys.length > 0) {
      return selectedRowKeys.some((key) => {
        let atom = dataSource?.find((item) => item.atom_table_id === key);
        return atom && atom.atom_id;
      });
    }
    return false;
  }

  function handlePostSeed(data) {
    addRecords(data);
  }

  function deleteData(allowed) {
    if (allowed) {
      const deleteData = selectedRowKeys.map((rowKey) => {
        const dataObject = dataSource.find(
          (row) => row.atom_table_id === rowKey
        );

        if (dataObject) {
          const { atom_id, atom_transition_id } = dataObject;

          return {
            atom_id: atom_id || null,
            atom_transition_id: atom_transition_id || null,
          };
        }

        return null;
      });

      const filteredDeleteData = deleteData.filter((data) => data !== null);

      if (filteredDeleteData.length > 0) {
        deleteRecords(filteredDeleteData);
      }
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

  function onBoardData(allowed) {
    if (allowed) {
      let ipAddressesToOnBoard = selectedRowKeys.map((rowKey) => {
        const dataObject = dataSource.find(
          (row) => row.atom_table_id === rowKey
        );

        if (dataObject.atom_id) {
          return dataObject.ip_address;
        }

        return null;
      });

      ipAddressesToOnBoard = ipAddressesToOnBoard.filter(
        (data) => data !== null
      );

      if (ipAddressesToOnBoard.length > 0) {
        onBoardRecords(ipAddressesToOnBoard);
      }
    } else {
      setSelectedRowKeys([]);
    }
  }

  function handleOnBoard() {
    if (selectedRowKeys.length > 0) {
      handleCallbackAlert(ONBOARD_PROMPT, onBoardData);
    } else {
      handleInfoAlert(ONBOARD_SELECTION_PROMPT);
    }
  }

  function handleInputClick() {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  }

  function handleAdd(optionType) {
    const { ADD_MANUALLY, FROM_DISCOVERY } =
      dropdownButtonOptionsConstants.atom_add;
    if (optionType === ADD_MANUALLY) {
      setOpen(true);
    } else if (optionType === FROM_DISCOVERY) {
      setOpenAddFromAutoDiscoveryModal(true);
    }
  }

  function handleClose() {
    setRecordToEdit(null);
    setOpen(false);
  }

  function handleOpenSiteModal() {
    setSiteModalOpen(true);
  }

  function handleCloseSiteModal() {
    setSiteModalOpen(false);
  }

  function handleOpenRackModal() {
    setRackModalOpen(true);
  }

  function handleCloseRackModal() {
    setRackModalOpen(false);
  }

  function handleOpenPasswordGroupModal() {
    setPasswordGroupModalOpen(true);
  }

  function handleClosePasswordGroupModal() {
    setPasswordGroupModalOpen(false);
  }

  function handleTableConfigurationsOpen() {
    setTableConfigurationsOpen(true);
  }

  function handleExport(optionType) {
    const { ALL_DATA, TEMPLATE, COMPLETE, INCOMPLETE } =
      dropdownButtonOptionsConstants.atom_export;
    if (dataSource?.length > 0) {
      if (optionType === ALL_DATA) {
        jsonToExcel(dataSource, FILE_NAME_EXPORT_ALL_DATA);
      } else if (optionType === COMPLETE) {
        jsonToExcel(
          dataSource.filter((item) => item.hasOwnProperty(ATOM_ID)),
          FILE_NAME_EXPORT_COMPLETE_DATA
        );
      } else if (optionType === INCOMPLETE) {
        jsonToExcel(
          dataSource.filter((item) => item.hasOwnProperty(ATOM_TRANSITION_ID)),
          FILE_NAME_EXPORT_INCOMPLETE_DATA
        );
      } else {
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

  function handleEdit(record) {
    setRecordToEdit(record);
    setOpen(true);
  }

  function handleCloseAddFromAutoDiscoveryModal() {
    setOpenAddFromAutoDiscoveryModal(false);
  }

  return (
    <DefaultSpinner
      spinning={
        isFetchRecordsLoading ||
        isAddRecordsLoading ||
        isDeleteRecordsLoading ||
        isOnBoardRecordsLoading
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
          open={open}
          handleClose={handleClose}
          recordToEdit={recordToEdit}
          handleOpenSiteModal={handleOpenSiteModal}
          handleOpenRackModal={handleOpenRackModal}
          handleOpenPasswordGroupModal={handleOpenPasswordGroupModal}
        />
      ) : null}

      {openAddFromAutoDiscoveryModal ? (
        <AddFromAutoDiscoveryModal
          handleClose={handleCloseAddFromAutoDiscoveryModal}
          open={openAddFromAutoDiscoveryModal}
        />
      ) : null}
      {siteModalOpen ? (
        <SiteModal
          handleClose={handleCloseSiteModal}
          open={siteModalOpen}
          recordToEdit={null}
        />
      ) : null}

      {rackModalOpen ? (
        <RackModal
          handleClose={handleCloseRackModal}
          open={rackModalOpen}
          recordToEdit={null}
          nested={true}
        />
      ) : null}

      {passwordGroupModalOpen ? (
        <PasswordGroupModal
          handleClose={handleClosePasswordGroupModal}
          open={passwordGroupModalOpen}
          recordToEdit={null}
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
