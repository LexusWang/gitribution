import os
import csv
import re
import json
import numpy as np
import copy
import math
import pandas as pd
from matplotlib import pyplot as plt
from tools import *


def feedback(old_graph, contri_factor):
	new_graph = copy.deepcopy(old_graph)
	for key in old_graph.keys():
		parents_list = old_graph[key]['ancestors']
		parents_num = len(parents_list)
		if parents_num > 0 and parents_list[0]!='ROOT':
			for item in parents_list:
				new_graph[item]['weight'] += contri_factor * \
					(1/parents_num) * old_graph[key]['weight']
	return new_graph

def propagate(old_graph):
	old_graph = dict_normalization(old_graph, 
		show_value=lambda x: x['weight'], 
		give_value=lambda a, b: {'weight': a['weight']/b, 'ancestors': a['ancestors']})
	initial_value = 1
	prev_graph = copy.deepcopy(old_graph)
	for i in range(10):
		new_graph = feedback(prev_graph, initial_value*np.power(0.5, i))
		new_graph = dict_normalization(new_graph, 
		show_value=lambda x: x['weight'], 
		give_value=lambda a, b: {'weight': a['weight']/b, 'ancestors': a['ancestors']})
		total_distance = 0
		for key in new_graph.keys():
			total_distance += math.pow(new_graph[key]
			                           ['weight']-prev_graph[key]['weight'], 2)
		print('ite'+str(i)+' total distance:'+str(total_distance))
		prev_graph = copy.deepcopy(new_graph)
	return new_graph

def add_by_Author(graph, commit_dict):
	Author_dict = {}
	Author_contribution = {}
	for key in commit_dict.keys():
		if commit_dict[key]['Author'] not in Author_dict:
			Author_dict[commit_dict[key]['Author']] = []
			Author_contribution[commit_dict[key]['Author']] = 0
		Author_dict[commit_dict[key]['Author']].append(key)
		Author_contribution[commit_dict[key]['Author']] += graph[key]['weight']
	return Author_dict, Author_contribution
