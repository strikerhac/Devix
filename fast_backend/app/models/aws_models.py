from sqlalchemy import ForeignKey, Column, Boolean, Integer, String, DateTime, Date
from datetime import datetime

from app.core.config import Base

class AWS_CREDENTIALS(Base):
    __tablename__ = 'aws_credentials_table'
    access_key = Column(String(150), primary_key=True)
    secrete_access_key = Column(String(150))
    account_label = Column(String(100))


class AWS_EC2(Base):
    __tablename__ = 'aws_ec2_table'
    id = Column(Integer, primary_key=True)
    instance_id = Column(String(100))
    instance_name =  Column(String(100))
    region_id = Column(String(100))
    monitoring_status = Column(String(150), default='Disabled')
    access_key = Column(String(150), ForeignKey(
        'aws_credentials_table.access_key'))


class AWS_S3(Base):
    __tablename__ = 'aws_s3_table'
    id = Column(Integer, primary_key=True)
    bucket_name = Column(String(100))
    region_id = Column(String(100))
    monitoring_status = Column(String(150), default='Disabled')
    access_key = Column(String(150), ForeignKey(
        'aws_credentials_table.access_key'))


class AWS_ELB(Base):
    __tablename__ = 'aws_elb_table'
    id = Column(Integer, primary_key=True)
    lb_name = Column(String(100))
    lb_type = Column(String(100))
    lb_scheme = Column(String(100))
    lb_arn = Column(String(300))
    region_id = Column(String(100))
    monitoring_status = Column(String(150), default='Disabled')
    access_key = Column(String(150), ForeignKey(
        'aws_credentials_table.access_key'))
