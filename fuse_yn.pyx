# -*- coding: utf-8 -*-
"""
适用于云南项目现场的数据，MySQL数据库
"""
import pymysql
import pandas as pd
from grid_utils_yn import table_properties


def get_data_from_db(data_source, train_data, logger):
    """根据标注的训练集，从数据源读取指定表的指定数据。

    Args:
        data_source(dic): 数据源连接信息
        train_data(pd.DataFrame): 训练集

    Returns:

    """
    assert train_data.columns.to_list() == ['table1', 'table2', 'id1', 'id2', 'label'], 'Wrong format of train data'
    tables = [list(train_data.table1.value_counts().index),
              list(train_data.table2.value_counts().index)]
    check_tab_valid(tables[0], data_source)
    check_tab_valid(tables[1], data_source)
    data_ids = {}
    data_dict = {}
    for t1 in tables[0]:
        if not data_ids.get(t1):
            data_ids[t1] = train_data[train_data['table1'] == t1].id1.tolist()
        else:
            data_ids[t1].extend(train_data[train_data['table1'] == t1].id1.tolist())
    for t2 in tables[1]:
        if not data_ids.get(t2):
            data_ids[t2] = train_data[train_data['table2'] == t2].id2.tolist()
        else:
            data_ids[t2].extend(train_data[train_data['table2'] == t2].id2.tolist())

    db_type = data_source['db_type'].upper()
    if db_type == 'ORACLE':
        pass
    else:
        logger.info("Reading MySQL data...")
        data_source = data_source['config']
        connection = pymysql.connect(**data_source)
        assert connection.ping() is None, "无法连接数据源"
        for tab in data_ids:
            # 只获取标注数据集中的数据
            # todo：只获取可利用的字段，进一步减小内存占用
            value = pd.read_sql(f'select * from {tab} where {table_properties[tab]["idColName"]} '
                                f'in {tuple(data_ids[tab])}', connection)
            data_dict[tab] = value
    return data_dict


def check_tab_valid(table_list, data_source):
    db_type = data_source['db_type'].upper()
    if db_type == 'MYSQL':
        data_source = data_source['config']
        db = data_source['db']
        connection = pymysql.connect(**data_source)
        assert connection.ping() is None, "无法连接数据源"
        with connection.cursor() as cr:
            cr.execute(f'select table_name from information_schema.tables where table_schema = "{db}"')
            all_tables = cr.fetchall()
        all_tables = set([i[0] for i in all_tables])
        if set(table_list).union(all_tables) != all_tables:
            raise Exception
    else:
        raise Exception
