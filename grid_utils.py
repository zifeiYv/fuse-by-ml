# -*- coding: utf-8 -*-
#
# 电网相关的配置信息
#

# 各个主数据表的上下级表
table_relation = {
    'G_SUBS': {'father': '', 'child': 'G_LINE'},
    'G_LINE': {'father': 'G_SUBS', 'child': 'G_TRAN'},
    'G_TRAN': {'father': 'G_LINE', 'child': ''},
    'T_TX_ZNYC_DZ': {'father': '', 'child': 'T_TX_ZWYC_DKX'},
    'T_TX_ZWYC_DKX': {'father': 'T_TX_ZNYC_DZ', 'child': 'T_TX_ZNYC_PDBYQ,T_TX_ZWYC_ZSBYQ'},
    'T_TX_ZNYC_PDBYQ': {'father': 'T_TX_ZWYC_DKX', 'child': ''},
    'T_TX_ZWYC_ZSBYQ': {'father': 'T_TX_ZWYC_DKX', 'child': ''},
    'T_SB_ZNYC_DZ': {'father': '', 'child': 'T_SB_ZWYC_DKX'},
    'T_SB_ZWYC_DKX': {'father': 'T_SB_ZNYC_DZ', 'child': 'T_SB_ZNYC_PDBYQ,T_SB_ZWYC_ZSBYQ'},
    'T_SB_ZNYC_PDBYQ': {'father': 'T_SB_ZWYC_DKX', 'child': ''},
    'T_SB_ZWYC_ZSBYQ': {'father': 'T_SB_ZWYC_DKX', 'child': ''}
}

# 各个主数据表的关键属性
table_properties = {
    'G_SUBS': {'systemType': 'yx', 'idColName': 'SUBS_ID',
               'nameCol': 'SUBS_NAME', 'addrCol': 'SUBS_ADDR',
               'voltCol': 'VOLT_CODE', 'orgCol': 'ORG_NO'},
    'G_LINE': {'systemType': 'yx', 'idColName': 'LINE_ID',
               'nameCol': 'LINE_NAME', 'addrCol': '',
               'voltCol': 'VOLT_CODE', 'orgCol': 'ORG_NO'},
    'G_TRAN': {'systemType': 'yx', 'idColName': 'EQUIP_ID',
               'nameCol': 'TRAN_NAME', 'addrCol': '',
               'voltCol': 'FRSTSIDE_VOLT_CODE', 'orgCol': 'ORG_NO'},
    'T_TX_ZNYC_DZ': {'systemType': 'gis', 'idColName': 'OID',
                     'nameCol': 'SBMC', 'addrCol': '',
                     'voltCol': 'DYDJ', 'orgCol': 'YXDW'},
    'T_TX_ZWYC_DKX': {'systemType': 'gis', 'idColName': 'OID',
                      'nameCol': 'SBMC', 'addrCol': '',
                      'voltCol': 'DYDJ', 'orgCol': 'YXDW'},
    'T_TX_ZWYC_ZSBYQ': {'systemType': 'gis', 'idColName': 'OID',
                        'nameCol': 'SBMC', 'addrCol': '',
                        'voltCol': 'DYDJ', 'orgCol': 'YXDW'},
    'T_TX_ZNYC_PDBYQ': {'systemType': 'gis', 'idColName': 'OID',
                        'nameCol': 'SBMC', 'addrCol': '',
                        'voltCol': 'DYDJ', 'orgCol': 'YXDW'},
    'T_SB_ZNYC_DZ': {'systemType': 'pms', 'idColName': 'OBJ_ID',
                     'nameCol': 'BDZMC', 'addrCol': 'ZZ',
                     'voltCol': 'DYDJ', 'orgCol': 'YWDW'},
    'T_SB_ZWYC_DKX': {'systemType': 'pms', 'idColName': 'OBJ_ID',
                      'nameCol': 'XLMC', 'addrCol': '',
                      'voltCol': 'DYDJ', 'orgCol': 'YWDW'},
    'T_SB_ZWYC_ZSBYQ': {'systemType': 'pms', 'idColName': 'OBJ_ID',
                        'nameCol': 'SBMC', 'addrCol': '',
                        'voltCol': 'DYDJ', 'orgCol': 'YWDW'},
    'T_SB_ZNYC_PDBYQ': {'systemType': 'pms', 'idColName': 'OBJ_ID',
                        'nameCol': 'SBMC', 'addrCol': '',
                        'voltCol': 'DYDJ', 'orgCol': 'YWDW'}
}

# 各个主数据表之间的关联关系
tab_conn_rel = {
    'G_SUBS-G_LINE': [['G_SUBS', 'G_SUBS_LINE_RELA', 'SUBS_ID', 'SUBS_ID'],
                      ['G_SUBS_LINE_RELA', 'G_LINE', 'LINE_ID', 'LINE_ID']],
    'G_LINE-G_SUBS': [['G_LINE', 'G_SUBS_LINE_RELA', 'LINE_ID', 'LINE_ID'],
                      ['G_SUBS_LINE_RELA', 'G_SUBS', 'SUBS_ID', 'SUBS_ID']],
    'G_LINE-G_TRAN': [['G_LINE', 'G_LINE_TG_RELA', 'LINE_ID', 'LINE_ID'],
                      ['G_LINE_TG_RELA', 'G_TRAN', 'TG_ID', 'TG_ID']],
    'G_TRAN-G_LINE': [['G_TRAN', 'G_LINE_TG_RELA', 'TG_ID', 'TG_ID'],
                      ['G_LINE_TG_RELA', 'G_LINE', 'LINE_ID', 'LINE_ID']],
    'T_TX_ZNYC_DZ-T_TX_ZWYC_DKX': [['T_TX_ZNYC_DZ', 'T_TX_ZWYC_DKX', 'SBID', 'QSDZ']],
    'T_TX_ZWYC_DKX-T_TX_ZNYC_DZ': [['T_TX_ZWYC_DKX', 'T_TX_ZNYC_DZ', 'QSDZ', 'SBID']],
    'T_TX_ZWYC_DKX-T_TX_ZNYC_PDBYQ': [['T_TX_ZWYC_DKX', 'T_TX_ZNYC_PDBYQ', 'OID', 'SSDKX']],
    'T_TX_ZNYC_PDBYQ-T_TX_ZWYC_DKX': [['T_TX_ZNYC_PDBYQ', 'T_TX_ZWYC_DKX', 'SSDKX', 'OID']],
    'T_TX_ZWYC_DKX-T_TX_ZWYC_ZSBYQ': [['T_TX_ZWYC_DKX', 'T_TX_ZWYC_ZSBYQ', 'OID', 'SSDKX']],
    'T_TX_ZWYC_ZSBYQ-T_TX_ZWYC_DKX': [['T_TX_ZWYC_ZSBYQ', 'T_TX_ZWYC_DKX', 'SSDKX', 'OID']],
    'T_SB_ZNYC_DZ-T_SB_ZWYC_DKX': [['T_SB_ZNYC_DZ', 'T_SB_ZWYC_DKX', 'OBJ_ID', 'QSDZ']],
    'T_SB_ZWYC_DKX-T_SB_ZNYC_DZ': [['T_SB_ZWYC_DKX', 'T_SB_ZNYC_DZ', 'QSDZ', 'OBJ_ID']],
    'T_SB_ZWYC_DKX-T_SB_ZNYC_PDBYQ': [['T_SB_ZWYC_DKX', 'T_SB_ZNYC_PDBYQ', 'OBJ_ID', 'SSDKX']],
    'T_SB_ZNYC_PDBYQ-T_SB_ZWYC_DKX': [['T_SB_ZNYC_PDBYQ', 'T_SB_ZWYC_DKX', 'SSDKX', 'OBJ_ID']],
    'T_SB_ZWYC_DKX-T_SB_ZWYC_ZSBYQ': [['T_SB_ZWYC_DKX', 'T_SB_ZWYC_ZSBYQ', 'OBJ_ID', 'SSDKX']],
    'T_SB_ZWYC_ZSBYQ-T_SB_ZWYC_DKX': [['T_SB_ZWYC_ZSBYQ', 'T_SB_ZWYC_DKX', 'SSDKX', 'OBJ_ID']]
}

# 电压等级在不同系统中的映射关系, 'pms': 'cms'
volt_mapping = {
    '01': ['AC00062'], '02': ['AC00122'], '03': ['AC00242'], '04': ['AC00362'],
    '05': ['AC00482'], '06': ['AC01102'], '07': ['AC02202'], '09': ['AC06602'],
    '10': ['AC10002'], '11': ['AC06002'], '12': ['AC07502'], '13': ['AC15002'],
    '14': ['AC30002'], '15': ['AC25002'], '20': ['AC00031'], '21': ['AC00061'],
    '22': ['AC00101'], '24': ['AC00201'], '25': ['AC00351'], '30': ['AC00661'],
    '32': ['AC01101'], '33': ['AC02201'], '34': ['AC03301'], '35': ['AC05001'],
    '36': ['AC07501'], '37': ['AC10001'], '51': ['DC00062'], '52': ['DC00122'],
    '53': ['DC00242'], '54': ['DC00362'], '55': ['DC00482'], '56': ['DC01102'],
    '60': ['DC02202'], '70': ['DC06002'], '71': ['DC07502'], '72': ['DC15002'],
    '73': ['DC30002'], '83': ['DC05001']
}
