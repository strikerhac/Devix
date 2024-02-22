import React, { useState } from "react";
import Grid from "@mui/material/Grid";
import { useSelector } from "react-redux";
import { selectAtomsToAddInMonitoringDevicesData } from "../../../store/features/monitoringModule/devices/selectors";
import { selectMonitoringCredentialsNames } from "../../../store/features/dropDowns/selectors";
import {
  useGetAtomsToAddInMonitoringDevicesQuery,
  useAddAtomsInMonitoringDevicesMutation,
} from "../../../store/features/monitoringModule/devices/apis";
import useErrorHandling, {
  TYPE_FETCH,
  TYPE_BULK,
  TYPE_BULK_ADD,
} from "../../../hooks/useErrorHandling";
import useColumnsGenerator from "../../../hooks/useColumnsGenerator";
import useButtonsConfiguration from "../../../hooks/useButtonsConfiguration";
import DefaultTableConfigurations from "../../../components/tableConfigurations";
import DefaultDialog from "../../../components/dialogs";
import { CancelDialogFooter } from "../../../components/dialogFooters";
import DefaultPageTableSection from "../../../components/pageSections";
import DefaultSpinner from "../../../components/spinners";
import { useIndexTableColumnDefinitions } from "../../atomModule/atoms/columnDefinitions";
import { ATOM_ID as TABLE_DATA_UNIQUE_ID } from "../../atomModule/atoms/constants";
import { PAGE_NAME } from "../../atomModule/atoms/constants";
import { ATOM_ID } from "../../atomModule/atoms/constants";
import { MONITORING_CREDENTIALS_ID, CREDENTIALS } from "./constants";

const Index = ({ handleClose, open }) => {
  // selectors
  const monitoringCredentialsNames = useSelector(
    selectMonitoringCredentialsNames
  );

  const monitoringCredentialsOptions = monitoringCredentialsNames.map(
    (item) => ({
      name: item[CREDENTIALS],
      value: item[MONITORING_CREDENTIALS_ID],
    })
  );

  // states required in hooks
  const [selectedRows, setSelectedRows] = useState([]);
  const [dropdownValues, setDropdownValues] = useState({});
  const [selectedRowKeys, setSelectedRowKeys] = useState([]);

  // hooks
  const { columnDefinitionsForMonitoringDevices: columnDefinitions } =
    useIndexTableColumnDefinitions({
      dropDowns: {
        handler: handleSelectsChange,
        data: {
          [MONITORING_CREDENTIALS_ID]: monitoringCredentialsOptions,
        },
      },
    });
  const generatedColumns = useColumnsGenerator({ columnDefinitions });
  const { buttonsConfigurationList } = useButtonsConfiguration({
    configure_table: { handleClick: handleTableConfigurationsOpen },
    default_add: {
      handleClick: handleAdd,
      namePostfix: PAGE_NAME,
      visible: selectedRowKeys.length > 0,
    },
  });

  // states
  const [tableConfigurationsOpen, setTableConfigurationsOpen] = useState(false);
  const [columns, setColumns] = useState(generatedColumns);
  const [availableColumns, setAvailableColumns] = useState([]);
  const [displayColumns, setDisplayColumns] = useState(generatedColumns);

  // apis
  const {
    data: getAtomsToAddInMonitoringDevicesData,
    isSuccess: isGetAtomsToAddInMonitoringDevicesSuccess,
    isLoading: isGetAtomsToAddInMonitoringDevicesLoading,
    isError: isGetAtomsToAddInMonitoringDevicesError,
    error: getAtomsToAddInMonitoringDevicesError,
  } = useGetAtomsToAddInMonitoringDevicesQuery();

  const [
    addAtomsInMonitoring,
    {
      data: addAtomsInMonitoringDevicesData,
      isSuccess: isAddAtomsInMonitoringDevicesSuccess,
      isLoading: isAddAtomsInMonitoringDevicesLoading,
      isError: isAddAtomsInMonitoringDevicesError,
      error: addAtomsInMonitoringDevicesError,
    },
  ] = useAddAtomsInMonitoringDevicesMutation();

  // error handling custom hooks
  useErrorHandling({
    data: getAtomsToAddInMonitoringDevicesData,
    isSuccess: isGetAtomsToAddInMonitoringDevicesSuccess,
    isError: isGetAtomsToAddInMonitoringDevicesError,
    error: getAtomsToAddInMonitoringDevicesError,
    type: TYPE_FETCH,
  });

  useErrorHandling({
    data: addAtomsInMonitoringDevicesData,
    isSuccess: isAddAtomsInMonitoringDevicesSuccess,
    isError: isAddAtomsInMonitoringDevicesError,
    error: addAtomsInMonitoringDevicesError,
    type: TYPE_BULK_ADD,
    callback: handleClose,
  });

  // getting dropdowns data from the store
  const dataSource = useSelector(selectAtomsToAddInMonitoringDevicesData);

  // handlers
  function handleSelectsChange(selectName, recordId, value) {
    setDropdownValues((prevValues) => {
      return {
        ...prevValues,
        [selectName]: {
          ...(prevValues[selectName] || {}),
          [recordId]: value,
        },
      };
    });
  }

  function handleTableConfigurationsOpen() {
    setTableConfigurationsOpen(true);
  }

  function handleAdd() {
    const defaultMonitoringCredentialId =
      monitoringCredentialsNames?.length > 0
        ? monitoringCredentialsNames[0][MONITORING_CREDENTIALS_ID]
        : "";

    const data = selectedRowKeys?.map((rowKey) => {
      const selectedCredentialId =
        dropdownValues[MONITORING_CREDENTIALS_ID]?.[rowKey] ||
        defaultMonitoringCredentialId;

      return {
        [ATOM_ID]: rowKey,
        [MONITORING_CREDENTIALS_ID]: selectedCredentialId,
      };
    });

    addAtomsInMonitoring(data);
  }

  return (
    <DefaultDialog title={`${"Add"} ${PAGE_NAME}`} open={open}>
      <Grid container>
        <Grid item xs={12}>
          <DefaultSpinner
            spinning={
              isGetAtomsToAddInMonitoringDevicesLoading ||
              isAddAtomsInMonitoringDevicesLoading
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

            <DefaultPageTableSection
              PAGE_NAME={PAGE_NAME}
              TABLE_DATA_UNIQUE_ID={TABLE_DATA_UNIQUE_ID}
              buttonsConfigurationList={buttonsConfigurationList}
              displayColumns={displayColumns}
              dataSource={dataSource}
              selectedRowKeys={selectedRowKeys}
              setSelectedRowKeys={setSelectedRowKeys}
              selectedRows={selectedRows}
              setSelectedRows={setSelectedRows}
              dynamicWidth={false}
              defaultPageSize={7}
            />
          </DefaultSpinner>
        </Grid>
        <Grid item xs={12}>
          <CancelDialogFooter handleClose={handleClose} />
        </Grid>
      </Grid>
    </DefaultDialog>
  );
};

export default Index;
