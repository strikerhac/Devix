import React, { useEffect, useState } from "react";
import { Row, Col } from "antd";
import { useDispatch } from "react-redux";
import { useSelector } from "react-redux";
import {
  useFetchRecordsQuery,
  useUpdateAdminUserRoleConfigurationMutation,
  useDeleteRecordsMutation,
} from "../../../store/features/adminModule/roles/apis";
import {
  selectTableData,
  selectSelectedRole,
  selectSelectedRoleForComparison,
} from "../../../store/features/adminModule/roles/selectors";
import { setSelectedRole } from "../../../store/features/adminModule/roles";
import { deepEqual, jsonToExcel } from "../../../utils/helpers";
import { SUCCESSFUL_FILE_EXPORT_MESSAGE } from "../../../utils/constants";
import useErrorHandling, {
  TYPE_BULK_DELETE,
} from "../../../hooks/useErrorHandling";
import useSweetAlert from "../../../hooks/useSweetAlert";
import useColumnsGenerator from "../../../hooks/useColumnsGenerator";
import useButtonsConfiguration from "../../../hooks/useButtonsConfiguration";
import {
  TYPE_FETCH,
  TYPE_SINGLE,
  TYPE_BULK,
} from "../../../hooks/useErrorHandling";
import { useAuthorization } from "../../../hooks/useAuth";
import DefaultPageTableSection from "../../../components/pageSections";
import DefaultCard from "../../../components/cards";
import { UpdateDialogFooter } from "../../../components/dialogFooters";
import DefaultSpinner from "../../../components/spinners";
import ExpandableConfigurationPanel from "./expandableConfigurationPanel";
import { useIndexTableColumnDefinitions } from "./columnDefinitions";
import Modal from "./modal";
import {
  PAGE_NAME,
  ELEMENT_NAME,
  FILE_NAME_EXPORT_ALL_DATA,
  TABLE_DATA_UNIQUE_ID,
  indexColumnNameConstants,
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
  const dispatch = useDispatch();
  const { handleSuccessAlert, handleInfoAlert, handleCallbackAlert } =
    useSweetAlert();
  const { columnDefinitions } = useIndexTableColumnDefinitions({
    pageEditable,
    handleEdit,
  });
  const generatedColumns = useColumnsGenerator({ columnDefinitions });
  const { buttonsConfigurationList } = useButtonsConfiguration({
    default_export: { handleClick: handleDefaultExport },
    default_delete: {
      handleClick: handleDelete,
      visible: selectedRowKeys.length > 0 && pageEditable,
    },
    default_add: {
      handleClick: handleDefaultAdd,
      namePostfix: ELEMENT_NAME,
      visible: pageEditable,
    },
  });

  // selectors
  const dataSource = useSelector(selectTableData);
  const selectedRole = useSelector(selectSelectedRole);
  const selectedRoleForComparison = useSelector(
    selectSelectedRoleForComparison
  );

  // states
  const [selectedRowKey, setSelectedRowKey] = useState(null);
  const [selectedRow, setSelectedRow] = useState(null);
  const [recordToEdit, setRecordToEdit] = useState(null);
  const [open, setOpen] = useState(false);
  const [displayColumns, setDisplayColumns] = useState(generatedColumns);

  // apis
  const {
    data: fetchRecordsData,
    isSuccess: isFetchRecordsSuccess,
    isLoading: isFetchRecordsLoading,
    isError: isFetchRecordsError,
    error: fetchRecordsError,
  } = useFetchRecordsQuery();

  const [
    updateRecord,
    {
      data: updateRecordData,
      isSuccess: isUpdateRecordSuccess,
      isLoading: isUpdateRecordLoading,
      isError: isUpdateRecordError,
      error: updateRecordError,
    },
  ] = useUpdateAdminUserRoleConfigurationMutation();

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
    data: updateRecordData,
    isSuccess: isUpdateRecordSuccess,
    isError: isUpdateRecordError,
    error: updateRecordError,
    type: TYPE_SINGLE,
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
    if (selectedRole) {
      setSelectedRowKey(selectedRole[indexColumnNameConstants.ROLE_ID]);
    }
  }, [selectedRole]);

  useEffect(() => {
    if (selectedRow) {
      let data = {
        ...selectedRow,
        [indexColumnNameConstants.CONFIGURATION]:
          typeof selectedRow[indexColumnNameConstants.CONFIGURATION] ===
          "string"
            ? JSON.parse(selectedRow[indexColumnNameConstants.CONFIGURATION])
            : selectedRow[indexColumnNameConstants.CONFIGURATION],
      };

      dispatch(setSelectedRole(data));
    } else {
      dispatch(setSelectedRole(selectedRow));
    }
  }, [selectedRow]);

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
      handleCallbackAlert(
        "Are you sure you want delete these records?",
        deleteData
      );
    } else {
      handleInfoAlert("No record has been selected to delete!");
    }
  }

  function handleEdit(record) {
    setRecordToEdit(record);
    setOpen(true);
  }

  function handleDefaultAdd() {
    setOpen(true);
  }

  function handleClose() {
    setRecordToEdit(null);
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

  function handleCancel() {
    if (selectedRoleForComparison)
      dispatch(setSelectedRole(selectedRoleForComparison));
  }

  function handleUpdate() {
    let data = {
      [indexColumnNameConstants.ROLE_ID]:
        selectedRole[indexColumnNameConstants.ROLE_ID],
      [indexColumnNameConstants.CONFIGURATION]: JSON.stringify(
        selectedRole[indexColumnNameConstants.CONFIGURATION]
      ),
    };
    updateRecord(data);
  }

  return (
    <DefaultSpinner
      spinning={
        isFetchRecordsLoading || isUpdateRecordLoading || isDeleteRecordsLoading
      }
    >
      {!deepEqual(selectedRole, selectedRoleForComparison) && pageEditable ? (
        <div
          style={{
            position: "fixed",
            zIndex: "9999",
            bottom: 0,
            left: "50%", // Center horizontally
            transform: "translateX(-50%)", // Center horizontally
            width: "50%",
            // glass
            background: "rgba(255, 255, 255, 0.1)", // Glass color with transparency
            padding: "20px",
            borderRadius: "10px 10px 0 0",
            backdropFilter: "blur(10px)", // Blur effect for glass
            boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)", // Shadow for depth
            textAlign: "center",
          }}
        >
          <UpdateDialogFooter
            handleCancel={handleCancel}
            handleUpdate={handleUpdate}
          />
        </div>
      ) : null}
      <DefaultCard sx={{ padding: "20px 15px", marginBottom: "20px" }}>
        <Row gutter={16}>
          <Col span={9}>
            {open ? (
              <Modal
                handleClose={handleClose}
                open={open}
                recordToEdit={recordToEdit}
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
              rowClickable={true}
              selectedRowKey={selectedRowKey}
              setSelectedRowKey={setSelectedRowKey}
              selectedRow={selectedRow}
              setSelectedRow={setSelectedRow}
              dynamicWidth={false}
              scroll={false}
            />
          </Col>

          <Col span={15}>
            {selectedRole
              ? Object.keys(
                  selectedRole[indexColumnNameConstants.CONFIGURATION]
                ).map((moduleKey) => {
                  const moduleConfigurations =
                    selectedRole[indexColumnNameConstants.CONFIGURATION][
                      moduleKey
                    ];
                  return (
                    <ExpandableConfigurationPanel
                      moduleKey={moduleKey}
                      moduleConfigurations={moduleConfigurations}
                      pageEditable={pageEditable}
                    />
                  );
                })
              : null}
          </Col>
        </Row>
      </DefaultCard>
    </DefaultSpinner>
  );
};

export default Index;
