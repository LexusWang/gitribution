import os
import csv
import re
import json
import numpy as np
import copy
import pandas as pd
from matplotlib import pyplot as plt


def dict_to_pie(data_dict, title=None, file_path=None, show_value=lambda x: x):
	data = []
	label = []
	for key, value in data_dict.items():
		label.append(key)
		data.append(value)
	plt.figure(figsize=(6, 6))  # 将画布设定为正方形，则绘制的饼图是正圆
	# explode = [0.01, 0.01, 0.01]  # 设定各项距离圆心n个半径
	plt.pie(data, labels=label, autopct='%1.1f%%')  # 绘制饼图
	if title != None:
		plt.title(title)  # 绘制标题
	if file_path != None:
		plt.savefig(file_path)  # 保存图片
	plt.show()


def dict_to_bar(data_dict, title=None, file_path=None):
	rank = sorted(data_dict.items(), key=lambda x: x[1], reverse=True)
	data = []
	label = []
	data_sum = 0
	for item in rank:
		data_sum += item[1]
		label.append(item[0])
	for i in range(len(rank)):
		rank[i] = [rank[i][0], rank[i][1]/data_sum]
		data.append(rank[i][1])
		print(rank[i][0], rank[i][1])
	plt.figure(figsize=(16, 16))  # 将画布设定为正方形，则绘制的饼图是正圆
	plt.barh(label, data)  # 横放条形图函数 barh
	if title != None:
		plt.title(title)  # 绘制标题
	if file_path != None:
		plt.savefig(file_path)  # 保存图片
	# plt.show()

def dict_to_csvfile(data_dict, file_name, header,if_sorted=True):
	sorted_dict = sorted(data_dict.items(),key = lambda x: x[1],reverse=True)
	with open(file_name,'w',newline='')as fout:
		writer = csv.writer(fout,delimiter=',')
		writer.writerow(header)
		for item in sorted_dict:
			writer.writerow([item[0],item[1]])


def dict_normalization(data_dict, show_value=lambda x: x, give_value = lambda a,b:a/b):
	sum_data = 0
	for key in data_dict.keys():
		sum_data += show_value(data_dict[key])
	for key in data_dict.keys():
		# data_dict[key] /= sum_data
		data_dict[key] = give_value(data_dict[key],sum_data)
	return data_dict
