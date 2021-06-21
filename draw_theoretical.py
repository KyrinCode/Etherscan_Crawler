import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

def get_value_polynomial_2(n, coef1, coef2, coef3):
	#秦九韶算法求多项式值
	return (coef1 * n + coef2) * n + coef3

def get_root(alpha, beta, gamma, start, end):
	#二分算法求函数解
	left = float(start)
	right = float(end)
	error = 1e-5

	while True:
		mid = (left + right) / 2
		value = get_value_polynomial_2(mid, gamma, -(alpha+beta+gamma), (alpha+beta-1))
		if value < -error:
			left = mid
		elif value > error:
			right = mid
		else:
			return mid

def tps_less_than_threshold(N, alpha, beta):
	return (N**2) / (1 + (alpha + beta) * (N - 1))

def tps_more_than_threshold(N, gamma):
	return N / ((N - 1) * gamma)

def get_theoretical_tps(x, N_threshold, alpha, beta, gamma):
	y = []
	for xi in x:
		if xi < N_threshold:
			y.append(tps_less_than_threshold(xi, alpha, beta))
		else:
			y.append(tps_more_than_threshold(xi, gamma))
	return y

if __name__ == '__main__':
	#选择数量级差异：0，1，2，3
	gamma_flag = 3
	#选择是否展开局部图：0，1
	expand_flag = 0

	alpha = 1
	beta = 1

	#绘制不同数量级下的TPS
	if gamma_flag == 0:
		gamma = 1
		N_threshold = get_root(alpha, beta, gamma, 0, 100)
		print(N_threshold)
		x = [2**i for i in range(1, 8)]
		fs = 10
		title = r"$\alpha$=1, $\beta$=1, $\gamma$=10$^{-1}$"
	elif gamma_flag == 1:
		gamma = 1e-1
		N_threshold = get_root(alpha, beta, gamma, 0, 100)
		x = [2**i for i in range(1, 8)]
		fs = 10
		title = r"$\alpha$=1, $\beta$=1, $\gamma$=10$^{-1}$"
	elif gamma_flag ==2:
		gamma = 1e-2
		N_threshold = get_root(alpha, beta, gamma, 200, 300)
		x = [2**i for i in range(1, 12)]
		fs = 7
		title = r"$\alpha$=1, $\beta$=1, $\gamma$=10$^{-2}$"
	elif gamma_flag ==3:
		gamma = 1e-3
		N_threshold = get_root(alpha, beta, gamma, 2000, 3000)
		x = [2**i for i in range(1, 16)]
		fs = 4
		title = r"$\alpha$=1, $\beta$=1, $\gamma$=10$^{-3}$"
	y = get_theoretical_tps(x, N_threshold, alpha, beta, gamma)

	print(x)
	print(y)

	plt.figure(dpi=100, figsize=(10, 6))
	plt.grid()

	#需要放大的部分
	if expand_flag == 0:
		plt.plot(x, y, c='red', linewidth=1)
		plt.scatter(x, y, c='red', edgecolor='none', s=40)
		for a, b in zip(x, y):
			plt.text(a, b, (a, round(b, 1)), ha='right', va='bottom', fontsize=fs)
	elif expand_flag == 1:
		if gamma_flag == 2:
			x_expand = x[7:]
			y_expand = y[7:]
		elif gamma_flag == 3:
			x_expand = x[10:]
			y_expand = y[10:]

		plt.plot(x_expand, y_expand, c='red', linewidth=1)
		plt.scatter(x_expand, y_expand, c='red', edgecolor='none', s=40)
		for a, b in zip(x_expand, y_expand):
			plt.text(a, b, (a, round(b, 1)), ha='left', va='bottom', fontsize=12)

	#x轴以对数显示
	if gamma_flag > 1 and expand_flag == 0:
		plt.xscale('log')

	plt.title(title, fontsize=14)
	plt.xlabel("分片数量", fontsize=14)
	plt.ylabel("通量增长率", fontsize=14)
	plt.show()