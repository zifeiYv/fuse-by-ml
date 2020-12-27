# -*- coding: utf-8 -*-
data_source_config = {
    # 'db_type': 'oracle',
    # 'config': {
    #     'user': 'tc',
    #     'password': 'tc',
    #     'host': '191.168.7.150',
    #     'port': 1521,
    #     "service_name": 'bj',
    #     'schema': 'tc'
    # }
    'db_type': 'mysql',
    'config': {
        'user': 'tc',
        'password': 'tc',
        'host': '191.168.7.150',
        'port': 1521,
        'db': 'tc'
    }
}

# 融合训练及预测所用到的表
table_names = [
    'dw_bdz_yx', 'bdz_xlxd_yx', 'dw_xlxd_yx', 'xlxd_yxbyq_yx', 'dw_yxbyq_yx',
    'substation_sc', 'substation_tenkvline_sc', 'line_sc', 'tenkvline_distran_sc', 'power_transformer_sc',
    'net_s_substation_gis', 'substation_tenkvline1_gis', 'dm_grid_m_net_df_branch_kx_gis',
    'grid_tenkvline_distran_rela1_gis', 'net_ds_trans_gis'
]

# 用于测试模型效果的数据
test_data = {
    'yx': {'dw_xlxd_yx': ['1148043', '1148045', '1148044', '2500006302', '2500006289', '324712', '324914', '2500006318',
                          '796782',
                          '2500006339', '2500006454', '2500006338', '2500006340']},
    'pms': {
        'line_sc': ['26DKX-526', '26DKX-546', '26DKX-547', '26DKX-1154', '26DKX-1424', '26DKX-887', '26DKX-952',
                    '26DKX-1385',
                    '26DKX-1422', '26DKX-1381', '26DKX-457']},
    'gis': {'dm_grid_m_net_df_branch_kx_gis': ['526', '546', '547', '1154', '1424', '887', '952', '1385']}
}
