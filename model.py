# -*- coding: utf-8 -*-
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle
import os


class ModelStack:
    def __init__(self,  model_path):

        if not os.path.exists(model_path):
            os.makedirs(model_path)
        self.model_path = model_path

    def build_sub_model(self, trained_df, label_column, fea_columns, model_names):
        num_models = len(fea_columns)
        y = np.array(trained_df[label_column])
        prob_list = []
        for t in range(num_models):
            sub_df = trained_df[fea_columns[t]]
            sub_fea_data = np.array(sub_df)
            rf = RandomForestClassifier()  # Random Forest Classifier
            model = rf.fit(sub_fea_data, y)
            with open(f'{self.model_path}/sub_rf_{model_names[t]}.pkl', 'wb') as f:
                pickle.dump(model, f)
            prob = model.predict_proba(sub_fea_data)
            prob_list.append(prob)
        return prob_list

    def build_stack_model(self, trained_df, label_column, prob_list):
        y = np.array(trained_df[label_column])
        row_num = len(prob_list[0])
        col_num = len(prob_list)
        data = np.zeros([row_num, col_num])
        for k in range(col_num):
            prob = prob_list[k]
            data[:, k] = prob[:, 1]

        rf = RandomForestClassifier()
        model = rf.fit(data, y)
        with open(f'{self.model_path}/stack_model.pkl', 'wb') as f:
            pickle.dump(model, f)

    def build_model(self, trained_df, label_column, fea_columns, model_names):
        prob_data = self.build_sub_model(trained_df, label_column, fea_columns, model_names)
        self.build_stack_model(trained_df, label_column, prob_data)

    def predict(self, df, fea_columns, model_names):
        row_num = df.shape[0]
        sub_model_data = np.zeros([row_num, len(fea_columns)])
        for i in range(len(fea_columns)):
            model = pickle.load(open(f"{self.model_path}/sub_rf_{model_names[i]}.pkl", 'rb'))
            fea_data = np.array(df[fea_columns[i]])
            prob = model.predict_proba(fea_data)
            sub_model_data[:, i] = prob[:, 1]
        model = pickle.load(open(f"{self.model_path}/stack_model.pkl", 'rb'))
        prob = model.predict_proba(sub_model_data)
        prob = prob[:, 1].tolist()
        total_prob = prob[0]
        sub_prob = sub_model_data[0]

        sim_dict = {}
        for i in range(len(model_names)):
            sim_dict[model_names[i] + '-sim'] = sub_prob[i]
        return total_prob, sim_dict
