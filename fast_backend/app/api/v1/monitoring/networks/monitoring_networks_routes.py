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
    prefix="/monitoring_network",
    tags=["monitoring_network"]
)

@router.post('/get_interfaces_by_ip_address',responses={
    200:{"model":list[InterfaceCardDataSchema]},
    500:{"model":str}
},
summary="API to get the interfaces based on ip address",
description="API to get the interfaces based on ip address"
)
def get_interfaces_by_ip_address(ip: MonitoringAlertsByIpAddress):
    try:
        ip=ip.ip_address
        interfaces_list = []
        query = f'import "strings"\
                       import "influxdata/influxdb/schema"\
                       from(bucket: "monitoring")\
                       |> range(start: -1d)\
                       |> filter(fn: (r) => r["_measurement"] == "Interfaces")\
                       |> filter(fn: (r) => r["IP_ADDRESS"] == "{ip}")\
                       |> schema.fieldsAsCols()\
                       |> sort(columns: ["_time"], desc: true)\
                       |> unique(column: "Interface_Name")\
                       |> yield(name: "unique")'
        interfaces_dict = {
            "interfaces":get_interface_influx_data(query)
        }
        result = get_interface_influx_data(query)
        print("interfaces dict is:::::::::::::::",result,file=sys.stderr)
        interfaces_list.append(result)
        return result
    except Exception as e:
        configs.db.rollback()
        traceback.print_exc()
        return JSONResponse(content="Error OCcured While Getting the interfaces by ip address",status_code=500)


@router.get('/get_all_devices_in_networks',
            responses={
                200:{"model":list[GetMonitoringNetworkDevicesSchema]},
                500:{"model":str}
            },
            summary="use this api in monitoring network=>devices to list down all devices in table",
            description = "use this api in monitoring network=>devices to list down all devices in table"

)
async def get_all_devices_in_networks():
    try:
        final_list = []
        org = "monetx"
        query_api = configs.client.query_api()
        query = f'import "strings"\
                   import "influxdata/influxdb/schema"\
                   from(bucket: "monitoring")\
                   |> range(start:-60d)\
                   |> filter(fn: (r) => r["_measurement"] == "Devices")\
                   |> filter(fn: (r) => r["FUNCTION"] != "VM")\
                   |> last()\
                   |> schema.fieldsAsCols()'
        result = query_api.query(org="monetx", query=query)
        print("result in get all networking devices is::for influx is", result, file=sys.stderr)
        results = []

        for table in result:
            print("table in result is:::::::::::::::::", table, file=sys.stderr)
            for record in table.records:
                print("record is::::::::::::::::::::", record, file=sys.stderr)
                try:
                    objDict = {
                        'ip_address': record.get("IP_ADDRESS"),
                        'function': record.get("FUNCTION"),
                        'response': record.get('Response'),
                        'status': record.get('STATUS'),
                        'uptime': record.get('Uptime'),
                        'vendor': record.get('VENDOR'),
                        'cpu': record.get('CPU'),
                        'memory': record.get('Memory'),
                        'packets': record.get('PACKETS_LOSS'),
                        'device_name': record.get('DEVICE_NAME'),
                        'interfaces': record.get('INTERFACES'),
                        'date': record.get('Date'),
                        'device_description': record.get('DEVICE_DESCRIPTION'),
                        'discovered_time': record.get('DISCOVERED_TIME'),
                        'device_type': record.get('DEVICE_TYPE')
                    }
                    results.append(objDict)
                    print("results list is updated :::::::;", result, file=sys.stderr)
                except Exception as e:
                    print("error", str(e), file=sys.stderr)
                    traceback.print_exc()

        final = sorted(results, key=lambda k: k.get('date', ''), reverse=False)
        print("final list is:::::::::::::::::::::::::",final,file=sys.stderr)
        if final:
            final_list = list({v['ip_address']: v for v in final}.values())
            print("final list is not none:::::::",final_list,file=sys.stderr)
        return final_list
    except Exception as e:
        configs.db.rollback()
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Getting Network Devices",status_code=500)


@router.get('/get_all_devices_interfaces_in_networks',
            responses={
                200:{"model":list[GetDevicesInterfaceRecordSchema]},
                500:{"model":str}
            },
            summary="use this api in monitoring network=>devices=>interfaces to list down all devices interfaces in table",
            description="use this api in monitoring network=>devices=>interfaces to list down all devices interfaces in table"

)
async def get_all_interfaces_in_network():
    try:
        org = "monetx"
        query_api = configs.client.query_api()
        query = '''
            import "strings"
            import "influxdata/influxdb/schema"
            from(bucket: "monitoring")
            |> range(start:-60d)
            |> filter(fn: (r) => r["_measurement"] == "Interfaces")
            |> filter(fn: (r) => r["FUNCTION"] != "VM")
            |> schema.fieldsAsCols()
            |> sort(columns: ["_time"], desc: true)
            |> unique(column: "Interface_Name")
            |> yield(name: "unique")
        '''
        result = query_api.query(org="monetx", query=query)
        print("result is::::::::::::::::::::::::::::::",result,file=sys.stderr)
        interface_records = []
        for table in result:
            print("for table in result is::::::::::::::::",table,file=sys.stderr)
            for record in table.records:
                print("record is:::::::::::::::::::::",record,file=sys.stderr)
                try:
                    interface_record = GetDevicesInterfaceRecordSchema(
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
                    interface_records.append(interface_record)
                except Exception as e:
                    print(f"Error while processing record: {str(e)}", file=sys.stderr)
                    continue
        print("interrface record is:::::::::::::::::::::::::",interface_records,file=sys.stderr)
        # Filter unique InterfaceRecords based on 'interface_name'
        final_interfaces = list({record.interface_name: record for record in interface_records}.values())
        print("final interface is:::::::::::::::::::::::",final_interfaces,file=sys.stderr)
        return final_interfaces

    except Exception as e:
        configs.db.rollback()
        print(f"Error occurred: {str(e)}", file=sys.stderr)
        raise JSONResponse(status_code=500, detail="Internal Server Error")


@router.get('/get_all_devices_in_router',
            responses={
              200:{"model":list[GetMonitoringNetworkDevicesSchema]},
              500:{"model":str}
            },
            summary="Use this API in Monitoring ==>Netowrk==>Router==>devices.Use this API in the monitoring netowrk page to list down the devices in the table of router",
            description="Use this API in Monitoring ==>Netowrk==>Router==>devices.Use this API in the monitoring netowrk page to list down the devices in the table of router",
)
def get_all_devices_in_router():
    try:
        query_api = configs.client.query_api()
        query = f'import "strings"\
                    import "influxdata/influxdb/schema"\
                    from(bucket: "monitoring")\
                    |> range(start: -60d)\
                    |> filter(fn: (r) => r["_measurement"] == "Devices")\
                    |> filter(fn: (r) => r["FUNCTION"] == "Router")\
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
                    router_devices_Record = GetMonitoringNetworkDevicesSchema(
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
                    results.append(router_devices_Record)
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
        configs.db.rollback()
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Getting Network Devices",status_code=500)


@router.get('/get_all_devices_interfaces_in_routers',
            responses={
                200:{"model":list[GetDevicesInterfaceRecordSchema]},
                500:{"model":str}
            },
            summary="use this api in monitoring network=>devices=>interfaces to list down all devices interfaces in table",
            description="use this api in monitoring network=>devices=>interfaces to list down all devices interfaces in table"

)
async def get_all_interfaces_in_routers():
    try:
        router_interface_records = []
        query_api = configs.client.query_api()
        query = f'import "strings"\
        import "influxdata/influxdb/schema"\
        from(bucket: "monitoring")\
        |> range(start: -60d)\
        |> filter(fn: (r) => r["_measurement"] == "Interfaces")\
        |> filter(fn: (r) => r["FUNCTION"] == "Router")\
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
        return JSONResponse(content = final_interfaces,status_code=200)

    except Exception as e:
        configs.db.rollback()
        print("Error ",str(e),file=sys.stderr)
        traceback.print_exc()
        return JSONResponse("Error Ocucred while getting Router interfaces",status_code=500)


@router.get('/get_all_devices_in_switch',
            responses={
              200:{"model":list[GetMonitoringNetworkDevicesSchema]},
              500:{"model":str}
            },
            summary="Use this API in Monitoring ==>Netowrk==>Switch==>devices.Use this API in the monitoring netowrk page to list down the devices in the table of router",
            description="Use this API in Monitoring ==>Netowrk==>Switch==>devices.Use this API in the monitoring netowrk page to list down the devices in the table of router",
)
def get_all_devices_in_switch():
    try:
        query_api = configs.client.query_api()
        query = f'import "strings"\
                    import "influxdata/influxdb/schema"\
                    from(bucket: "monitoring")\
                    |> range(start: -60d)\
                    |> filter(fn: (r) => r["_measurement"] == "Devices")\
                    |> filter(fn: (r) => r["FUNCTION"] == "Switch")\
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
        configs.db.rollback()
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Getting Network switch Devices",status_code=500)


@router.get('/get_all_devices_interfaces_in_switch',
            responses={
                200:{"model":list[GetDevicesInterfaceRecordSchema]},
                500:{"model":str}
            },
            summary="use this api in monitoring network=>Switch=>interfaces to list down all switch devices interfaces in table",
            description="use this api in monitoring network=>Switch=>interfaces to list down all switch devices interfaces in table"

)
async def get_all_interfaces_in_switch():
    try:
        router_interface_records = []
        query_api = configs.client.query_api()
        query = f'import "strings"\
               import "influxdata/influxdb/schema"\
               from(bucket: "monitoring")\
               |> range(start: -60d)\
               |> filter(fn: (r) => r["_measurement"] == "Interfaces")\
               |> filter(fn: (r) => r["FUNCTION"] == "Switch")\
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
        return JSONResponse(content = final_interfaces,status_code=200)

    except Exception as e:
        configs.db.rollback()
        print("Error ",str(e),file=sys.stderr)
        traceback.print_exc()
        return JSONResponse("Error Ocucred while getting Switch interfaces",status_code=500)


@router.get('/get_all_devices_in_firewall',
            responses={
              200:{"model":list[GetMonitoringNetworkDevicesSchema]},
              500:{"model":str}
            },
            summary="Use this API in Monitoring ==>Netowrk==>FireWall==>devices.Use this API in the monitoring netowrk page to list down the devices in the table of Firewall",
            description="Use this API in Monitoring ==>Netowrk==>Firewall==>devices.Use this API in the monitoring netowrk page to list down the interface  in the table of interface Firewall",
)
def get_all_devices_in_firewall():
    try:
        query_api = configs.client.query_api()
        query = f'import "strings"\
                   import "influxdata/influxdb/schema"\
                   from(bucket: "monitoring")\
                   |> range(start: -60d)\
                   |> filter(fn: (r) => r["_measurement"] == "Devices")\
                   |> filter(fn: (r) => r["FUNCTION"] == "Firewall")\
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
        configs.db.rollback()
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Getting Network Devices",status_code=500)


@router.get('/get_all_devices_interfaces_in_firewall',
            responses={
                200:{"model":list[GetDevicesInterfaceRecordSchema]},
                500:{"model":str}
            },
            summary="use this api in monitoring network=>Firewall=>interfaces to list down all firewall devices in table",
            description="use this api in monitoring network=>Firewall=>interfaces to list down all firewall interfaces in table",

)
async def get_all_interfaces_in_firewall():
    try:
        router_interface_records = []
        query_api = configs.client.query_api()
        query = f'import "strings"\
                import "influxdata/influxdb/schema"\
                from(bucket: "monitoring")\
                |> range(start: -60d)\
                |> filter(fn: (r) => r["_measurement"] == "Interfaces")\
                |> filter(fn: (r) => r["FUNCTION"] == "Firewall")\
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
        return JSONResponse(content = final_interfaces,status_code=200)

    except Exception as e:
        configs.db.rollback()
        print("Error ",str(e),file=sys.stderr)
        traceback.print_exc()
        return JSONResponse("Error Ocucred while getting Firewall interfaces",status_code=500)




@router.get('/get_all_devices_in_wireless',
            responses={
              200:{"model":list[GetMonitoringNetworkDevicesSchema]},
              500:{"model":str}
            },
            summary="Use this API in Monitoring ==>Netowrk==>Wireless==>devices.Use this API in the monitoring netowrk page to list down the devices in the table of Wireless",
            description="Use this API in Monitoring ==>Netowrk==>Wireless==>devices.Use this API in the monitoring netowrk page to list down the devices in the table of Wireless",
)
def get_all_devices_in_wireless():
    try:
        query_api = configs.client.query_api()
        query = f'import "strings"\
                    import "influxdata/influxdb/schema"\
                    from(bucket: "monitoring")\
                    |> range(start: -60d)\
                    |> filter(fn: (r) => r["_measurement"] == "Devices")\
                    |> filter(fn: (r) => r["FUNCTION"] == "Wireless")\
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
        configs.db.rollback()
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Getting Network Devices",status_code=500)


@router.get('/get_all_devices_interfaces_in_wireless',
            responses={
                200:{"model":list[GetDevicesInterfaceRecordSchema]},
                500:{"model":str}
            },
            summary="use this api in monitoring network=>Wireless=>interfaces to list down all Wireless devices  in table",
            description="use this api in monitoring network=>Wireless=>interfaces to list down all Wireless interfaces  in table",

)
async def get_all_interfaces_in_wireless():
    try:
        router_interface_records = []
        query_api = configs.client.query_api()
        query = f'import "strings"\
                import "influxdata/influxdb/schema"\
                from(bucket: "monitoring")\
                |> range(start: -60d)\
                |> filter(fn: (r) => r["_measurement"] == "Interfaces")\
                |> filter(fn: (r) => r["FUNCTION"] == "Wireless")\
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
        return JSONResponse(content = final_interfaces,status_code=200)

    except Exception as e:
        configs.db.rollback()
        print("Error ",str(e),file=sys.stderr)
        traceback.print_exc()
        return JSONResponse("Error Ocucred while getting Wireless interfaces",status_code=500)
