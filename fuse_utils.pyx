# -*- coding: utf-8 -*-
"""
用于特征工程及建模的一些函数
"""
import cx_Oracle
import pandas as pd
import numpy as np
from utils import Entity, Similarities, _compute_name_fea
from grid_utils_yn import table_properties, volt_mapping, table_relation, tab_conn_rel
import pymysql


def return_mysql_conn(data_source):
    data_source = data_source['config']
    conn = pymysql.connect(**data_source)
    return conn


def get_data_from_db(data_source, tabs, logger):
    """从数据源读取指定表的数据。

    只适用于最初采用Oracle数据进行验证，未来将会被移除。

    Args:
        logger:
        data_source(dic): 数据源连接信息
        tabs(list): 存储表名的列表

    Returns:

    """
    data_dict = {}
    db_type = data_source['db_type'].upper()
    if db_type == 'ORACLE':
        logger.info("Reading Oracle data...")
        data_source = data_source['config']
        user = data_source['user']
        passwd = data_source['password']
        schema = data_source['schema']
        dsn = cx_Oracle.makedsn(host=data_source['host'], port=1521, service_name='bj')
        connection = cx_Oracle.connect(user, passwd, dsn)
        assert connection.ping() is None, "无法连接数据源"
        for tab in tabs:
            if tab == 'G_TRAN':
                value = pd.read_sql('select * from ' + schema + '.' + tab + ' where PUB_PRIV_FLAG=\'1\'', connection)
            elif tab == 'T_TX_ZNYC_PDBYQ':
                value = pd.read_sql('select * from ' + schema + '.' + tab + ' where SBZLX=30200002', connection)
            elif tab == 'T_TX_ZWYC_ZSBYQ':
                value = pd.read_sql('select * from ' + schema + '.' + tab + ' where SBZLX=11000000', connection)
            else:
                value = pd.read_sql('select * from ' + schema + '.' + tab, connection)
            data_dict[tab] = value
        logger.info("数据读取结束")
    else:  # TODO
        logger.error("unsupported database type")
        pass
    return data_dict


def compare_volt(data_dict, entity1, entity2):
    """比较两个实体的电压等级是否一致。

    Args:
        data_dict(dict):
        entity1(Entity):
        entity2(Entity):

    Returns:

    """
    tab1, tab2 = entity1.ent_tab, entity2.ent_tab
    id1, id2 = entity1.ent_id, entity2.ent_id
    df1, df2 = data_dict[tab1], data_dict[tab2]
    volt_field1 = table_properties[tab1]['voltCol']
    volt_field2 = table_properties[tab2]['voltCol']
    id_field1 = table_properties[tab1]['idColName']
    id_field2 = table_properties[tab2]['idColName']

    df1[id_field1] = df1[id_field1].astype(str)
    df2[id_field2] = df2[id_field2].astype(str)
    row1 = df1[df1[id_field1] == id1]
    row2 = df2[df2[id_field2] == id2]
    volt1 = str(row1[volt_field1].tolist()[0])
    volt2 = str(row2[volt_field2].tolist()[0])

    flag1 = (volt1 != '' and volt1.upper() != 'NONE' and volt1.upper() != 'NAN')
    flag2 = (volt2 != '' and volt2.upper() != 'NONE' and volt2.upper() != 'NAN')
    if flag1 and flag2:
        volt1 = volt1.replace(' ', '')
        volt2 = volt2.replace(' ', '')
        if volt1.startswith('AC') or volt1.startswith('DC'):
            volt2_mapped = volt_mapping.get(volt2)
            if not volt2_mapped:
                return 0
            else:
                volt2 = volt2_mapped[0]
                if volt2 == volt1:
                    return 1
                else:
                    return 0
        else:
            volt1_mapped = volt_mapping.get(volt1)
            if not volt1_mapped:
                return 0
            else:
                volt1 = volt1_mapped
                if volt1 == volt2:
                    return 1
                else:
                    return 0
    else:
        return 0


def get_text_fea(data_dict, entity1, entity2):
    """对于给定的两个实体，计算其文本特征。

    Args:
        data_dict(dict):
        entity1(Entity):
        entity2(Entity):

    Returns:

    """
    tab1, tab2 = entity1.ent_tab, entity2.ent_tab
    id_field1 = table_properties[tab1]['idColName']
    id_field2 = table_properties[tab2]['idColName']
    name_field1 = table_properties[tab1]['nameCol']
    name_field2 = table_properties[tab2]['nameCol']
    df1, df2 = data_dict[tab1], data_dict[tab2]
    id1, id2 = entity1.ent_id, entity2.ent_id

    row1 = df1[df1[id_field1] == id1]
    row2 = df2[df2[id_field2] == id2]
    len1 = len(row1)
    len2 = len(row2)

    total_len = len1 + len2
    if total_len < 2:
        return [0, 0, 0, 0.7, 1, 0, 1, 0]
    else:
        name1 = row1[name_field1].tolist()[0]
        name2 = row2[name_field2].tolist()[0]
        # # 特殊化处理
        # if name1.startswith('电网_'):
        #     name1 = name1[3:len(name1)]
        # if name2.startswith('电网_'):
        #     name2 = name2[3:len(name2)]
        #
        return _compute_name_fea(name1, name2)


def get_connected_value(from_id, inner_table, connection):
    """根据父实体的id，通过中间表，获取子实体的id列表。

    Args:
        from_id(str):
        inner_table(str):
        connection:

    Returns:

    """
    with connection.cursor() as cr:
        cr.execute(f'select to_id from {inner_table} where from_id="{from_id}"')
    value = cr.fetchall()
    if not value:
        return []
    else:
        return list(map(lambda x: x[0], value))


def get_children(entity, connection):
    """根据输入的实体，获取其子节点实体。

    Args:
        connection:
        entity(Entity):

    Returns:

    """
    id_ = entity.ent_id
    tab = entity.ent_tab
    child_tab = table_relation[tab]['child']
    path = tab + '-' + child_tab
    conn_list = tab_conn_rel[path]
    inner_tab = conn_list[0][1]
    values = get_connected_value(id_, inner_tab, connection)
    return child_tab, values


def get_father(data_dict, entity):
    """根据输入的实体，获取其父节点实体。

    Args:
        data_dict(dict):
        entity(Entity):

    Returns:

    """
    id_ = entity.ent_id
    tab = entity.ent_tab
    fa_tab = table_relation[tab]['father']
    fa_id_field = table_properties[fa_tab]['idColName']
    fa_df = data_dict[fa_tab]
    path = tab + '-' + fa_tab
    conn_list = tab_conn_rel[path]

    df1 = data_dict[tab]
    id_filed = table_properties[tab]['idColName']
    former_field = conn_list[0][2]
    latter_tab = conn_list[0][1]
    latter_field = conn_list[0][2]
    df2 = data_dict[latter_tab]

    values1 = get_connected_value(df1, id_filed, [id_], former_field, df2, latter_field)
    if len(conn_list) == 1:  # No inner table
        if len(values1) == 0:
            return fa_tab, None
        else:
            fa_ids = fa_df[fa_df[latter_field] == values1[0]][fa_id_field].tolist()[0]
            return fa_tab, fa_ids
    else:  # One inner table
        df1 = df2
        id_filed = latter_field
        former_field = conn_list[1][2]
        df2 = data_dict[conn_list[1][1]]
        latter_field = conn_list[1][3]
        values1 = get_connected_value(df1, id_filed, values1, former_field, df2, latter_field)
        if len(values1) == 0:
            return fa_tab, None
        else:
            fa_ids = fa_df[fa_df[latter_field] == values1[0]][fa_id_field].tolist()[0]
            return fa_tab, fa_ids


def get_child_name(child_info, connection):
    """根据子节点的信息，获取其名称。

    Args:
        child_info(tuple):
        connection:

    Returns:

    """
    table, lists = child_info
    id_filed = table_properties[table]['idColName']
    name_filed = table_properties[table]['nameCol']
    sql = f'select {name_filed} from {table} where {id_filed} in {tuple(lists)}'
    if len(lists) == 1:
        sql = sql[:-2] + ')'
    elif not lists:
        return []
    print(sql)
    values = pd.read_sql(sql, connection)
    return values.iloc[:, 0].tolist()


def _get_name_sim(name1, name2, type_):
    """获取两个名称字符串的相似度。

    Args:
        name1(str):
        name2(str):
        type_(str): 相似度算法

    Returns:

    """
    assert type_ in ['subseq', 'pinyin', 'edit']
    simmer = Similarities()

    lens = [len(name1), len(name2)]
    names = [name1, name2]
    ind = lens.index(max(lens))
    max_len = lens[ind]
    min_len = lens[1 - ind]
    long = names[ind]
    short = names[1 - ind]

    min_num = min(6, min_len)
    sim_matrix = np.zeros([min_num, max_len])
    for i in range(min_num):
        for j in range(max_len):
            if type_ == 'subseq':
                sim_matrix[i, j] = simmer.get_max_common_sub_seq_sim(short[i], long[j])
            elif type_ == 'pinyin':
                sim_matrix[i, j] = simmer.get_pinyin_max_common_sub_seq_sim(short[i], long[j])
            elif type_ == 'edit':
                sim_matrix[i, j] = simmer.get_edit_sim(short[i], long[j])
    return sim_matrix.max(axis=1).mean()


def get_child_fea(connection, child_info1, child_info2):
    """根据子节点的信息，计算其特征。

    Args:
        connection:
        child_info1(tuple):
        child_info2(tuple:

    Returns:

    """
    no_child_same = 0
    num_ratio = 0
    high_sim_child = 0
    sim1, sim2, sim3 = 0, 0, 0

    names1 = get_child_name(child_info1, connection)
    names2 = get_child_name(child_info2, connection)
    len1 = len(names1)
    len2 = len(names2)
    min_len = min(len1, len2)
    max_len = max(len1, len2)
    if max_len == 0:
        no_child_same = 1
    elif min_len == 0:
        num_ratio = 0
    else:
        num_ratio = min_len / max_len
        no_child_same = 1
        sim1 = _get_name_sim(names1, names2, 'subseq')
        sim2 = _get_name_sim(names1, names2, 'pinyin')
        sim3 = _get_name_sim(names1, names2, 'edit')
        mean_sim = np.mean([sim1, sim2, sim3])
        if mean_sim > 0.85:
            high_sim_child = 1
    return [num_ratio, no_child_same, high_sim_child, sim1, sim2, sim3]


def get_numeric_fea(data_dict, entity1, entity2):
    """计算两个实体的非字符类特征。

    Args:
        data_dict(dict):
        entity1(Entity):
        entity2(Entity):

    Returns:

    """
    return [0]
    # return [compare_volt(data_dict, entity1, entity2)]


def get_all_fea(data_dict, entity1, entity2, data_source):
    """对于来自不同系统的两个实体，计算其所有的特征。

    Args:
        data_dict(dict):
        entity1(Entity):
        entity2(Entity):
        data_source:

    Returns:

    """
    connection = return_mysql_conn(data_source)

    text_fea = get_text_fea(data_dict, entity1, entity2)

    child_info1 = get_children(entity1, connection)
    child_info2 = get_children(entity2, connection)
    child_fea = get_child_fea(connection, child_info1, child_info2)

    numeric_fea = get_numeric_fea(data_dict, entity1, entity2)

    all_fea = text_fea + child_fea + numeric_fea

    columns = ['nodeSim1', 'nodeSim2', 'nodeSim3', 'lenRatio', 'hasNumSame',
               'numSame', 'hasLetterSame', 'letterSame', 'childNumRatio',
               'noChildrenSame', 'hasHighSimChild', 'childSim1',
               'childSim2', 'childSim3', 'voltSame']
    return pd.DataFrame([all_fea], columns=columns)


def get_all_train_fea(data_dict, train_df, data_source):
    """处理所有的训练数据的特征。

    Args:
        data_dict(dict):
        train_df(pd.DataFrame): 训练数据集
        data_source:

    Returns:

    """
    connection = return_mysql_conn(data_source)
    fea_list = []
    for i in range(train_df.shape[0]):
        row_data = train_df.iloc[i]
        tab1, tab2 = row_data['table1'], row_data['table2']
        label = row_data['label']
        id1, id2 = row_data['id1'], row_data['id2']
        entity1 = Entity('yx', 'tran', id1, tab1)
        entity2 = Entity('pms', 'tran', id2, tab2)
        # 文本特征
        text_fea = get_text_fea(data_dict, entity1, entity2)

        # 子实体的特征
        child_info1, child_info2 = get_children(entity1, connection), get_children(entity2, connection)
        print(child_info1)
        print(child_info2)
        children_fea = get_child_fea(connection, child_info1, child_info2)

        # 数值类特征
        numeric_fea = get_numeric_fea(data_dict, entity1, entity2)

        all_fea = text_fea + children_fea + numeric_fea
        all_fea.append(label)
        fea_list.append(all_fea)
    columns = ['nodeSim1', 'nodeSim2', 'nodeSim3', 'lenRatio', 'hasNumSame',
               'numSame', 'hasLetterSame', 'letterSame', 'childNumRatio', 'noChildrenSame',
               'hasHighSimChild', 'childSim1', 'childSim2', 'childSim3', 'voltSame',
               'label']
    return pd.DataFrame(fea_list, columns=columns)
