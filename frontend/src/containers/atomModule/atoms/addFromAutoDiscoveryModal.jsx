import React, { useState } from "react";
import Grid from "@mui/material/Grid";
import { useSelector } from "react-redux";
import { selectAtomDevicesFromDiscovery } from "../../../store/features/atomModule/atoms/selectors";
import {
  useGetAtomsDevicesFromDiscoveryQuery,
  useAddAtomsDevicesFromDiscoveryMutation,
} from "../../../store/features/atomModule/atoms/apis";
import useErrorHandling, {
  TYPE_FETCH,
  TYPE_BULK,
  TYPE_BULK_ADD,
} from "../../../hooks/useErrorHandling";
import useColumnsGenerator from "../../../hooks/useColumnsGenerator";
import useButtonsConfiguration from "../../../hooks/useButtonsConfiguration";
import DefaultPageTableSection from "../../../components/pageSections";
import DefaultDialog from "../../../components/dialogs";
import { CancelDialogFooter } from "../../../components/dialogFooters";
import DefaultTableConfigurations from "../../../components/tableConfigurations";
import DefaultSpinner from "../../../components/spinners";
import { useIndexTableColumnDefinitions } from "../../autoDiscoveryModule/discovery/columnDefinitions";
import { TABLE_DATA_UNIQUE_ID } from "../../autoDiscoveryModule/discovery/constants";
import { PAGE_NAME } from "../../autoDiscoveryModule/discovery/constants";

const Index = ({ handleClose, open }) => {
  // states required in hooks
  const [selectedRowKeys, setSelectedRowKeys] = useState([]);

  // hooks
  const { columnDefinitions } = useIndexTableColumnDefinitions();
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
    data: getAtomsDevicesFromDiscoveryData,
    isSuccess: isGetAtomsDevicesFromDiscoverySuccess,
    isLoading: isGetAtomsDevicesFromDiscoveryLoading,
    isError: isGetAtomsDevicesFromDiscoveryError,
    error: getAtomsDevicesFromDiscoveryError,
  } = useGetAtomsDevicesFromDiscoveryQuery();

  const [
    addAtomsDevicesFromDiscovery,
    {
      data: addAtomsDevicesFromDiscoveryData,
      isSuccess: isAddAtomsDevicesFromDiscoverySuccess,
      isLoading: isAddAtomsDevicesFromDiscoveryLoading,
      isError: isAddAtomsDevicesFromDiscoveryError,
      error: addAtomsDevicesFromDiscoveryError,
    },
  ] = useAddAtomsDevicesFromDiscoveryMutation();

  // error handling custom hooks
  useErrorHandling({
    data: getAtomsDevicesFromDiscoveryData,
    isSuccess: isGetAtomsDevicesFromDiscoverySuccess,
    isError: isGetAtomsDevicesFromDiscoveryError,
    error: getAtomsDevicesFromDiscoveryError,
    type: TYPE_FETCH,
  });

  useErrorHandling({
    data: addAtomsDevicesFromDiscoveryData,
    isSuccess: isAddAtomsDevicesFromDiscoverySuccess,
    isError: isAddAtomsDevicesFromDiscoveryError,
    error: addAtomsDevicesFromDiscoveryError,
    type: TYPE_BULK_ADD,
    callback: handleClose,
  });

  // getting dropdowns data from the store
  const dataSource = useSelector(selectAtomDevicesFromDiscovery);

  // handlers
  function handleTableConfigurationsOpen() {
    setTableConfigurationsOpen(true);
  }

  function handleAdd() {
    addAtomsDevicesFromDiscovery(selectedRowKeys);
  }

  return (
    <DefaultDialog title={`${"Add"} from ${PAGE_NAME}`} open={open}>
      <Grid container>
        <Grid item xs={12}>
          <DefaultSpinner
            spinning={
              isGetAtomsDevicesFromDiscoveryLoading ||
              isAddAtomsDevicesFromDiscoveryLoading
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
