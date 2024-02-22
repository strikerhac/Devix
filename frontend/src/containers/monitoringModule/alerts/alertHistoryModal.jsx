import React, { useState, useEffect } from "react";
import Grid from "@mui/material/Grid";
import { useSelector } from "react-redux";
import { selectAlertHistoryDetails } from "../../../store/features/monitoringModule/alerts/selectors";
import { useGetAlertsHistoryByIpAddressMutation } from "../../../store/features/monitoringModule/alerts/apis";
import useErrorHandling, { TYPE_FETCH } from "../../../hooks/useErrorHandling";
import useColumnsGenerator from "../../../hooks/useColumnsGenerator";
import useButtonsConfiguration from "../../../hooks/useButtonsConfiguration";
import DefaultTableConfigurations from "../../../components/tableConfigurations";
import DefaultPageTableSection from "../../../components/pageSections";
import DefaultDialog from "../../../components/dialogs";
import { CancelDialogFooter } from "../../../components/dialogFooters";
import DefaultSpinner from "../../../components/spinners";
import { useIndexTableColumnDefinitions } from "./columnDefinitions";
import { TABLE_DATA_UNIQUE_ID } from "./constants";
import { PAGE_NAME } from "./constants";

const Index = ({ handleClose, open, record = null }) => {
  // states required in hooks
  const [selectedRowKeys, setSelectedRowKeys] = useState([]);

  // hooks
  const { alertHistoryColumnDefinitions: columnDefinitions } =
    useIndexTableColumnDefinitions();
  const generatedColumns = useColumnsGenerator({ columnDefinitions });
  const { buttonsConfigurationList } = useButtonsConfiguration({
    configure_table: { handleClick: handleTableConfigurationsOpen },
  });

  // states
  const [tableConfigurationsOpen, setTableConfigurationsOpen] = useState(false);
  const [columns, setColumns] = useState(generatedColumns);
  const [availableColumns, setAvailableColumns] = useState([]);
  const [displayColumns, setDisplayColumns] = useState(generatedColumns);

  // apis
  const [
    getAlertsHistoryByIpAddress,
    {
      data: getAlertsHistoryByIpAddressData,
      isSuccess: isGetAlertsHistoryByIpAddressSuccess,
      isLoading: isGetAlertsHistoryByIpAddressLoading,
      isError: isGetAlertsHistoryByIpAddressError,
      error: getAlertsHistoryByIpAddressError,
    },
  ] = useGetAlertsHistoryByIpAddressMutation();

  // error handling custom hooks
  useErrorHandling({
    data: getAlertsHistoryByIpAddressData,
    isSuccess: isGetAlertsHistoryByIpAddressSuccess,
    isError: isGetAlertsHistoryByIpAddressError,
    error: getAlertsHistoryByIpAddressError,
    type: TYPE_FETCH,
  });

  // getting dropdowns data from the store
  const dataSource = useSelector(selectAlertHistoryDetails);

  // effects
  useEffect(() => {
    if (record) {
      getAlertsHistoryByIpAddress({
        ip_address: record.ip_address,
      });
    }
  }, []);

  // handlers
  function handleTableConfigurationsOpen() {
    setTableConfigurationsOpen(true);
  }

  return (
    <DefaultDialog title={`${PAGE_NAME} History Details`} open={open}>
      <Grid container>
        <Grid item xs={12}>
          <DefaultSpinner spinning={isGetAlertsHistoryByIpAddressLoading}>
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
              scroll={false}
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
