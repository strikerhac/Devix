import React, { useState } from "react";
import Grid from "@mui/material/Grid";
import { useSelector } from "react-redux";
import { selectAtomsToAddInNcmDevicesData } from "../../../store/features/ncmModule/manageConfigurations/selectors";
import {
  useGetAtomsToAddInNcmDevicesQuery,
  useAddAtomsInNcmDevicesMutation,
} from "../../../store/features/ncmModule/manageConfigurations/apis";
import useErrorHandling, {
  TYPE_BULK_ADD,
} from "../../../hooks/useErrorHandling";
import useColumnsGenerator from "../../../hooks/useColumnsGenerator";
import useButtonsConfiguration from "../../../hooks/useButtonsConfiguration";
import { TYPE_FETCH, TYPE_BULK } from "../../../hooks/useErrorHandling";
import DefaultPageTableSection from "../../../components/pageSections";
import DefaultDialog from "../../../components/dialogs";
import { CancelDialogFooter } from "../../../components/dialogFooters";
import DefaultTableConfigurations from "../../../components/tableConfigurations";
import DefaultSpinner from "../../../components/spinners";
import { ATOM_ID as TABLE_DATA_UNIQUE_ID } from "../../atomModule/atoms/constants";
import { useIndexTableColumnDefinitions } from "../../atomModule/atoms/columnDefinitions";
import { ELEMENT_NAME_BULK } from "./constants";

const Index = ({ handleClose, open }) => {
  // states required in hooks
  const [selectedRowKeys, setSelectedRowKeys] = useState([]);

  // hooks
  const { columnDefinitionsForNcmDevices: columnDefinitions } =
    useIndexTableColumnDefinitions();
  const generatedColumns = useColumnsGenerator({ columnDefinitions });
  const { buttonsConfigurationList } = useButtonsConfiguration({
    configure_table: { handleClick: handleTableConfigurationsOpen },
    default_add: {
      handleClick: handleAdd,
      namePostfix: ELEMENT_NAME_BULK,
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
    data: getAtomsToAddInNcmDevicesData,
    isSuccess: isGetAtomsToAddInNcmDevicesSuccess,
    isLoading: isGetAtomsToAddInNcmDevicesLoading,
    isError: isGetAtomsToAddInNcmDevicesError,
    error: getAtomsToAddInNcmDevicesError,
  } = useGetAtomsToAddInNcmDevicesQuery();

  const [
    addAtomsInNcm,
    {
      data: addAtomsInNcmDevicesData,
      isSuccess: isAddAtomsInNcmDevicesSuccess,
      isLoading: isAddAtomsInNcmDevicesLoading,
      isError: isAddAtomsInNcmDevicesError,
      error: addAtomsInNcmDevicesError,
    },
  ] = useAddAtomsInNcmDevicesMutation();

  // error handling custom hooks
  useErrorHandling({
    data: getAtomsToAddInNcmDevicesData,
    isSuccess: isGetAtomsToAddInNcmDevicesSuccess,
    isError: isGetAtomsToAddInNcmDevicesError,
    error: getAtomsToAddInNcmDevicesError,
    type: TYPE_FETCH,
  });

  useErrorHandling({
    data: addAtomsInNcmDevicesData,
    isSuccess: isAddAtomsInNcmDevicesSuccess,
    isError: isAddAtomsInNcmDevicesError,
    error: addAtomsInNcmDevicesError,
    type: TYPE_BULK_ADD,
    callback: handleClose,
  });

  // getting dropdowns data from the store
  const dataSource = useSelector(selectAtomsToAddInNcmDevicesData);

  // handlers
  function handleTableConfigurationsOpen() {
    setTableConfigurationsOpen(true);
  }

  function handleAdd() {
    addAtomsInNcm(selectedRowKeys);
  }

  return (
    <DefaultDialog title={`${"Add"} ${ELEMENT_NAME_BULK}`} open={open}>
      <Grid container>
        <Grid item xs={12}>
          <DefaultSpinner
            spinning={
              isGetAtomsToAddInNcmDevicesLoading ||
              isAddAtomsInNcmDevicesLoading
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
              PAGE_NAME={ELEMENT_NAME_BULK}
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
