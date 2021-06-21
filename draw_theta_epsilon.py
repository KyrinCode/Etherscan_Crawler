import json
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

# plot theta
plt.figure()
color = ['red', 'blue', 'green', 'cyan']
for n in range(1, 4):
	plt.subplot(1, 3, n)
	filename = '{}_bits_v3.json'.format(n)
	with open(filename) as f_json:
		dict_manage_pieces = json.load(f_json)
		dict_manage_shards = dict_manage_pieces["piece_0"]
	N = 2**n
	x = list(range(1, N+1))
	theta = []
	for i in range(N):
		shard = "shard_" + str(i)
		theta.append(dict_manage_shards[shard]["theta"])

	plt.scatter(x, theta, c=color[n-1], edgecolor='none', s=40)
	plt.grid()
	plt.xlim((0, N+1))
	plt.ylim((0, 1))
	plt.xticks(np.arange(0, N+1, 1))
	plt.yticks(np.arange(0, 1, 0.1))
	plt.title(r"分片数量 N = " + str(N), fontsize=14)
	plt.xlabel("测量分片", fontsize=14)
	plt.ylabel(r"$f(N)$ 值", fontsize=14)
plt.show()

# plt.figure()
# color = ['red', 'blue', 'green', 'cyan']
# for n in range(1, 5):
# 	filename = '{}_bits_v3.json'.format(n)
# 	with open(filename) as f_json:
# 		dict_manage_pieces = json.load(f_json)
# 		dict_manage_shards = dict_manage_pieces["piece_0"]
# 	N = 2**n
# 	x = list(range(1, N+1))
# 	theta = []
# 	for i in range(N):
# 		shard = "shard_" + str(i)
# 		theta.append(dict_manage_shards[shard]["theta"])

# 	plt.scatter(x, theta, c=color[n-1], edgecolor='none', s=20)
# 	plt.xlim((0, N+1))
# 	plt.ylim((0, 1))
# 	plt.xticks(np.arange(0, N+1, 1))
# 	plt.yticks(np.arange(0, 1, 0.1))
# 	plt.title(r"$\theta$ Shard number =2,4,8,16", fontsize=24)
# 	plt.xlabel("Measure times", fontsize=14)
# 	plt.ylabel(r"$\theta$ value", fontsize=14)
# plt.grid()
# plt.show()

#plot epsilon
# for n in range(1, 5):
# 	filename = '{}_bits_v3.json'.format(n)
# 	with open(filename) as f_json:
# 		dict_manage_pieces = json.load(f_json)
# 		dict_manage_shards = dict_manage_pieces["piece_0"]
# 	N = 2**n
# 	x = list(range(1, N+1))
# 	epsilon = []
# 	for i in range(N):
# 		shard = "shard_" + str(i)
# 		epsilon.append(dict_manage_shards[shard]["epsilon"][i])

# 	plt.scatter(x, epsilon, c='blue', edgecolor='none', s=40)
# 	plt.grid()
# 	plt.xlim((0, N+1))
# 	plt.ylim((0, 1))
# 	plt.xticks(np.arange(0, N+1, 1))
# 	plt.yticks(np.arange(0, 1, 0.1))
# 	plt.title(r"$\epsilon$(i,i) Shard number =" + str(N), fontsize=24)
# 	plt.xlabel("Measure times", fontsize=14)
# 	plt.ylabel(r"$\epsilon$(i,i) value", fontsize=14)
# 	plt.show()

# plt.figure()
# color = ['red', 'blue', 'green', 'cyan']
# for n in range(1, 5):
# 	filename = '{}_bits_v3.json'.format(n)
# 	with open(filename) as f_json:
# 		dict_manage_pieces = json.load(f_json)
# 		dict_manage_shards = dict_manage_pieces["piece_0"]
# 	N = 2**n
# 	x = list(range(1, N+1))
# 	epsilon = []
# 	for i in range(N):
# 		shard = "shard_" + str(i)
# 		epsilon.append(dict_manage_shards[shard]["epsilon"][i])

# 	plt.scatter(x, epsilon, c=color[n-1], edgecolor='none', s=20)
# 	plt.xlim((0, N+1))
# 	plt.ylim((0, 1))
# 	plt.xticks(np.arange(0, N+1, 1))
# 	plt.yticks(np.arange(0, 1, 0.1))
# 	plt.title(r"$\epsilon$(i,i) Shard number =2,4,8,16", fontsize=24)
# 	plt.xlabel("Measure times", fontsize=14)
# 	plt.ylabel(r"$\epsilon$(i,i) value", fontsize=14)
# plt.grid()
# plt.show()