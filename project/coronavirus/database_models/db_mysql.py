#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from urllib import parse

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


from .base_class import MappedBase as Base

""" 
说明：SqlAlchemy
"""

SQLALCHEMY_DATABASE_URL = f'mysql+asyncmy://root:xjxai@lj@127.0.0.1:' \
                          f'3306/test?charset="utf8"'

try:
    # 数据库引擎
    async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
    # log.success('数据库连接成功')
except Exception as e:
    print('❌ 数据库链接失败 {}', e)
    sys.exit()
else:
    async_db_session = async_sessionmaker(bind=async_engine, autoflush=False, expire_on_commit=False)


async def get_db() -> AsyncSession:
    """
    session 生成器

    :return:
    """
    session = async_db_session()
    try:
        yield session
    except Exception as se:
        await session.rollback()
        raise se
    finally:
        await session.close()


# async def create_table():
#     """
#     创建数据库表
#     """
#     async with async_engine.begin() as coon:
#         await coon.run_sync(MappedBase.metadata.create_all)

