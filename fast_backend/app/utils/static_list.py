from app.pullers.A10.a10_inv import A10Puller
from app.pullers.ACI.aci_inv import ACIPuller
from app.pullers.ASA.cisco_asa_inv import ASAPuller
from app.pullers.Arbor.arbor_inv import ArborPuller
from app.pullers.Arista.arista_inv import AristaPuller
from app.pullers.Fireeye.fireeye_inv import FireEyePuller
from app.pullers.Firepower.firepower_inv import FirePowerPuller
from app.pullers.Fortinet.fortinet_inv import FortinetPuller
from app.pullers.H3C.h3c import H3CPuller
from app.pullers.IOS.ios_inv import IOSPuller
from app.pullers.IOSXE.ios_xe_inv import XEPuller
from app.pullers.IOSXR.ios_xr_inv import XRPuller
from app.pullers.Infoblox.infoblox_inv import InfoboxPuller
from app.pullers.Juniper.juniper_inv import JuniperPuller
from app.pullers.NXOS.nxos_inv import NXOSPuller
from app.pullers.PaloAlto.palo_alto_inv import PaloAltoPuller
from app.pullers.Prime.prime_inv import PrimePuller
from app.pullers.Pulse_Secure.pulse_secure_inv import PulseSecurePuller
from app.pullers.Symantec.symantec_inv import SymantecPuller
from app.pullers.UCS.ucs_cimc_inv import UCSPuller
from app.pullers.WLC.cisco_wlc_inv import WLCPuller
from app.pullers.Wirefilter.wirefilter_inv import WirefilterPuller



password_group_types_list = [
    "SSH",
    "TELNET"
]


status_list = [
    "Production",
    "Not Production"
]

vendor_list = [
    "Cisco",
    "Extreme",
    "Fortinet",
    "HC3"
    "Huawei",
    "Juniper",
    "Linux",
    "Microsoft",
    "Paloalto",
]

function_list = [
    "Router",
    "Switch",
    "Wireless",
    "Firewall",
    "Load Balancer",
    "Controller",
    "VM",
    "EXSI",
    "Other"
]

device_type_list = [
    "a10",
    "arbor",
    "arista",
    "cisco_aireos",
    "cisco_apic",
    "cisco_asa",
    "cisco_ftd",
    "cisco_ios",
    "cisco_ios_xe",
    "cisco_ios_xr",
    "cisco_nxos",
    "cisco_ucs",
    "cisco_wlc",
    "extream_os",
    "f5_ltm",
    "fireeye",
    "firepower",
    "fortinet",
    "greatbay",
    "huawei",
    "h3c",
    "infobox",
    "juniper",
    "juniper_screenos",
    "linux",
    "paloalto",
    "prime",
    "pulse_secure",
    "symantec",
    "wire_filter",
    "window",
    "other",
]

device_type_ssh_dictionary = {
    "a10": "a10",
    "arista": "arista_eos",
    "cisco_asa": "cisco_asa",
    "cisco_ftd": "cisco_ftd",
    "cisco_ios": "cisco_ios",
    "cisco_ios_xe": "cisco_xe",
    "cisco_ios_xr": "cisco_xr",
    "cisco_nxos": "cisco_nxos",
    "cisco_wlc": "cisco_wlc",
    "extream_os": "extreme_exos",
    "f5_ltm": "f5_ltm",
    "fortinet": "fortinet",
    "huawei": "huawei",
    "h3c": "hp_comware",
    "juniper": "juniper",
    "juniper_screenos": "juniper_screenos",
    "linux": "linux",
    "paloalto": "paloalto_panos",
}

device_type_telnet_dictionary = {
    "arista": "arista_eos_telnet",
    "cisco_ios": "cisco_ios_telnet",
    "cisco_ios_xr": "cisco_xr_telnet",
    "extream_os": "extreme_exos_telnet",
    "huawei": "huawei_telnet",
    "h3c": "hp_comware_telnet",
    "paloalto": "paloalto_panos_telnet",
}

ncm_command_list = {
    "cisco_asa": ["show running-config", "show ip interface brief", "show version"],
    "cisco_ftd": ["show running-config", "show ip interface brief", "show version"],
    "cisco_ios": ["show running-config", "show ip interface brief", "show version"],
    "cisco_ios_xe": ["show running-config", "show ip interface brief", "show version"],
    "cisco_ios_xr": ["show running-config", "show ip interface brief", "show version"],
    "cisco_nxos": ["show running-config", "show ip interface brief", "show version"],
    "cisco_wlc": ["show running-config", "show ip interface brief", "show version"],
    "fortinet": ["show full-configuration"],
    "f5_ltm": ["show running-config", "yes"],
    "huawei": ["display current-cofiguration"]
}

onboard_dict = {
    "a10": A10Puller(),
    "arbor": ArborPuller(),
    "arista": AristaPuller(),
    "cisco_aci": ACIPuller(),
    "cisco_apic": ACIPuller(),
    "cisco_asa": ASAPuller(),
    "cisco_ios": IOSPuller(),
    "cisco_ios_xe": XEPuller(),
    "cisco_ios_xr": XRPuller(),
    "cisco_nxos": NXOSPuller(),
    "cisco_usc": UCSPuller(),
    "cisco_wlc": WLCPuller(),
    "cisco_wlc_ssh": WLCPuller(),
    "fireeye": FireEyePuller(),
    "firepower": FirePowerPuller(),
    "fortinet": FortinetPuller(),
    "greatbay": PrimePuller(),
    "hp_comware": H3CPuller(),
    "h3c": H3CPuller(),
    "infobox": InfoboxPuller(),
    "juniper": JuniperPuller(),
    "juniper_screenos": JuniperPuller(),
    "paloalto": PaloAltoPuller(),
    "prime": PrimePuller(),
    "pulse_secure": PulseSecurePuller(),
    "symantec": SymantecPuller(),
    "wire_filter": WirefilterPuller()
}



user_status_list =[
    "Active",
    "In Active"
]

user_account_type_list = [
    "Permanent",
    "Not Permanent"
]


virutal_list = [
    'Virtual',
    'Not-Virtual'
]

criticality_list = [
    'low',
    'medium',
    'high'
]