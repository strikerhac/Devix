from app.api.v1.monitoring.device.utils.puller_utils import *
from app.utils.db_utils import *

cisco_ios_oids = {
    'device_name': '1.3.6.1.2.1.1.5',
    'device_description': '1.3.6.1.2.1.1.1',
    'uptime': '1.3.6.1.6.3.10.2.1.3',

    'cpu_utilization': '1.3.6.1.4.1.9.2.1.56',
    'memory_used': '1.3.6.1.4.1.9.9.48.1.1.1.5',
    'memory_free': '1.3.6.1.4.1.9.9.48.1.1.1.6',

    'interfaces': '1.3.6.1.2.1.31.1.1.1.1',
    'interface_status': '1.3.6.1.2.1.2.2.1.7',
    'interface_description': '1.3.6.1.2.1.2.2.1.2',

    'download': '1.3.6.1.2.1.31.1.1.1.6',
    'upload': '1.3.6.1.2.1.31.1.1.1.10',
}

cisco_ios_xr_oids = {
    'device_name': '1.3.6.1.2.1.1.5',
    'device_description': '1.3.6.1.2.1.1.1',
    'uptime': '1.3.6.1.6.3.10.2.1.3',

    'cpu_utilization': ('1.3.6.1.4.1.9.9.109.1.1.1.1.7', '289'),
    'memory_used': '1.3.6.1.4.1.9.9.221.1.1.1.1.18.4193',
    'memory_free': '1.3.6.1.4.1.9.9.221.1.1.1.1.20.4193',

    'interfaces': '1.3.6.1.2.1.31.1.1.1.1',
    'interface_status': '1.3.6.1.2.1.2.2.1.7',
    'interface_description': '1.3.6.1.2.1.2.2.1.2',

    'download': '1.3.6.1.2.1.31.1.1.1.6',
    'upload': '1.3.6.1.2.1.31.1.1.1.10',
}

cisco_apic_oids = {
    'device_name': '1.3.6.1.2.1.1.5',
    'device_description': '1.3.6.1.2.1.1.1',
    'uptime': '1.3.6.1.6.3.10.2.1.3',

    'cpu_utilization': '1.3.6.1.4.1.9.9.109.1.1.1.1.7',
    'memory_used': '1.3.6.1.4.1.9.9.109.1.1.1.1.12',
    'memory_free': '1.3.6.1.4.1.9.9.109.1.1.1.1.13',

    'interfaces': '1.3.6.1.2.1.31.1.1.1.1',
    'interface_status': '1.3.6.1.2.1.2.2.1.7',
    'interface_description': '1.3.6.1.2.1.2.2.1.2',

    'download': '1.3.6.1.2.1.31.1.1.1.6',
    'upload': '1.3.6.1.2.1.31.1.1.1.10',
}

cisco_nxos_oids = {
    'device_name': '1.3.6.1.2.1.1.5',
    'device_description': '1.3.6.1.2.1.1.1',
    'uptime': '1.3.6.1.6.3.10.2.1.3',

    'cpu_utilization': '1.3.6.1.4.1.9.9.109.1.1.1.1.7',
    'memory_used': '1.3.6.1.4.1.9.9.109.1.1.1.1.12',
    'memory_free': '1.3.6.1.4.1.9.9.109.1.1.1.1.13',

    'interfaces': '1.3.6.1.2.1.31.1.1.1.1',
    'interface_status': '1.3.6.1.2.1.2.2.1.7',
    'interface_description': '1.3.6.1.2.1.2.2.1.2',

    'download': '1.3.6.1.2.1.31.1.1.1.6',
    'upload': '1.3.6.1.2.1.31.1.1.1.10',
}

cisco_asa_oids = {
    'device_name': '1.3.6.1.2.1.1.5',
    'device_description': '1.3.6.1.2.1.1.1',
    'uptime': '1.3.6.1.2.1.1.3',

    'cpu_utilization': '1.3.6.1.4.1.9.9.109.1.1.1.1.2.2',
    'memory_used': '1.3.6.1.4.1.9.9.48.1.1.1.5',
    'memory_free': '1.3.6.1.4.1.9.9.48.1.1.1.6',

    'interfaces': '1.3.6.1.2.1.31.1.1.1.1',
    'interface_status': '1.3.6.1.2.1.2.2.1.7',
    'interface_description': '1.3.6.1.2.1.2.2.1.2',

    'download': '1.3.6.1.2.1.31.1.1.1.6',
    'upload': '1.3.6.1.2.1.31.1.1.1.10',
}

cisco_wlc_oids = {
    'device_name': '1.3.6.1.2.1.1.5',
    'device_description': '1.3.6.1.2.1.1.1',
    'uptime': '1.3.6.1.2.1.1.3.0',

    'cpu_utilization': '1.3.6.1.4.1.14179.1.1.5.1',
    'memory': '1.3.6.1.4.1.9.9.618.1.8.6',

    'interfaces': '1.3.6.1.2.1.2.2.1.2',
    'interface_status': '1.3.6.1.2.1.2.2.1.7',
    'interface_description': '1.3.6.1.2.1.2.2.1.2',

    'download': '1.3.6.1.2.1.31.1.1.1.6',
    'upload': '1.3.6.1.2.1.31.1.1.1.10',
}

extreme_oids = {
    'device_name': '1.3.6.1.2.1.1.5.0',
    'device_description': '1.3.6.1.2.1.1.1.0',
    'uptime': '1.3.6.1.2.1.1.3.0',

    'cpu_utilization': '1.3.6.1.4.1.1916.1.32.1.4.1.7',
    'memory_total': ' 1.3.6.1.4.1.1916.1.32.2.2.1.2',
    'memory_free': '1.3.6.1.4.1.1916.1.32.2.2.1.3',
    'memory_used_system': '1.3.6.1.4.1.1916.1.32.2.2.1.4',
    'memory_used_user': '1.3.6.1.4.1.1916.1.32.2.2.1.5',

    'interfaces': '1.3.6.1.2.1.31.1.1.1.1',
    'interface_status': '1.3.6.1.2.1.2.2.1.8',
    'interface_description': '1.3.6.1.2.1.2.2.1.2',

    'download': '1.3.6.1.2.1.2.2.1.10',
    'upload': '1.3.6.1.2.1.2.2.1.11',
}

fortinet_oids = {
    'device_name': '1.3.6.1.2.1.1.5',
    'device_description': '1.3.6.1.2.1.1.1',
    'uptime': '1.3.6.1.2.1.1.3',

    'cpu_utilization': '1.3.6.1.4.1.12356.101.4.1.3',
    'memory': '1.3.6.1.4.1.12356.101.4.1.4',

    'interfaces': '1.3.6.1.2.1.31.1.1.1.1',
    'interface_status': '1.3.6.1.2.1.2.2.1.7',
    'interface_description': '1.3.6.1.2.1.2.2.1.2',

    'download': '1.3.6.1.2.1.31.1.1.1.6',
    'upload': '1.3.6.1.2.1.31.1.1.1.10',
}

juniper_oids = {
    'device_name': '1.3.6.1.2.1.1.5',
    'device_description': '1.3.6.1.2.1.1.1',
    'uptime': '1.3.6.1.4.1.2636.3.1.5',

    'cpu_utilization': '1.3.6.1.4.1.2636.3.1.13.1.8.9.1',
    'memory': '1.3.6.1.4.1.2636.3.1.13.1.11.9',

    'interfaces': '1.3.6.1.2.1.31.1.1.1.1',
    'interface_status': '1.3.6.1.2.1.2.2.1.7',
    'interface_description': '1.3.6.1.2.1.2.2.1.2',

    'download': '1.3.6.1.4.1.2636.3.3.1.1.1',
    'upload': '1.3.6.1.4.1.2636.3.3.1.1.4',
}

linux_oids = {
    'device_name': '1.3.6.1.2.1.1.5',
    'device_description': '1.3.6.1.2.1.1.1',
    'uptime': '1.3.6.1.2.1.1.3',

    'cpu_utilization': '1.3.6.1.4.1.2021.11.9',
    'memory_total': '1.3.6.1.4.1.2021.4.5',
    'memory_free': '1.3.6.1.4.1.2021.4.11',

    'interfaces': '1.3.6.1.2.1.2.2.1.2',
    'interface_status': '1.3.6.1.2.1.2.2.1.7',
    'interface_description': '1.3.6.1.2.1.2.2.1.2',

    'download': '1.3.6.1.2.1.2.2.1.10',
    'upload': '1.3.6.1.2.1.2.2.1.16',
}

palo_oids = {
    'device_name': '1.3.6.1.2.1.1.5',
    'device_description': '1.3.6.1.2.1.1.1',
    'uptime': '1.3.6.1.2.1.25.1.1.0',

    'cpu_utilization': '1.3.6.1.2.1.25.3.3.1.2.2',
    'memory_total': '1.3.6.1.2.1.25.2.3.1.5.1020',
    'memory_used': '1.3.6.1.2.1.25.2.3.1.6.1020',

    'interfaces': '1.3.6.1.2.1.2.2.1.2',
    'interface_status': '1.3.6.1.2.1.2.2.1.7',
    'interface_description': '1.3.6.1.2.1.2.2.1.2',

    'download': '1.3.6.1.2.1.2.2.1.10',
    'upload': '1.3.6.1.2.1.2.2.1.16'
}

windows_oids = {
    'device_name': '1.3.6.1.2.1.1.5',
    'device_description': '1.3.6.1.2.1.1.1',
    'uptime': '1.3.6.1.2.1.1.3.0',

    'cpu_utilization': '1.3.6.1.2.1.25.3.3.1.2',
    'memory_total': '1.3.6.1.2.1.25.2.3.1.5',
    'memory_used': '1.3.6.1.2.1.25.2.3.1.6',

    'interfaces': '1.3.6.1.2.1.31.1.1.1.1',
    'interface_status': '1.3.6.1.2.1.2.2.1.8',
    'interface_description': '1.3.6.1.2.1.2.2.1.2',

    'download': '1.3.6.1.2.1.2.2.1.10',
    'upload': '1.3.6.1.2.1.2.2.1.11',
}


class CommonPuller(object):
    def __init__(self):
        pass

    def poll(self, host):
        atom, monitoring, credentials = host
        output = dict()

        status = ping(host[1])[0]
        print(f"{atom.ip_address} : {status}", file=sys.stderr)

        monitoring.ping_status = status
        UpdateDBData(monitoring)

        # if status == "Down":
        #     return

        if atom.device_type == "cisco_asa":
            output = getSnmpData(host, cisco_asa_oids)
        elif atom.device_type == "cisco_apic":
            output = getSnmpData(host, cisco_apic_oids)
        elif atom.device_type == "cisco_ios":
            output = getSnmpData(host, cisco_ios_oids)
        elif atom.device_type == "cisco_ios_xe":
            output = getSnmpData(host, cisco_ios_oids)
        elif atom.device_type == "cisco_ios_xr":
            output = getSnmpData(host, cisco_ios_xr_oids)
        elif atom.device_type == "cisco_nxos":
            output = getSnmpData(host, cisco_nxos_oids)
        elif atom.device_type == "cisco_wlc":
            output = getSnmpData(host, cisco_wlc_oids)
        elif atom.device_type == "extream":
            output = getSnmpData(host, extreme_oids)
        elif atom.device_type == "fortinet":
            output = getSnmpData(host, fortinet_oids)
        elif atom.device_type == "juniper":
            output = getSnmpData(host, juniper_oids)
        elif atom.device_type == "linux":
            output = getSnmpData(host, linux_oids)
        elif atom.device_type == "paloalto":
            output = getSnmpData(host, palo_oids)
        elif atom.device_type == "window":
            output = getSnmpData(host, windows_oids)
        else:
            print(
                f"\n-------- {atom.ip_address}: Support Not Available for "
                f"{atom.ip_address} --------\n",
                file=sys.stderr)
