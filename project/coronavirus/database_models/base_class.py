#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr, MappedAsDataclass
from sqlalchemy.orm import DeclarativeMeta
from typing_extensions import Annotated

# 通用数据类主键
id_key = Annotated[int, mapped_column(primary_key=True, index=True, autoincrement=True, comment='主键id')]


class _BaseMixin:
    """
    Mixin 数据类

    Mixin: 一种面向对象编程概念, 使结构变得更加清晰, `Wiki <https://en.wikipedia.org/wiki/Mixin/>`__
    """

    id: Mapped[id_key] = mapped_column(init=False)
    create_user: Mapped[int] = mapped_column(comment='创建者')
    update_user: Mapped[Optional[int]] = mapped_column(comment='修改者')
    created_time: Mapped[datetime] = mapped_column(init=False, default=func.now(), comment='创建时间')
    updated_time: Mapped[Optional[datetime]] = mapped_column(init=False, onupdate=func.now(), comment='更新时间')


class MappedBase(DeclarativeBase):
    """
    声明性基类, 原始 DeclarativeBase 类, 作为所有基类或数据模型类的父类而存在

    `DeclarativeBase <https://docs.sqlalchemy.org/en/20/orm/declarative_config.html>`__
    `mapped_column() <https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column>`__
    """

    @declared_attr.directive
    def __tablename__(cls) -> Optional[str]:  # noqa
        return cls.__name__.lower()


class DataClassBase(MappedAsDataclass, MappedBase):
    """
    声明性数据类基类, 它将带有数据类集成, 允许使用更高级配置, 但你必须注意它的一些特性, 尤其是和 DeclarativeBase 一起使用时

    `MappedAsDataclass <https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#declaring-mapped-classes>`__
    """

    __abstract__ = True


class Base(_BaseMixin, MappedAsDataclass, MappedBase):
    """
    声明性 Mixin 数据类基类, 带有数据类集成, 并包含 MiXin 数据类基础表结构, 你可以简单的理解它为含有基础表结构的数据类基类
    """

    __abstract__ = True


def use_uuid() -> str:
    """
    使用uuid

    :return:
    """
    return uuid.uuid4().hex
