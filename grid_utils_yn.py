# -*- coding: utf-8 -*-
#
# 电网相关的配置信息
#

# 各个主数据表的上下级表
table_relation = {
    'dw_bdz_yx': {'father': '', 'child': 'dw_xlxd_yx'},
    'dw_xlxd_yx': {'father': 'dw_bdz_yx', 'child': 'dw_yxbyq_yx'},
    'dw_yxbyq_yx': {'father': 'dw_xlxd_yx', 'child': ''},

    'substation_sc': {'father': '', 'child': 'line_sc'},
    'line_sc': {'father': 'substation_sc', 'child': 'power_transformer_sc'},
    'power_transformer_sc': {'father': 'line_sc', 'child': ''},

    'net_s_substation_gis': {'father': '', 'child': 'dm_grid_m_net_df_branch_kx_gis'},
    'dm_grid_m_net_df_branch_kx_gis': {'father': 'net_s_substation_gis', 'child': 'net_ds_trans_gis'},
    'net_ds_trans_gis': {'father': 'dm_grid_m_net_df_branch_kx_gis', 'child': ''},
}

# 各个主数据表的关键属性
table_properties = {
    'dw_bdz_yx': {'systemType': 'yx', 'idColName': 'bdzbh',
                  'nameCol': 'bdzmc', 'addrCol': '',
                  'voltCol': 'dydjdm', 'orgCol': 'gddwbm'},
    'substation_sc': {'systemType': 'sc', 'idColName': 'id',
                      'nameCol': 'fl_name', 'addrCol': 'address',
                      'voltCol': 'base_voltage_id', 'orgCol': ''},
    'net_s_substation_gis': {'systemType': 'gis', 'idColName': 'id',
                             'nameCol': 'fl_name', 'addrCol': 'address',
                             'voltCol': 'base_voltage_id', 'orgCol': 'mrid'},

    'dw_xlxd_yx': {'systemType': 'yx', 'idColName': 'xlbh',
                   'nameCol': 'xlmc', 'addrCol': '',
                   'voltCol': 'dydjdm', 'orgCol': ''},
    'line_sc': {'systemType': 'sc', 'idColName': 'id',
                'nameCol': 'fl_name', 'addrCol': '',
                'voltCol': 'base_voltage_id', 'orgCol': ''},
    'dm_grid_m_net_df_branch_kx_gis': {'systemType': 'gis', 'idColName': 'id',
                                       'nameCol': 'fl_name', 'addrCol': '',
                                       'voltCol': 'base_voltage_id', 'orgCol': 'mrid'},

    'dw_yxbyq_yx': {'systemType': 'yx', 'idColName': 'sbbs',
                    'nameCol': 'mc', 'addrCol': '',
                    'voltCol': '', 'orgCol': 'gddwbm'},

    'power_transformer_sc': {'systemType': 'sc', 'idColName': 'id',
                             'nameCol': 'fl_name', 'addrCol': 'zlocation',
                             'voltCol': 'base_voltage_id', 'orgCol': ''},

    'net_ds_trans_gis': {'systemType': 'gis', 'idColName': 'id',
                         'nameCol': 'fl_name', 'addrCol': '',
                         'voltCol': 'base_voltage_id', 'orgCol': 'mrid'}
}
table_names = [
    'dw_bdz_yx', 'bdz_xlxd_yx', 'dw_xlxd_yx', 'xlxd_yxbyq_yx', 'dw_yxbyq_yx',
    'substation_sc', 'substation_tenkvline_sc', 'line_sc', 'tenkvline_distran_sc', 'power_transformer_sc',
    'net_s_substation_gis', 'substation_tenkvline1_gis', 'dm_grid_m_net_df_branch_kx_gis',
    'grid_tenkvline_distran_rela1_gis', 'net_ds_trans_gis'
]
# 各个主数据表之间的关联关系
tab_conn_rel = {
    'dw_bdz_yx-dw_xlxd_yx': [['dw_bdz_yx', 'bdz_xlxd_yx', 'bdzbh', 'from_id'],
                             ['bdz_xlxd_yx', 'dw_xlxd_yx', 'to_id', 'xlbh']],
    'dw_xlxd_yx-dw_bdz_yx': [['dw_xlxd_yx', 'bdz_xlxd_yx', 'xlbh', 'to_id'],
                             ['bdz_xlxd_yx', 'dw_bdz_yx', 'from_id', 'bdzbh']],
    'dw_xlxd_yx-dw_yxbyq_yx': [['dw_xlxd_yx', 'xlxd_yxbyq_yx', 'xlbh', 'from_id'],
                               ['xlxd_yxbyq_yx', 'dw_yxbyq_yx', 'to_id', 'sbbs']],
    'dw_yxbyq_yx-dw_xlxd_yx': [['dw_yxbyq_yx', 'xlxd_yxbyq_yx', 'sbbs', 'to_id'],
                               ['xlxd_yxbyq_yx', 'dw_xlxd_yx', 'from_id', 'xlbh']],

    'substation_sc-line_sc': [['substation_sc', 'substation_tenkvline_sc', 'id', 'from_id'],
                              ['substation_tenkvline_sc', 'line_sc', 'to_id', 'id']],
    'line_sc-substation_sc': [['line_sc', 'substation_tenkvline_sc', 'id', 'to_id'],
                              ['substation_tenkvline_sc', 'substation_sc', 'from_id', 'id']],
    'line_sc-power_transformer_sc': [['line_sc', 'tenkvline_distran_sc', 'id', 'from_id'],
                                     ['tenkvline_distran_sc', 'power_transformer_sc', 'to_id', 'id']],
    'power_transformer_sc-line_sc': [['power_transformer_sc', 'tenkvline_distran_sc', 'id', 'to_id'],
                                     ['tenkvline_distran_sc', 'line_sc', 'from_id', 'id']],

    'net_s_substation_gis-dm_grid_m_net_df_branch_kx_gis': [['net_s_substation_gis', 'substation_tenkvline1_gis',
                                                             'id', 'from_id'],
                                                            ['substation_tenkvline1_gis',
                                                             'dm_grid_m_net_df_branch_kx_gis', 'to_id', 'id']],
    'dm_grid_m_net_df_branch_kx_gis-net_s_substation_gis': [['dm_grid_m_net_df_branch_kx_gis',
                                                             'substation_tenkvline1_gis', 'id', 'to_id'],
                                                            ['substation_tenkvline1_gis', 'net_s_substation_gis',
                                                             'from_id', 'id']],
    'dm_grid_m_net_df_branch_kx_gis-net_ds_trans_gis': [['dm_grid_m_net_df_branch_kx_gis',
                                                         'grid_tenkvline_distran_rela1_gis', 'id', 'from_id'],
                                                        ['grid_tenkvline_distran_rela1_gis', 'net_ds_trans_gis',
                                                         'to_id', 'id']],
    'net_ds_trans_gis-dm_grid_m_net_df_branch_kx_gis': [['net_ds_trans_gis', 'grid_tenkvline_distran_rela1_gis',
                                                         'id', 'from_id'],
                                                        ['grid_tenkvline_distran_rela1_gis',
                                                         'dm_grid_m_net_df_branch_kx_gis', 'to_id', 'id']],
}

# 电压等级在不同系统中的映射关系, 'yx': 'sc'
volt_mapping = {
    "13": "306",  # 220kV
    "12": "298",  # 110kV
    "10": "290",  # 35kV
}
