# -*- coding: utf-8 -*-
from config import data_source_config, test_data
from fuse_utils import get_all_fea, return_mysql_conn
from utils import gen_logger, Entity
from grid_utils_yn import table_properties
import numpy as np
import pandas as pd
import pickle


def predict(df, entity1, entity2, models):
    """对于输入的实体对进行预测。

    Args:
        df:
        entity1(Entity):
        entity2(Entity):
        models(list):

    Returns:

    """
    fea_df = get_all_fea(df, entity1, entity2, data_source_config)
    columns = fea_df.columns.tolist()
    fea_list = [columns[0: 8], columns[8: 14], columns[13: 15] + columns[8: 10]]
    row_num = fea_df.shape[0]
    col_num = len(models) - 1
    stack_model_data = np.zeros([row_num, col_num])
    for i in range(col_num):
        model = models[i]
        fea = fea_list[i]
        sub_df = np.array(fea_df[fea])
        prob = model.predict_proba(sub_df)
        stack_model_data[:, i] = prob[:, 1]
    model = models[-1]
    prob = model.predict_proba(stack_model_data)
    total_prob = prob[:, 1].tolist()[0]
    sub_prob = stack_model_data[0]

    sim_dict = {'total_prob': total_prob}
    for i in range(col_num):
        sim_dict[f'sub_model{i}_prob'] = sub_prob[i]

    return sim_dict


def match_entity(df, data, models, logger):
    """使用训练好的模型对测试数据进行预测。

    Args:
        df: 原始数据集合
        data(dict): 测试数据字典
        models(list): 训练好的模型的列表

    Returns:

    """
    yx_tab = list(data['yx'].keys())[0]
    yx_list = [(i, yx_tab) for i in data['yx'][yx_tab]]

    pms_tab = list(data['pms'].keys())[0]
    pms_list = [(i, pms_tab) for i in data['pms'][pms_tab]]

    gis_tab = list(data['gis'].keys())[0]
    gis_list = [(i, gis_tab) for i in data['gis'][gis_tab]]

    res_list = []
    # matching with pms and gis basing on yx
    logger.info('1st, matching with pms and gis basing on yx ...')
    for term in yx_list:
        id_field = table_properties[yx_tab]['idColName']
        base_entity = Entity('yx', 'line', term[0], term[1])
        # value = yx_df[yx_df[id_field] == term[0]]

        # travers among pms
        if pms_list:
            pms_pred = []
            for p_term in pms_list:
                p_ent = Entity('pms', 'line', p_term[0], p_term[1])
                prob_dict = predict(df, base_entity, p_ent, models)
                pms_pred.append(prob_dict)
            total_prob = [i['total_prob'] for i in pms_pred]
            max_prob = max(total_prob)
            if max_prob > 0.6:
                max_ind = total_prob.index(max_prob)
                pms_match = pms_list[max_ind]
                pms_sim_dict = pms_pred[max_ind]
                pms_list.remove(pms_match)
            else:
                pms_sim_dict = None
                pms_match = None
        else:
            pms_sim_dict = None
            pms_match = None

        # travers among gis
        if gis_list:
            gis_pred = []
            for g_term in gis_list:
                g_ent = Entity('gis', 'line', g_term[0], g_term[1])
                prob_dict = predict(df, base_entity, g_ent, models)
                gis_pred.append(prob_dict)
            total_prob = [i['total_prob'] for i in gis_pred]
            max_prob = max(total_prob)
            if max_prob > 0.6:
                max_ind = total_prob.index(max_prob)
                gis_match = gis_list[max_ind]
                gis_sim_dict = gis_pred[max_ind]
                gis_list.remove(gis_match)
            else:
                gis_sim_dict = None
                gis_match = None
        else:
            gis_sim_dict = None
            gis_match = None

        if pms_sim_dict is not None and gis_sim_dict is None:
            res_list.append([yx_tab, pms_match[1], None,
                             term[0], pms_match[0], None,
                             pms_sim_dict['sub_model0_prob'], pms_sim_dict['sub_model1_prob'],
                             pms_sim_dict['sub_model2_prob'], pms_sim_dict['total_prob']])
        elif pms_sim_dict is None and gis_sim_dict is not None:
            res_list.append([yx_tab, None, gis_match[1],
                             term[0], None, gis_match[0],
                             gis_sim_dict['sub_model0_prob'], gis_sim_dict['sub_model1_prob'],
                             gis_sim_dict['sub_model2_prob'], gis_sim_dict['total_prob']])
        elif pms_sim_dict is not None and gis_sim_dict is not None:
            res_list.append([yx_tab, pms_match[1], gis_match[1],
                             term[0], pms_match[0], gis_match[0],
                             (pms_sim_dict['sub_model0_prob'] + gis_sim_dict['sub_model0_prob']) / 2,
                             (pms_sim_dict['sub_model1_prob'] + gis_sim_dict['sub_model1_prob']) / 2,
                             (pms_sim_dict['sub_model2_prob'] + gis_sim_dict['sub_model2_prob']) / 2,
                             (pms_sim_dict['total_prob'] + gis_sim_dict['total_prob']) / 2])
        else:
            res_list.append([yx_tab, None, None, term[0], None, None, None, None, None, None])

    # matching with gis basing on pms
    logger.info('2nd, matching with gis basing on pms ...')
    for term in pms_list:
        base_entity = Entity('pms', 'line', term[0], term[1])

        # travers among gis
        if gis_list:
            gis_pred = []
            for g_term in gis_list:
                g_ent = Entity('gis', 'line', g_term[0], g_term[1])
                prob_dict = predict(df, base_entity, g_ent, models)
                gis_pred.append(prob_dict)
            total_prob = [i['total_prob'] for i in gis_pred]
            max_prob = max(total_prob)
            if max_prob > 0.6:
                max_ind = total_prob.index(max_prob)
                gis_match = gis_list[max_ind]
                gis_sim_dict = gis_pred[max_ind]
                gis_list.remove(gis_match)
            else:
                gis_sim_dict = None
                gis_match = None
        else:
            gis_sim_dict = None
            gis_match = None

        if gis_sim_dict is not None:
            res_list.append([None, pms_tab, gis_match[1],
                             None, term[0], gis_match[0],
                             gis_sim_dict['sub_model0_prob'], gis_sim_dict['sub_model1_prob'],
                             gis_sim_dict['sub_model2_prob'], gis_sim_dict['total_prob']])
        else:
            res_list.append([None, pms_tab, None, None, term[0], None, None, None, None, None])

    # set the rest gis entities to result list
    logger.info('3rd, setting the rest entities to result list ...')
    for term in gis_list:
        res_list.append([None, None, term[0], None, None, gis_tab, None, None, None, None])

    res_df = pd.DataFrame(res_list, columns=['yx_tab', 'pms_tab', 'gis_tab',
                                             'yx_id', 'pms_id', 'gis_id',
                                             'sim1', 'sim2', 'sim3', 'total_sim'])
    return res_df


def get_test_data_dict(test_data):
    conn = return_mysql_conn(data_source_config)
    data_dict = {}
    for sys in test_data:
        for tab in test_data[sys]:
            ids = tuple(test_data[sys][tab])
            sql = f"select * from {tab} where {table_properties[tab]['idColName']} in {ids}"
            if len(ids) == 0:
                continue
            elif len(ids) == 1:
                sql = sql[:-2] + ')'
            else:
                pass
            value = pd.read_sql(sql, conn)
            data_dict[tab] = value
    return data_dict


if __name__ == '__main__':
    logger = gen_logger()
    model_path = './path_to_model'
    model0 = pickle.load(open(model_path + '/sub_rf_name.pkl', 'rb'))
    model1 = pickle.load(open(model_path + '/sub_rf_child.pkl', 'rb'))
    model2 = pickle.load(open(model_path + '/sub_rf_feature.pkl', 'rb'))
    stack_model = pickle.load(open(model_path + '/stack_model.pkl', 'rb'))
    models = [model0, model1, model2, stack_model]
    data_dict = get_test_data_dict(test_data)
    pred_res = match_entity(data_dict, test_data, models, logger)
    pred_res.to_csv('./pred_res.csv', index=False)
