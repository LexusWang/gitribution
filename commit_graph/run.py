import os
import csv
import pandas as pd
from graph import *
from propagate import *


def main():
	data_file1 = '../dataset/commit-parent.csv'
	data_file2 = '../dataset/commit-stat.txt'
	graph_file = '../dataset/commit.json'
	result_1 = '../dataset/result-prev.csv'
	result_2 = '../dataset/result-post.csv'
	commit_dict = graph_construction(data_file1, data_file2, graph_file)
	graph_dict = graph_initialize(commit_dict)
	# for key in graph_dict.keys():
	# 	for dest in graph_dict[key]['ancestors']:
	# 		print(key+','+dest)
	graph_stastic(graph_dict)
	Author_dict, Author_contribution = add_by_Author(graph_dict, commit_dict)
	Author_contribution = dict_normalization(Author_contribution)
	dict_to_csvfile(Author_contribution, result_1, ['Name', 'Contribution'])
	final_graph = propagate(graph_dict)
	Author_dict, Author_contribution = add_by_Author(final_graph, commit_dict)
	Author_contribution = dict_normalization(Author_contribution)
	dict_to_csvfile(Author_contribution, result_2, ['Name', 'Contribution'])
	dict_to_bar(Author_contribution)

if __name__ == "__main__":
	main()
