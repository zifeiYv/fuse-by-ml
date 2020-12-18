# -*- coding: utf-8 -*-
data_source_config = {
    'type': 'oracle',
    'user': 'tc',
    'password': 'tc',
    'host': '191.168.7.150',
    'port': 1521,
    "service_name": 'bj',
    'schema': 'tc'
}

table_name = ['G_SUBS', 'G_LINE', 'G_TRAN', 'G_SUBS_LINE_RELA', 'G_LINE_TG_RELA',
              'T_TX_ZNYC_DZ', 'T_TX_ZWYC_DKX', 'T_TX_ZNYC_PDBYQ', 'T_TX_ZWYC_ZSBYQ',
              'T_SB_ZNYC_DZ', 'T_SB_ZWYC_DKX', 'T_SB_ZNYC_PDBYQ', 'T_SB_ZWYC_ZSBYQ']

# 用于测试模型效果的数据
test_data = {
    'yx': {'G_LINE': ['1148043', '1148045', '1148044', '2500006302', '2500006289', '324712', '324914', '2500006318',
                      '796782',
                      '2500006339', '2500006454', '2500006338', '2500006340']},
    'pms': {
        'T_SB_ZWYC_DKX': ['26DKX-526', '26DKX-546', '26DKX-547', '26DKX-1154', '26DKX-1424', '26DKX-887', '26DKX-952',
                          '26DKX-1385',
                          '26DKX-1422', '26DKX-1381', '26DKX-457']},
    'gis': {'T_TX_ZWYC_DKX': ['526', '546', '547', '1154', '1424', '887', '952', '1385']}
}
