# -*- coding: utf-8 -*-
from utils import gen_logger
import pandas as pd
from fuse_yn import get_data_from_db
from config import data_source_config
from model import ModelStack
from fuse_utils import get_all_train_fea


if __name__ == '__main__':
    logger = gen_logger()
    logger.info("日志模块加载成功")
    data_name = 'sub_tagged_data.csv'
    train_data = pd.read_csv(data_name)
    train_data = train_data.astype({'id1': 'str', 'id2': 'str'})
    logger.info("训练数据集读取成功")
    data = get_data_from_db(data_source_config, train_data, logger)
    logger.info("数据库数据加载成功")
    logger.info('正在进行特征工程...')
    train_data_fea = get_all_train_fea(data, train_data, data_source_config)
    logger.info('特征工程结束')
    all_columns = train_data_fea.columns.tolist()

    sub_model_name = ['name', 'child', 'feature']
    fea_list = [all_columns[0: 8], all_columns[8: 14], all_columns[13: 15] + all_columns[8: 10]]

    model_path = './path_to_model'
    modeler = ModelStack(model_path)
    logger.info('正在进行模型训练...')
    modeler.build_model(train_data_fea, all_columns[-1], fea_list, sub_model_name)
    logger.info('模型训练结束')
