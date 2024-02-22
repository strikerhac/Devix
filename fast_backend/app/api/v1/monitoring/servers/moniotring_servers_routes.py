from fastapi import  FastAPI,Query
from fastapi import APIRouter
from app.models.monitoring_models import *
from app.schema.monitoring_schema import *
import sys
import traceback
from fastapi.responses import JSONResponse
from app.models.atom_models import *
from app.api.v1.monitoring.device.utils.monitoring_utils import *
from app.schema.monitoring_network_schema import *


router = APIRouter(
    prefix="/monitoring_server",
    tags=["monitoring_server"]
)




@router.get('/get_all_devices_in_servers',
            responses={
              200:{"model":list[GetMonitoringNetworkDevicesSchema]},
              500:{"model":str}
            },
            summary="Use this API in Monitoring ==>Netowrk==>Server==>devices.Use this API in the monitoring netowrk page to list down the devices in the table of Server all devices",
            description="Use this API in Monitoring ==>Netowrk==>Server==>devices.Use this API in the monitoring netowrk page to list down the devices in the table of Server all devices",
)
def get_all_devices_in_servers():
    try:
        query_api = configs.client.query_api()
        query = f'import "strings"\
                    import "influxdata/influxdb/schema"\
                    from(bucket: "monitoring")\
                    |> range(start: -60d)\
                    |> filter(fn: (r) => r["_measurement"] == "Devices")\
                    |> filter(fn: (r) => r["FUNCTION"] == "VM")\
                    |> last()\
                    |> schema.fieldsAsCols()'

        result = query_api.query(org='monetx', query=query)
        print("result is::::::::::::::::::",result,file=sys.stderr)
        results = []
        for table in result:
            print("table in result is:::::::::::::",table,file=sys.stderr)
            for record in table.records:
                print("record is::::::::",record,file=sys.stderr)
                try:
                    switch_devices_record = GetMonitoringNetworkDevicesSchema(
                        ip_address = record.get("IP_ADDRESS"),
                        function = record.get("FUNCTION") ,
                        repsones = record.get("Response"),
                        status = record.get("STATUS"),
                        uptime = record.get("Uptime"),
                        vendor = record.get("VENDOR"),
                        cpu = record.get("CPU"),
                        memory = record.get("Memory"),
                        packets = record.get("PACKETS_LOSS"),
                        device_name = record.get("DEVICE_NAME"),
                        interfaces = record.get("INTERFACES"),
                        date = record.get("Date"),
                        device_description = record.get("DEVICE_DESCRIPTION"),
                        discovered_time = record.get("DISCOVERED_TIME"),
                        device_type = record.get("DEVICE_TYPE"),
                    )
                    results.append(switch_devices_record)
                except Exception as e:
                    print("Error:::",str(e),file=sys.stderr)
                    traceback.print_exc()
        final = sorted(results, key=lambda k: k['date'], reverse=False)
        print("final is::::::::::::::::::",final,file=sys.stderr)
        final_list = list({v['ip_address']: v for v in final}.values())
        print(results, file=sys.stderr)
        print("final list is:::::::::::::::::::::::::",final_list,file=sys.stderr)
        return final_list
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Getting Network Devices",status_code=500)


@router.get('/get_all_devices_interfaces_in_servers',
            responses={
                200:{"model":list[GetDevicesInterfaceRecordSchema]},
                500:{"model":str}
            },
            summary="use this api in monitoring network=>Server=>interfaces to list down all Server devices interfaces in table",
            description="use this api in monitoring network=>Server=>interfaces to list down all Server devices interfaces in table",

)
async def get_all_interfaces_in_servers():
    try:
        router_interface_records = []
        query_api = configs.client.query_api()
        query = f'import "strings"\
                import "influxdata/influxdb/schema"\
                from(bucket: "monitoring")\
                |> range(start: -60d)\
                |> filter(fn: (r) => r["_measurement"] == "Interfaces")\
                |> filter(fn: (r) => r["FUNCTION"] == "VM")\
                |> schema.fieldsAsCols()\
                |> sort(columns: ["_time"], desc: true)\
                |> unique(column: "Interface_Name")\
                |> yield(name: "unique")'
        result = query_api.query(org='monetx', query=query)
        results = []
        for table in result:
            print("for table in result is::::::::::::::::",table,file=sys.stderr)
            for record in table.records:
                print("record is:::::::::::::::::::::",record,file=sys.stderr)
                try:
                    router_interface_record = GetDevicesInterfaceRecordSchema(
                        ip_address=record.get("IP_ADDRESS"),
                        device_name=record.get("DEVICE_NAME"),
                        function=record.get("FUNCTION"),
                        interface_status=record.get("Status"),
                        vendor=record.get("VENDOR"),
                        download_speed=round(float(record.get("Download") or 0), 2),
                        upload_speed=round(float(record.get("Upload") or 0), 2),
                        interface_name=record.get("Interface_Name"),
                        interface_description=record.get("Interface_Des"),
                        date=record.get("Date"),
                        device_type=record.get("DEVICE_TYPE")
                    )
                    router_interface_records.append(router_interface_record)
                except Exception as e:
                    print(f"Error while processing record: {str(e)}", file=sys.stderr)
                    continue
        interface_dict = {record.interface_name: record.dict() for record in router_interface_records}
        final_interfaces = list(interface_dict.values())

        print(final_interfaces, file=sys.stderr)
        return final_interfaces

    except Exception as e:
        print("Error ",str(e),file=sys.stderr)
        traceback.print_exc()
        return JSONResponse("Error Ocucred while getting server interfaces",status_code=500)


@router.get('/get_all_devices_in_windows',
            responses={
              200:{"model":list[GetMonitoringNetworkDevicesSchema]},
              500:{"model":str}
            },
            summary="Use this API in Monitoring ==>Netowrk==>Windows==>devices.Use this API in the monitoring netowrk page to list down the devices in the table of windows",
            description="Use this API in Monitoring ==>Netowrk==>Windows==>devices.Use this API in the monitoring netowrk page to list down the devices in the table of windows",
)
def get_all_devices_in_windows():
    try:
        query_api = configs.client.query_api()
        query = f'import "strings"\
                    import "influxdata/influxdb/schema"\
                    from(bucket: "monitoring")\
                    |> range(start: -60d)\
                    |> filter(fn: (r) => r["_measurement"] == "Devices")\
                    |> filter(fn: (r) => r["FUNCTION"] == "VM")\
                    |> filter(fn: (r) => r["DEVICE_TYPE"] == "Window")\
                    |> last()\
                    |> schema.fieldsAsCols()'

        result = query_api.query(org='monetx', query=query)
        print("result is::::::::::::::::::",result,file=sys.stderr)
        results = []
        for table in result:
            print("table in result is:::::::::::::",table,file=sys.stderr)
            for record in table.records:
                print("record is::::::::",record,file=sys.stderr)
                try:
                    switch_devices_record = GetMonitoringNetworkDevicesSchema(
                        ip_address = record.get("IP_ADDRESS"),
                        function = record.get("FUNCTION") ,
                        repsones = record.get("Response"),
                        status = record.get("STATUS"),
                        uptime = record.get("Uptime"),
                        vendor = record.get("VENDOR"),
                        cpu = record.get("CPU"),
                        memory = record.get("Memory"),
                        packets = record.get("PACKETS_LOSS"),
                        device_name = record.get("DEVICE_NAME"),
                        interfaces = record.get("INTERFACES"),
                        date = record.get("Date"),
                        device_description = record.get("DEVICE_DESCRIPTION"),
                        discovered_time = record.get("DISCOVERED_TIME"),
                        device_type = record.get("DEVICE_TYPE"),
                    )
                    results.append(switch_devices_record)
                except Exception as e:
                    print("Error:::",str(e),file=sys.stderr)
                    traceback.print_exc()
        final = sorted(results, key=lambda k: k['date'], reverse=False)
        print("final is::::::::::::::::::",final,file=sys.stderr)
        final_list = list({v['ip_address']: v for v in final}.values())
        print(results, file=sys.stderr)
        print("final list is:::::::::::::::::::::::::",final_list,file=sys.stderr)
        return final_list
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Getting windows Devices",status_code=500)


@router.get('/get_all_devices_interfaces_in_windows',
            responses={
                200:{"model":list[GetDevicesInterfaceRecordSchema]},
                500:{"model":str}
            },
            summary="use this api in monitoring network=>Windows=>interfaces to list down all windows devices interfaces in table",
            description="use this api in monitoring network=>Windows=>interfaces to list down all windows devices interfaces in table"

)
async def get_all_interfaces_in_windows():
    try:
        router_interface_records = []
        query_api = configs.client.query_api()
        query = f'import "strings"\
                import "influxdata/influxdb/schema"\
                from(bucket: "monitoring")\
                |> range(start: -60d)\
                |> filter(fn: (r) => r["_measurement"] == "Interfaces")\
                |> filter(fn: (r) => r["FUNCTION"] == "VM")\
                |> filter(fn: (r) => r["DEVICE_TYPE"] == "Window")\
                |> schema.fieldsAsCols()\
                |> sort(columns: ["_time"], desc: true)\
                |> unique(column: "Interface_Name")\
                |> yield(name: "unique")'
        result = query_api.query(org='monetx', query=query)
        results = []
        for table in result:
            print("for table in result is::::::::::::::::",table,file=sys.stderr)
            for record in table.records:
                print("record is:::::::::::::::::::::",record,file=sys.stderr)
                try:
                    router_interface_record = GetDevicesInterfaceRecordSchema(
                        ip_address=record.get("IP_ADDRESS"),
                        device_name=record.get("DEVICE_NAME"),
                        function=record.get("FUNCTION"),
                        interface_status=record.get("Status"),
                        vendor=record.get("VENDOR"),
                        download_speed=round(float(record.get("Download") or 0), 2),
                        upload_speed=round(float(record.get("Upload") or 0), 2),
                        interface_name=record.get("Interface_Name"),
                        interface_description=record.get("Interface_Des"),
                        date=record.get("Date"),
                        device_type=record.get("DEVICE_TYPE")
                    )
                    router_interface_records.append(router_interface_record)
                except Exception as e:
                    print(f"Error while processing record: {str(e)}", file=sys.stderr)
                    continue
        interface_dict = {record.interface_name: record.dict() for record in router_interface_records}
        final_interfaces = list(interface_dict.values())

        print(final_interfaces, file=sys.stderr)
        return final_interfaces

    except Exception as e:
        print("Error ",str(e),file=sys.stderr)
        traceback.print_exc()
        return JSONResponse("Error Ocucred while getting windows interfaces",status_code=500)


@router.get('/get_all_devices_in_linux',
            responses={
              200:{"model":list[GetMonitoringNetworkDevicesSchema]},
              500:{"model":str}
            },
            summary="Use this API in Monitoring ==>Netowrk==>linux==>devices.Use this API in the monitoring netowrk page to list down the devices in the table of linux",
            description="Use this API in Monitoring ==>Netowrk==>linux==>devices.Use this API in the monitoring netowrk page to list down the devices in the table of linux",
)
def get_all_devices_in_linux():
    try:
        query_api = configs.client.query_api()
        query = f'import "strings"\
                   import "influxdata/influxdb/schema"\
                   from(bucket: "monitoring")\
                   |> range(start: -60d)\
                   |> filter(fn: (r) => r["_measurement"] == "Devices")\
                   |> filter(fn: (r) => r["FUNCTION"] == "VM")\
                   |> filter(fn: (r) => r["DEVICE_TYPE"] == "Linux")\
                   |> last()\
                   |> schema.fieldsAsCols()'

        result = query_api.query(org='monetx', query=query)
        print("result is::::::::::::::::::",result,file=sys.stderr)
        results = []
        for table in result:
            print("table in result is:::::::::::::",table,file=sys.stderr)
            for record in table.records:
                print("record is::::::::",record,file=sys.stderr)
                try:
                    switch_devices_record = GetMonitoringNetworkDevicesSchema(
                        ip_address = record.get("IP_ADDRESS"),
                        function = record.get("FUNCTION") ,
                        repsones = record.get("Response"),
                        status = record.get("STATUS"),
                        uptime = record.get("Uptime"),
                        vendor = record.get("VENDOR"),
                        cpu = record.get("CPU"),
                        memory = record.get("Memory"),
                        packets = record.get("PACKETS_LOSS"),
                        device_name = record.get("DEVICE_NAME"),
                        interfaces = record.get("INTERFACES"),
                        date = record.get("Date"),
                        device_description = record.get("DEVICE_DESCRIPTION"),
                        discovered_time = record.get("DISCOVERED_TIME"),
                        device_type = record.get("DEVICE_TYPE"),
                    )
                    results.append(switch_devices_record)
                except Exception as e:
                    print("Error:::",str(e),file=sys.stderr)
                    traceback.print_exc()
        final = sorted(results, key=lambda k: k['date'], reverse=False)
        print("final is::::::::::::::::::",final,file=sys.stderr)
        final_list = list({v['ip_address']: v for v in final}.values())
        print(results, file=sys.stderr)
        print("final list is:::::::::::::::::::::::::",final_list,file=sys.stderr)
        return final_list
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Getting server Devices",status_code=500)


@router.get('/get_all_devices_interfaces_in_linux',
            responses={
                200:{"model":list[GetDevicesInterfaceRecordSchema]},
                500:{"model":str}
            },
            summary="use this api in monitoring network=>linux=>interfaces to list down all devices interfaces in table for linux",
            description="use this api in monitoring network=>linux=>interfaces to list down all devices interfaces in table for linux",

)
async def get_all_interfaces_in_linux():
    try:
        router_interface_records = []
        query_api = configs.client.query_api()
        query = f'import "strings"\
                import "influxdata/influxdb/schema"\
                from(bucket: "monitoring")\
                |> range(start: -60d)\
                |> filter(fn: (r) => r["_measurement"] == "Interfaces")\
                |> filter(fn: (r) => r["FUNCTION"] == "VM")\
                |> filter(fn: (r) => r["DEVICE_TYPE"] == "Linux")\
                |> schema.fieldsAsCols()\
                |> sort(columns: ["_time"], desc: true)\
                |> unique(column: "Interface_Name")\
                |> yield(name: "unique")'
        result = query_api.query(org='monetx', query=query)
        results = []
        for table in result:
            print("for table in result is::::::::::::::::",table,file=sys.stderr)
            for record in table.records:
                print("record is:::::::::::::::::::::",record,file=sys.stderr)
                try:
                    router_interface_record = GetDevicesInterfaceRecordSchema(
                        ip_address=record.get("IP_ADDRESS"),
                        device_name=record.get("DEVICE_NAME"),
                        function=record.get("FUNCTION"),
                        interface_status=record.get("Status"),
                        vendor=record.get("VENDOR"),
                        download_speed=round(float(record.get("Download") or 0), 2),
                        upload_speed=round(float(record.get("Upload") or 0), 2),
                        interface_name=record.get("Interface_Name"),
                        interface_description=record.get("Interface_Des"),
                        date=record.get("Date"),
                        device_type=record.get("DEVICE_TYPE")
                    )
                    router_interface_records.append(router_interface_record)
                except Exception as e:
                    print(f"Error while processing record: {str(e)}", file=sys.stderr)
                    continue
        interface_dict = {record.interface_name: record.dict() for record in router_interface_records}
        final_interfaces = list(interface_dict.values())

        print(final_interfaces, file=sys.stderr)
        return final_interfaces

    except Exception as e:
        print("Error ",str(e),file=sys.stderr)
        traceback.print_exc()
        return JSONResponse("Error Ocucred while getting linux interfaces",status_code=500)

