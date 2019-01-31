import json
import matplotlib.pyplot as plt
import numpy as np


cnt = 0

alpha = 1
beta = 1
#选择数量级差异：1，2，3
for gamma in [1e-1, 1e-2, 1e-3]:
#绘制不同数量级下的TPS

	tps_growth = {
		"piece_0": [],
		"piece_1": [],
		"piece_2": []
	}

	for n in range(1, 12):
		filename = '{}_bits_v2.json'.format(n)
		with open(filename) as f_json:
			dict_manage_pieces = json.load(f_json)
		# js = json.dumps(dict_manage_pieces, indent=4, separators=(',', ':'))
		# print(js)
		# print('\n')
		for p in range(0,3):
			piece = "piece_" + str(p)
			dict_manage_shards = dict_manage_pieces[piece]
			t = []
			N = 2**n
			for s in range(0, N):
				shard = "shard_" + str(s)
				time = 0
				time += dict_manage_shards[shard]["theta"] * dict_manage_shards[shard]["epsilon"][s]
				#print(time)
				time += dict_manage_shards[shard]["theta"] * (1 - dict_manage_shards[shard]["epsilon"][s]) * alpha
				#print(time)
				for s_rest in range(0, N):
					if s_rest == s:
						continue
					shard_rest = "shard_" + str(s_rest)
					time += dict_manage_shards[shard_rest]["theta"] * dict_manage_shards[shard_rest]["epsilon"][s] * beta
				#print(time)
				#print("----------")
				t.append(time)
			print(t)
			if max(t) > gamma * (N - 1) / N:
				tps_growth[piece].append(1/max(t))
			else:
				tps_growth[piece].append(1/(gamma*(N-1)/N))

	js = json.dumps(tps_growth, indent=4, separators=(',', ':'))
	print(js)

	cnt+=1
	filename = "{}_tps_growth.json".format(cnt)
	with open(filename, 'w') as f_json:
		json.dump(tps_growth, f_json)




