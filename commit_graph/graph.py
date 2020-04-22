import os
import csv
import re
import json
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def add_parent(data_path, data_dict):
	data = []
	with open(data_path, 'r') as fin:
		csv_reader = csv.reader(fin, delimiter=',')
		for item in csv_reader:
			data_dict[item[0]] = {}
			if len(item[1]) == 0:
				print(item[0])
				parents = []
			elif len(item[1]) != 40:
				parents = item[1].split(' ')
			else:
				parents = [item[1]]
			data_dict[item[0]]['parent'] = parents
			data.append(item)
	return data_dict, data


def add_date(data_path, data_dict):
	data_index = len(data_dict)
	with open(data_path, 'r') as fin:
		csv_reader = csv.reader(fin, delimiter=',')
		for item in csv_reader:
			data_dict[item[0]]['date'] = item[2]
			data_dict[item[0]]['index'] = data_index
			data_index -= 1
	return data_dict


def add_Author(data_path, data_dict):
	commit_name = None
	with open(data_path, 'r') as fin:
		for lines in fin:
			if lines[:6] == 'commit':
				commit_name = lines[7:47]
				assert commit_name in data_dict, 'commit can\'t be found in data dict'
				data_dict[commit_name]['files'] = []
			elif lines[:6] == 'Author':
				data_dict[commit_name]['Author'] = lines[8:-1]
			elif lines[:4] == 'Date':
				data_dict[commit_name]['Date_spe'] = lines[8:-1]
			elif re.match(r'\s.*\s\|\s.*\s.*', lines, flags=0):
				# a = re.match(r'\s.*\s\|\s.*\s.*', lines, flags=0)
				files_changed = re.split(r'\s*\|\s*', lines[1:-1])
				if re.match(r'\s.*\s\|\s*[0-9]+\s.*', lines, flags=0):
					num_changed = int(re.split(r'\s+', files_changed[1])[0])
				elif re.match(r'\s.*\s\|\s*Bin\s.*', lines, flags=0):
					num_changed = 1
				else:
					num_changed = 0
				data_dict[commit_name]['files'].append(
					[files_changed[0], num_changed])
	return data_dict


def add_code_amount(data_dict):
	for key in data_dict.keys():
		code_amount = 0
		if 'files' not in data_dict[key]:
			data_dict[key]['files'] = []
		for item in data_dict[key]['files']:
			code_amount += item[1]
		data_dict[key]['code_amount'] = code_amount
	return data_dict


def commit_info():
	data_file = '../dataset/commit-parent&date.csv'
	commit_dict = {}
	commit_dict, _ = add_parent(data_file, commit_dict)
	commit_dict = add_date(data_file, commit_dict)
	data_file = '../dataset/commit-stat.txt'
	commit_dict = add_Author(data_file, commit_dict)
	commit_dict = add_code_amount(commit_dict)
	with open('../dataset/commit.json', 'w') as f:
		json.dump(commit_dict, f)


def graph_construction(data_file1,data_file2,graph_file):
	index = 0
	commit_index = {}
	commit_dict = {}
	commit_dict, commit_order = add_parent(data_file1, commit_dict)
	for item in commit_order:
		commit_index[item[0]] = index
		index += 1
	commit_dict = add_date(data_file1, commit_dict)
	commit_dict = add_Author(data_file2, commit_dict)
	commit_dict = add_code_amount(commit_dict)
	with open(graph_file, 'w') as f:
		json.dump(commit_dict, f)
	return commit_dict


def date_factor(index, decay=-0.001):
	weight = 10*np.exp(decay*index)
	return weight


def amount_factor(code_amount, decay=-0.001):
	# weight = np.sqrt(data_dict[key]['commit_amount'])
	weight = code_amount
	return weight


def file_factor(file_list, file_weight):
	weight = 0
	for file in file_list:
		weight += file_weight[file[0]]
	return weight


def file_importance(data_dict):
	file_importance = {}
	for key in data_dict.keys():
		file_list = data_dict[key]['files']
		for file in file_list:
			if file[0] not in file_importance:
				file_importance[file[0]] = 0
			file_importance[file[0]] += 1
	return file_importance


def sum_weight(data_weight):
	for key in data_weight.keys():
		data_weight[key]['weight'] = np.sum(data_weight[key]['weight'])
	return data_weight


def weight_initialize(graph_dict, commit_dict):
	file_weight = file_importance(commit_dict)
	sum_weight_list = [0 for i in range(3)]
	for key in commit_dict.keys():
		graph_dict[key]['weight'].append(date_factor(commit_dict[key]['index']))
		sum_weight_list[0] += graph_dict[key]['weight'][-1]
		graph_dict[key]['weight'].append(amount_factor(commit_dict[key]['code_amount']))
		sum_weight_list[1] += graph_dict[key]['weight'][-1]
		graph_dict[key]['weight'].append(file_factor(commit_dict[key]['files'], file_weight))
		sum_weight_list[2] += graph_dict[key]['weight'][-1]
	for key in commit_dict.keys():
		for i in range(len(graph_dict[key]['weight'])):
			graph_dict[key]['weight'][i] /= sum_weight_list[i]
	graph_dict = sum_weight(graph_dict)
	return graph_dict


def edge_initialize(graph_dict, commit_dict):
	commit_order = [[] for i in range(len(commit_dict))]
	file_history = {}
	for key in commit_dict.keys():
		parents = commit_dict[key]['parent']
		graph_dict[key]['ancestors'].extend(parents)
		commit_order[commit_dict[key]['index']-1] = [key,commit_dict[key]['files']]
	for i in range(len(commit_dict)):
		key = commit_order[i][0]
		file_list = commit_order[i][1]
		for file in file_list:
			if file[0] not in file_history:
				file_history[file[0]] = []
			else:
				for ancestor in file_history[file[0]]:
					graph_dict[key]['ancestors'].append(ancestor)
			file_history[file[0]].append(key)
	return graph_dict

def graph_initialize(commit_dict):
	graph_dict = {}
	for key in commit_dict:
		graph_dict[key] = {}
		graph_dict[key]['weight'] = []
		graph_dict[key]['ancestors'] = []
	graph_dict = weight_initialize(graph_dict, commit_dict)
	graph_dict = edge_initialize(graph_dict, commit_dict)
	return graph_dict

def graph_stastic(graph):
	total_node = len(graph)
	print('节点数：'+str(total_node))
	total_edge = 0
	for key in graph.keys():
		total_edge += len(graph[key]['ancestors'])
	print('总边数：'+str(total_edge))
	print('平均度数：'+str(total_edge/total_node))
