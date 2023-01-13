#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, date
from typing import Optional

from sqlalchemy import func, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship, Mapper, foreign

from .base_class import MappedBase as Base


# class User(DataClassBase):
#     """ 用户表 """
#     __tablename__ = 'sys_user'
#
#     id: Mapped[id_key] = mapped_column(init=False)
#     uid: Mapped[str] = mapped_column(String(50), init=False, insert_default=use_uuid, unique=True, comment='唯一标识')
#     username: Mapped[str] = mapped_column(String(20), unique=True, index=True, comment='用户名')
#     password: Mapped[str] = mapped_column(String(255), comment='密码')
#     email: Mapped[str] = mapped_column(String(50), unique=True, index=True, comment='邮箱')
#     is_superuser: Mapped[bool] = mapped_column(default=False, comment='超级权限')
#     is_active: Mapped[bool] = mapped_column(default=True, comment='用户账号状态')
#     avatar: Mapped[Optional[str]] = mapped_column(String(255), default=None, comment='头像')
#     mobile_number: Mapped[Optional[str]] = mapped_column(String(11), default=None, comment='手机号')
#     wechat: Mapped[Optional[str]] = mapped_column(String(20), default=None, comment='微信')
#     qq: Mapped[Optional[str]] = mapped_column(String(10), default=None, comment='QQ')
#     blog_address: Mapped[Optional[str]] = mapped_column(String(255), default=None, comment='博客地址')
#     introduction: Mapped[Optional[str]] = mapped_column(LONGTEXT, default=None, comment='自我介绍')
#     time_joined: Mapped[datetime] = mapped_column(init=False, default=func.now(), comment='注册时间')
#     last_login: Mapped[Optional[datetime]] = mapped_column(init=False, onupdate=func.now(), comment='上次登录')

class City(Base):
    __tablename__ = 'city'  # 数据表的表名
    id = Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    province = Mapped[str] = mapped_column(String(100), unique=True, nullable=False, comment='省/直辖市')
    country = Mapped[str] = mapped_column(String(100), nullable=False, comment="国家")
    country_code = Mapped[str] = mapped_column(String(100), nullable=False, comment="国家代码")
    country_population = Mapped[int] = mapped_column(nullable=False, comment="国家人口")
    # Data是关联的类名,参数back_populates来指定反向访问的属性名
    data = relationship('Data', back_populates='city')

    created_at = Mapped[datetime] = mapped_column(server_default=func.now(), comment='创建时间')
    updated_at = Mapped[datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now(), comment='更新时间')
    # 默认是正序，倒序加上.desc()方法
    __mapper_args__ = {"order_by": country_code}

    def __repr__(self):
        return f'{self.country}_{self.province}'


class Data(Base):
    __tablename__ = 'data'
    id = Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    city_id = Mapped[int] = mapped_column(foreign('city.id'), comment='所属省/直辖市')
    date = Mapped[date] = mapped_column(nullable=False, comment='数据日期')
    confirmed = Mapped[int] = mapped_column(default=0, nullable=False, comment='确诊的数量')
    deaths = Mapped[int] = mapped_column(default=0, nullable=False, comment='死亡的数量')
    recovered = Mapped[int] = mapped_column(default=0, nullable=False, comment='痊愈的数量')
    # City是关联的类名,back_populates来指定反向访问的属性名
    city = relationship('city', back_populates='data')

    created_at = Mapped[datetime] = mapped_column(server_default=func.now(), comment='创建时间')
    updated_at = Mapped[datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now(), comment='更新时间')
    # 默认是正序，倒序加上.desc()方法
    __mapper_args__ = {"order_by": date.desc()}

    def __repr__(self):
        return f'{repr(self.date)}: 确证{self.confirmed}例'