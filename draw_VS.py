import json
import matplotlib.pyplot as plt
import numpy as np

import draw_theoretical as dt

#选择数量级差异：1，2，3
gamma_flag = 1

alpha = 1
beta = 1

#绘制不同数量级下的TPS
if gamma_flag == 1:
	gamma = 1e-1
	N_threshold = dt.get_root(alpha, beta, gamma, 0, 100)
	x = [2**i for i in range(1, 8)]
	fs = 10
	title = r"$\alpha$=1, $\beta$=1, $\gamma$=10$^{-1}$"

	filename = "1_tps_growth.json"
	with open(filename) as f_json:
		tps_growth =json.load(f_json)
	p_0 = tps_growth["piece_0"][:7]
	p_1 = tps_growth["piece_1"][:7]
	p_2 = tps_growth["piece_2"][:7]
elif gamma_flag ==2:
	gamma = 1e-2
	N_threshold = dt.get_root(alpha, beta, gamma, 200, 300)
	x = [2**i for i in range(1, 8)]
	fs = 7
	title = r"$\alpha$=1, $\beta$=1, $\gamma$=10$^{-2}$"

	filename = "2_tps_growth.json"
	with open(filename) as f_json:
		tps_growth =json.load(f_json)
	p_0 = tps_growth["piece_0"][:7]
	p_1 = tps_growth["piece_1"][:7]
	p_2 = tps_growth["piece_2"][:7]
elif gamma_flag ==3:
	gamma = 1e-3
	N_threshold = dt.get_root(alpha, beta, gamma, 2000, 3000)
	x = [2**i for i in range(1, 8)]
	fs = 4
	title = r"$\alpha$=1, $\beta$=1, $\gamma$=10$^{-3}$"

	filename = "3_tps_growth.json"
	with open(filename) as f_json:
		tps_growth =json.load(f_json)
	p_0 = tps_growth["piece_0"][:7]
	p_1 = tps_growth["piece_1"][:7]
	p_2 = tps_growth["piece_2"][:7]

y = dt.get_theoretical_tps(x, N_threshold, alpha, beta, gamma)

plt.figure(dpi=100, figsize=(10, 6))
plt.grid()
	
plt.plot(x, y, c='red', linewidth=1)
plt.scatter(x, y, c='red', edgecolor='none', s=40)

plt.plot(x, p_0, c='blue', linewidth=1)
plt.scatter(x, p_0, c='blue', edgecolor='none', s=40)

plt.plot(x, p_1, c='blue', linewidth=1)
plt.scatter(x, p_1, c='blue', edgecolor='none', s=40)

plt.plot(x, p_2, c='blue', linewidth=1)
plt.scatter(x, p_2, c='blue', edgecolor='none', s=40)


#x轴以对数显示
# if gamma_flag > 1:
# 	plt.xscale('log')

plt.title(title, fontsize=24)
plt.xlabel("Shard number", fontsize=14)
plt.ylabel("TPS growth rate", fontsize=14)
plt.show()