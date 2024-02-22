import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { useSelector } from "react-redux";
import { selectTableData } from "../../../../store/features/ipamModule/subnetsDropDown/ipDetails/selectors";
import { selectSelectedSubnet } from "../../../../store/features/ipamModule/subnetsDropDown/subnets/selectors";
import { setSelectedIpDetail } from "../../../../store/features/ipamModule/subnetsDropDown/ipDetails";
import { setSelectedSubnet } from "../../../../store/features/ipamModule/subnetsDropDown/subnets";
import {
  useFetchRecordsLazyQuery,
  useGetIpDetailsBySubnetAddressMutation,
} from "../../../../store/features/ipamModule/subnetsDropDown/ipDetails/apis";
import { jsonToExcel } from "../../../../utils/helpers";
import { SUCCESSFUL_FILE_EXPORT_MESSAGE } from "../../../../utils/constants";
import { useAuthorization } from "../../../../hooks/useAuth";
import useErrorHandling, {
  TYPE_FETCH,
} from "../../../../hooks/useErrorHandling";
import useSweetAlert from "../../../../hooks/useSweetAlert";
import useColumnsGenerator from "../../../../hooks/useColumnsGenerator";
import useButtonsConfiguration from "../../../../hooks/useButtonsConfiguration";
import DefaultSpinner from "../../../../components/spinners";
import DefaultPageTableSection from "../../../../components/pageSections";
import DefaultTableConfigurations from "../../../../components/tableConfigurations";
import DefaultDetailCards from "../../../../components/detailCards";
import firewallIcon from "../../../../resources/designRelatedSvgs/firewall.svg";
import deviceIcon from "../../../../resources/designRelatedSvgs/otherDevices.svg";
import switchIcon from "../../../../resources/designRelatedSvgs/switches.svg";
import { DROPDOWN_PATH } from "../../subnetsDropDown";
import { PAGE_PATH as PAGE_PATH_IP_HISTORY } from "../ipHistory/constants";
import { indexColumnNameConstants as subnetsColumnNameConstants } from "../subnets/constants";
import { useIndexTableColumnDefinitions } from "./columnDefinitions";
import {
  PAGE_NAME,
  FILE_NAME_EXPORT_ALL_DATA,
  TABLE_DATA_UNIQUE_ID,
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

  // hooks
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { handleSuccessAlert, handleInfoAlert } = useSweetAlert();
  const { columnDefinitions } = useIndexTableColumnDefinitions({
    handleIpAddressClick,
  });
  const generatedColumns = useColumnsGenerator({ columnDefinitions });
  const { buttonsConfigurationList } = useButtonsConfiguration({
    configure_table: { handleClick: handleTableConfigurationsOpen },
    default_export: { handleClick: handleDefaultExport },
  });

  // states
  const [tableConfigurationsOpen, setTableConfigurationsOpen] = useState(false);
  const [columns, setColumns] = useState(generatedColumns);
  const [availableColumns, setAvailableColumns] = useState([]);
  const [displayColumns, setDisplayColumns] = useState(generatedColumns);

  // selectors
  const dataSource = useSelector(selectTableData);
  const selectedSubnet = useSelector(selectSelectedSubnet);

  // apis
  const [
    fetchRecords,
    {
      data: fetchRecordsData,
      isSuccess: isFetchRecordsSuccess,
      isLoading: isFetchRecordsLoading,
      isError: isFetchRecordsError,
      error: fetchRecordsError,
    },
  ] = useFetchRecordsLazyQuery();

  const [
    getIpDetailsBySubnetAddress,
    {
      data: getIpDetailsBySubnetAddressData,
      isSuccess: isGetIpDetailsBySubnetAddressSuccess,
      isLoading: isGetIpDetailsBySubnetAddressLoading,
      isError: isGetIpDetailsBySubnetAddressError,
      error: getIpDetailsBySubnetAddressError,
    },
  ] = useGetIpDetailsBySubnetAddressMutation();

  // error handling custom hooks
  useErrorHandling({
    data: fetchRecordsData,
    isSuccess: isFetchRecordsSuccess,
    isError: isFetchRecordsError,
    error: fetchRecordsError,
    type: TYPE_FETCH,
  });

  useErrorHandling({
    data: getIpDetailsBySubnetAddressData,
    isSuccess: isGetIpDetailsBySubnetAddressSuccess,
    isError: isGetIpDetailsBySubnetAddressError,
    error: getIpDetailsBySubnetAddressError,
    type: TYPE_FETCH,
  });

  // effects
  useEffect(() => {
    if (selectedSubnet) {
      getIpDetailsBySubnetAddress({
        [subnetsColumnNameConstants.SUBNET_ADDRESS]:
          selectedSubnet[subnetsColumnNameConstants.SUBNET_ADDRESS],
      });
    } else {
      fetchRecords();
    }

    return () => {
      dispatch(setSelectedSubnet(null));
    };
  }, []);

  // handlers
  function handleDefaultExport() {
    if (dataSource?.length > 0) {
      jsonToExcel(dataSource, FILE_NAME_EXPORT_ALL_DATA);
      handleSuccessAlert(SUCCESSFUL_FILE_EXPORT_MESSAGE);
    } else {
      handleInfoAlert("No data to export.");
    }
  }

  function handleIpAddressClick(record) {
    dispatch(setSelectedIpDetail(record));
    navigate(
      `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH}/${PAGE_PATH_IP_HISTORY}`
    );
  }

  function handleTableConfigurationsOpen() {
    setTableConfigurationsOpen(true);
  }

  return (
    <DefaultSpinner
      spinning={isFetchRecordsLoading || isGetIpDetailsBySubnetAddressLoading}
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

      {selectedSubnet ? (
        <DefaultDetailCards
          data={{
            [subnetsColumnNameConstants.SUBNET_ADDRESS]:
              selectedSubnet[subnetsColumnNameConstants.SUBNET_ADDRESS],
            [subnetsColumnNameConstants.SUBNET_NAME]:
              selectedSubnet[subnetsColumnNameConstants.SUBNET_NAME],
            [subnetsColumnNameConstants.SUBNET_MASK]:
              selectedSubnet[subnetsColumnNameConstants.SUBNET_MASK],
            [subnetsColumnNameConstants.SUBNET_LOCATION]:
              selectedSubnet[subnetsColumnNameConstants.SUBNET_LOCATION],
          }}
          icons={[
            "carbon:kubernetes-ip-address",
            "carbon:ibm-cloud-subnets",
            "fe:mask",
            "mingcute:location-3-line",
          ]}
        />
      ) : null}

      <DefaultPageTableSection
        PAGE_NAME={PAGE_NAME}
        TABLE_DATA_UNIQUE_ID={TABLE_DATA_UNIQUE_ID}
        buttonsConfigurationList={buttonsConfigurationList}
        displayColumns={displayColumns}
        dataSource={dataSource}
      />
    </DefaultSpinner>
  );
};

export default Index;
