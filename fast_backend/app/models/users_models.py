from app.utils.db_utils import *
from app.core.config import *
from sqlalchemy import ForeignKey,String,Boolean,Column,Integer,DateTime
from datetime import datetime
from app.models.base_model import *

"""
User Models
License Models
Login Model
End User Models
"""

class EndUserTable(Base):
    __tablename__ = 'end_user_table'
    end_user_id = Column(Integer,primary_key=True,autoincrement=True)
    company_name = Column(String(500),nullable=False)
    po_box = Column(String(50),nullable=True)
    address = Column(String(2500),nullable = True)
    street_name = Column(String(500),nullable=True)
    city = Column(String(500),nullable=True)
    country = Column(String(500),nullable=True)
    contact_person = Column(String(500),nullable=True)
    contact_number = Column(String(500),nullable=True)
    email = Column(String(500),nullable=True)
    domain_name = Column(String(500),nullable=True)
    industry_type = Column(String(500),nullable=True)
    creation_date = Column(DateTime,default=datetime.now())
    modification_date = Column(DateTime,default=datetime.now())
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



class LicenseVerfificationModel(Base):
    __tablename__ = 'license_verification_table'
    license_verfification_id = Column(Integer,primary_key=True,autoincrement=True)
    license_generate_key = Column(String(2500),nullable=False)
    license_verfification_key = Column(String(2500),nullable=False)
    start_date = Column(DateTime,nullable=False)
    end_date = Column(DateTime,nullable=False)
    verification = Column(String(500),nullable=False)
    device_onboard_limit = Column(Integer,nullable=False)
    end_user_id = Column(Integer,ForeignKey('end_user_table.end_user_id',ondelete='CASCADE',onupdate='CASCADE'),nullable=False)
    creation_date = Column(DateTime,default=datetime.now())
    modification_date = Column(DateTime,default=datetime.now())
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class DevicesLiscenceTableModel(Base):
    __tablename__ = 'devices_liscence_table'
    device_license_id = Column(Integer,primary_key=True,autoincrement=True)
    rfs_date = Column(DateTime)
    serial_number = Column(String(500),nullable=True)
    license_verfification_id = Column(Integer,ForeignKey('license_verification_table.license_verfification_id',onupdate='CASCADE',ondelete='CASCADE'),nullable=False)
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



class UserRoleTableModel(Base):
    __tablename__ = 'user_role_table'
    role_id = Column(Integer,primary_key=True,autoincrement=True)
    role = Column(String(50),nullable=False)
    configuration = Column(String(5000),nullable=True)
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserTableModel(BaseModel):
    __tablename__ = 'user_table'
    role = Column(String(255), nullable=True)
    end_user_id = Column(Integer,ForeignKey('end_user_table.end_user_id',onupdate='CASCADE',ondelete='CASCADE'),nullable=False)
    name = Column(String(500),nullable=True)
    email = Column(String(500),nullable=True)
    password = Column(String(500),nullable=True)
    status = Column(String(500),nullable=True)
    teams = Column(String(500),nullable=True)
    user_name = Column(String(500),nullable=True)
    account_type = Column(String(100),nullable=True)
    last_login = Column(DateTime,default=datetime.now(),nullable=True)
    user_token = Column(String(255), unique=True, index=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Login_Activity_Table(Base):
    __tablename__ = 'login_activity_table'

    login_id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey('user_table.user_id',onupdate='CASCADE',ondelete='CASCADE'),nullable=False)
    operation = Column(String(50), nullable=True)
    status = Column(String(50), nullable=True)
    description = Column(String(200), nullable=True)
    timestamp = Column(DateTime, default=datetime.now(), nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class password_reset_otp_table(Base):
    __tablename__ = 'password_reset_otp_table'

    otp_id = Column(Integer,primary_key=True,autoincrement=True)
    generated_otp_code = Column(String(15),nullable=False)
    user_otp_code = Column(String(15),nullable=True)
    user_name = Column(String(55),nullable=False)
    otp_status = Column(String(45))
    creation_date = Column(DateTime,default=datetime.now())
    modification_date = Column(DateTime,default=datetime.now())