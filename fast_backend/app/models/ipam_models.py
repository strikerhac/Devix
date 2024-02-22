from sqlalchemy import ForeignKey,Column,Boolean,String,Integer,DateTime,Date
from datetime import datetime
from app.core.config import Base
from app.models.atom_models import AtomTable


class IpamDevicesFetchTable(Base):
   __tablename__ = "ipam_devices_fetch_table"

   ipam_device_id = Column(Integer, primary_key=True, autoincrement=True)
   interface = Column(String(150), nullable=True)
   interface_ip = Column(String(156), nullable=True)
   interface_description = Column(String(256), nullable=True)
   virtual_ip = Column(String(256), nullable=True)
   vlan = Column(String(256), nullable=True)
   vlan_number = Column(String(256), nullable=True)
   interface_status = Column(String(256), nullable=True)
   fetch_date = Column(DateTime, nullable=True)
   user_id = Column(Integer, nullable=True)
   creation_date = Column(DateTime, default=datetime.now())
   modification_date = Column(DateTime, default=datetime.now())

   # Add the foreign key column for atom_id
   atom_id = Column(Integer, ForeignKey('atom_table.atom_id',ondelete='CASCADE'))

   def as_dict(self):
        data = {c.name:getattr(self,c.name) for c in self.__table__.columns}
        for key,value in data.items():
            if isinstance(value,datetime):
                data[key] = str(value)
        return data


class IpTable(Base):
    __tablename__ = 'ip_table'
    ip_id = Column(Integer,primary_key=True,autoincrement=True)
    mac_address = Column(String(256),nullable=True)
    status = Column(String(256),nullable=True)
    vip = Column(String(256),nullable=True)
    asset_tag = Column(String(256),nullable=True)
    configuration_switch = Column(String(256),nullable=True)
    configuration_interface = Column(String(256),nullable=True)
    open_ports = Column(String(256),nullable=True)
    ip_dns = Column(String(256),nullable=True)
    dns_ip =  Column(String(256),nullable=True)
    user_id = Column(Integer,nullable=True)
    last_used = Column(DateTime,nullable=True)
    ip_address = Column(String(256), nullable=True)  # New field for IP address
    subnet_id = Column(Integer, ForeignKey('subnet_table.subnet_id'), nullable=True)  # Foreign key to subnet_table
    # atom_id = Column(Integer,
    #     ForeignKey(
    #         'atom_table.atom_id',
    #     ),
    #     nullable =False
    # )
    creation_date = Column(DateTime,default=datetime.now())
    modification_date = Column(DateTime,default=datetime.now())

    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = str(value)
        return data
class IP_HISTORY_TABLE(Base):
    __tablename__ = 'ip_history_table'
    ip_history_id =Column(Integer, primary_key=True,autoincrement=True)
    ip_address = Column(String(50),nullable=True)
    mac_address = Column(String(50),nullable=True)
    asset_tag = Column(String(50),nullable=True)
    date = Column(DateTime, default=datetime.now(),
                     onupdate=datetime.now())
    ip_id = Column(Integer,ForeignKey('ip_table.ip_id'),nullable=True)
    creation_date = Column(DateTime, default=datetime.now())
    modification_date = Column(DateTime, default=datetime.now())

    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = str(value)
        return data

class subnet_table(Base):
    __tablename__ = 'subnet_table'
    subnet_id = Column(Integer,primary_key=True,autoincrement=True)
    subnet_address = Column(String(256),nullable=True)
    subnet_mask = Column(String(356),nullable=True)
    subnet_name = Column(String(256),nullable=True)
    location = Column(String(256),nullable=True)
    discovered_from = Column(String(256),nullable = True)
    user_id = Column(Integer,nullable=True)
    scan_date = Column(DateTime,nullable=True)
    discovered = Column(String(40),nullable=True)
    status = Column(String(45),nullable=True)
    subnet_state = Column(String(55),nullable = True)
    ipam_device_id = Column(Integer,
        ForeignKey('ipam_devices_fetch_table.ipam_device_id'
                   ),
    nullable=True
    )

    ip_id = Column(Integer,
        ForeignKey('ip_table.ip_id',

                   ),
                   nullable=True
                   )

    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = str(value)
        return data


class subnet_usage_table(Base):
    __tablename__ = 'subent_usage_table'
    subnet_usage_id = Column(Integer,primary_key=True,autoincrement=True)
    subnet_usage = Column(String(256),nullable=True)
    subnet_size = Column(String(256),nullable=True)
    subnet_id = Column(
        Integer,
        ForeignKey('subnet_table.subnet_id',

                   ),
        nullable=False
    )
    creation_date = Column(DateTime,default=datetime.now())
    modification_date = Column(DateTime,default=datetime.now())

    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = str(value)
        return data

class ip_interface_table(Base):
    __tablename__ = 'ip_interface_table'
    ip_interface_id = Column(Integer,primary_key=True,autoincrement=True)
    interface_ip = Column(String(256),nullable=True)
    interface_location = Column(String(256),nullable = True)
    discovered_from = Column(String(256),nullable=True)
    interface_status = Column(String(256),nullable=True)
    interfaces = Column(String(2500),nullable=True)
    mac_address = Column(String(150),nullable=True)
    ip_id = Column(Integer,
                   ForeignKey('ip_table.ip_id')
                   ,nullable=True
                   )
    ipam_device_id = Column(Integer,ForeignKey('ipam_devices_fetch_table.ipam_device_id'),nullable=True)

    creation_date = Column(DateTime,default=datetime.now())
    modification_date = Column(DateTime,default=datetime.now())

    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = str(value)
        return data
class ADD_DNS_TABLE(Base):
    __tablename__ = 'add_dns_table'
    dns_id = Column(Integer, primary_key=True)

    server_name = Column(String(50))
    username = Column(String(50))
    password = Column(String(50))

    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key, value in data.items():
                if isinstance(value, datetime):
                    data[key] = str(value)
        return data

class DnsServerTable(Base):
    __tablename__ = 'dns_server_table'
    dns_server_id = Column(Integer,primary_key=True,autoincrement=True)
    ip_address = Column(String(50))
    user_name = Column(String(50))
    password = Column(String(50))
    server_name = Column(String(256),nullable=True)
    type = Column(String(256),nullable=True)
    status = Column(String(256),nullable = True)
    number_of_zones = Column(Integer,nullable=True)
    user_id = Column(Integer,nullable=True)

    creation_date = Column(DateTime,default = datetime.now())
    modification_date = Column(DateTime,default = datetime.now() )

    ip_table = Column(Integer,
                      ForeignKey('ip_table.ip_id')
                      ,nullable=True
                      )

    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = str(value)
        return data

class DnsZonesTable(Base):
    __tablename__ = 'dns_zone_table'
    dns_zone_id = Column(Integer,primary_key=True,autoincrement=True)
    zone_name = Column(String(256),nullable=True)
    zone_type = Column(String(256),nullable=True)
    lookup_type = Column(String(256),nullable=True)
    zone_status = Column(String(256),nullable=True)
    number_of_zones = Column(Integer, nullable=True)
    dns_server_id = Column(Integer,
                           ForeignKey('dns_server_table.dns_server_id')
                           )
    creation_date = Column(DateTime,default = datetime.now())
    modification_date = Column(DateTime,default = datetime.now())
    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = str(value)
        return data


class DnsRecordTable(Base):
    __tablename__ = 'dns_record_table'
    dns_record_id = Column(Integer,primary_key=True,autoincrement=True)
    server_name = Column(String(256),nullable=True)
    server_ip = Column(String(256),nullable=True)
    dns_zone_id = Column(Integer,
                         ForeignKey('dns_zone_table.dns_zone_id')
                         ,nullable=False
                         )
    creation_date = Column(DateTime,default = datetime.now())
    modification_date = Column(DateTime,default = datetime.now())

    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = str(value)
        return data


class F5(Base):
    __tablename__ = 'f5'
    f5_id = Column(Integer, primary_key=True)
    ip_address = Column(String(50))
    device_name = Column(String(50))
    vserver_name = Column(String(500))
    vip = Column(String(50))
    pool_name = Column(String(500))
    pool_member = Column(String(500))
    node = Column(String(500))
    service_port =Column(String(500))
    monitor_value = Column(String(500))
    monitor_status = Column(String(500))
    lb_method = Column(String(500))
    creation_date = Column(DateTime, default=datetime.now())
    modification_date = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now())
    created_by = Column(String(50))
    modified_by = Column(String(50))

    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = str(value)
        return data


class FIREWALL_VIP(Base):
    __tablename__ = 'firewall_vip'
    firewall_vip_id = Column(Integer, primary_key=True)
    ip_address = Column(String(50))
    device_name = Column(String(50))
    internal_ip = Column(String(500))
    vip = Column(String(50))
    sport = Column(String(500))
    dport = Column(String(500))
    extintf = Column(String(500))
    creation_date = Column(DateTime, default=datetime.now())
    modification_date = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now())

    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = str(value)
        return data