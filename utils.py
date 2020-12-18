# -*- coding: utf-8 -*-
import numpy as np
from pypinyin import lazy_pinyin
from scipy.linalg import norm
import jieba
import Levenshtein as lvst
import logging


def gen_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)7s %(filename)10s %(lineno)3d |'
        ' %(message)s ',
        datefmt='%Y-%m-%d %H:%M:%S')
    console.setFormatter(formatter)
    logger.addHandler(console)
    return logger


class Similarities:
    """各种计算相似度的方法"""

    @staticmethod
    def get_common_str_sim(s1, s2):
        """获取公共字符相似度"""
        len1 = len(s1)
        len2 = len(s2)
        min_len = np.min([len1, len2])
        ss = [s1, s2]
        flag = (len1 > len2)
        short = ss[flag]
        long = ss[1 - flag]

        count_in = 0.0
        for elem in short:
            if elem in long:
                count_in += 1.0
        return count_in / min_len

    @staticmethod
    def get_max_common_sub_str_sim(s1, s2):
        """获取最大公共子串相似度"""
        len1 = len(s1)
        len2 = len(s2)
        down_line = np.zeros([len1])

        for p in range(len2):
            up_line = down_line.copy()
            for q in range(len1):
                flag = (s1[q] == s2[p])
                if flag and q > 0:
                    down_line[q] = up_line[q - 1] + 1.0
                elif flag and q == 0:
                    down_line[q] = 1.0

        common_len = down_line.max()
        short_len = np.min([len1, len2])
        sim = common_len / short_len
        return sim

    @staticmethod
    def get_max_common_sub_str_sim2(s1, s2):
        """获取最大公共子串相似度"""
        len1 = len(s1)
        len2 = len(s2)
        count_arr = np.zeros([len2, len1])
        for p in range(len2):
            for q in range(len1):
                flag = (s1[q] == s2[p])
                if p == 0 and flag:
                    count_arr[p, q] = 1
                elif q == 0 and flag:
                    count_arr[p, q] = 1
                elif flag:
                    count_arr[p, q] = count_arr[p - 1, q - 1] + 1
        common_len = count_arr.max(axis=0).max()
        short_len = np.min([len1, len2])
        sim = common_len * 1.0 / short_len
        return sim

    @staticmethod
    def get_max_common_sub_seq_sim(s1, s2):
        """获取最大公共子序列相似度"""
        len1 = len(s1)
        len2 = len(s2)
        arr = np.zeros([len2 + 1, len1 + 1])

        for p in range(1, len2 + 1):
            line_unit = s2[p - 1]
            for q in range(1, len1 + 1):
                left_value = arr[p, q - 1]
                top_value = arr[p - 1, q]
                corner_value = arr[p - 1, q - 1]

                if line_unit == s1[q - 1]:
                    corner_value += 1
                arr[p, q] = np.max([left_value, top_value, corner_value])
        common_len = arr[len2, len1]
        sim = common_len / min([len1, len2])
        return sim

    def get_pinyin_max_common_sub_seq_sim(self, s1, s2):
        """获取拼音的最大公共子序列相似度"""
        p1 = ''.join(lazy_pinyin(s1))
        p2 = ''.join(lazy_pinyin(s2))
        return self.get_max_common_sub_seq_sim(p1, p2)

    @staticmethod
    def get_words_cos_sim(s1, s2):
        """获取分词后向量的余弦相似度"""
        cut_res1 = jieba.cut(s1)
        list1 = ' | '.join(cut_res1).split(' | ')
        cut_res2 = jieba.cut(s2)
        list2 = ' | '.join(cut_res2).split(' | ')
        word_bag = []
        for word in list1 + list2:
            if word not in word_bag:
                word_bag.append(word)
        count1 = [0.0] * len(word_bag)
        count2 = [0.0] * len(word_bag)
        for w1 in list1:
            ind = word_bag.index(w1)
            count1[ind] += 1
        for w2 in list2:
            ind = word_bag.index(w2)
            count2[ind] += 1
        arr1 = np.array(count1)
        arr2 = np.array(count2)
        cos = arr1.dot(arr2) / (norm(arr1) * norm(arr2))
        cos_sim = 0.5 * (1.0 + cos)
        return cos_sim

    @staticmethod
    def get_str_cos_sim(s1, s2):
        """获取字符的余弦相似度"""
        union_set = []
        for elem in s1 + s2:
            if elem not in union_set:
                union_set.append(elem)
        count1 = [0.0] * len(union_set)
        count2 = [0.0] * len(union_set)
        for w1 in s1:
            ind = union_set.index(w1)
            count1[ind] += 1
        for w2 in s2:
            ind = union_set.index(w2)
            count2[ind] += 1
        arr1 = np.array(count1)
        arr2 = np.array(count2)
        cos = arr1.dot(arr2) / (norm(arr1) * norm(arr2))
        cos_sim = 0.5 * (1.0 + cos)
        return cos_sim

    @staticmethod
    def get_jaccard_sim(s1, s2):
        """获取Jaccard相似度"""
        union_set = []
        for elem in s1 + s2:
            if elem not in union_set:
                union_set.append(elem)
        count_inter = 0.0
        for term in union_set:
            if term in s1 and term in s2:
                count_inter += 1.0
        len_union = len(union_set)
        sim = count_inter / (1.0 * len_union)
        return sim

    @staticmethod
    def get_edit_sim(s1, s2):
        """获取编辑距离"""
        distance = lvst.distance(s1, s2)
        return 1 - (distance / max(len(s1), len(s2)))


class Entity:
    """实体类"""
    def __init__(self, sys_type, ent_type, ent_id, ent_tab):
        """分别记录实体所属系统，实体类型，实体的唯一标识，实体所属表"""
        self.sys_type = sys_type
        self.ent_type = ent_type
        self.ent_id = ent_id
        self.ent_tab = ent_tab
