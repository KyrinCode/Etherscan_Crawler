import sqlite3
import json

class ManageShardTxns():
	"""管理每种分片情况下，各分片的片内交易数和发起的跨片交易数"""
	def __init__(self, N):
		"""初始化该分片向各分片发起交易数为0"""
		self.txns = [0] * N

	def get_total_txns(self):
		"""获取该分片发起的所有交易数"""
		return sum(self.txns)

	def get_epsilon(self):
		"""获得向每个分片发起交易占发起交易的比例"""
		if self.get_total_txns() == 0:
			return self.txns
		epsilon = []
		total_txns = self.get_total_txns()
		for i in self.txns:
			epsilon.append(float(i) / total_txns)
		return epsilon

class ManageTxns():
	"""依据前n位分片"""
	def __init__(self, n):
		self.N = 2**n
		self.list_shard = []
		for i in range(self.N):
			self.list_shard.append(ManageShardTxns(self.N))

	def get_txns_num(self):
		"""获得所有交易数"""
		txns_num = 0
		for i in range(self.N):
			txns_num += self.list_shard[i].get_total_txns()
		return txns_num

	def get_theta(self, i):
		"""获得第i个分片发起交易的概率"""
		return float(self.list_shard[i].get_total_txns()) / self.get_txns_num()


def hex2bin(s):
	"""16进制转2进制"""
	bin_temp = bin(int(s, 16)).replace('0b', '')
	for i in range(160-len(bin_temp)):
		bin_temp = '0' + bin_temp
	return bin_temp

def bin2int(s):
	"""2进制转10进制"""
	return int(s, 2)

def get_latest_blockid(c):
	"""获取数据库中最近的block_id"""
	cursor = c.execute("SELECT max(block_id) from ETHERSCAN")
	for row in cursor:
		return row[0]

def get_earliest_blockid(c):
	"""获取数据库中最早的block_id"""
	cursor = c.execute("SELECT min(block_id) from ETHERSCAN")
	for row in cursor:
		return row[0]

def analyse_etherscan(n, manage_txns, c, last_blockid, blocknum=10000):
	"""
	last_blockid: 分析到最后的区块
	blocknum: 分析区块的数量
	"""
	cursor = c.execute("SELECT block_id, sender, receiver from ETHERSCAN")
	for row in cursor:
		if row[0] > last_blockid:
			continue
		if row[0] <= last_blockid - blocknum:
			break
		#print("Block_id: {} Sender: {} -> Receiver: {}".format(row[0], row[1], row[2]))
		sender = row[1]
		receiver = row[2]
		sender_bin = hex2bin(sender)
		receiver_bin = hex2bin(receiver)
		#print("Block_id: {} Sender: {} -> Receiver: {}".format(row[0], sender_bin, receiver_bin))
		sender_nbits = sender_bin[:n]
		receiver_nbits = receiver_bin[:n]
		sender_shardid = bin2int(sender_nbits)
		receiver_shardid = bin2int(receiver_nbits)
		#print("Sender's shard_id: {} -> Receiver's shard_id: {}".format(sender_shardid, receiver_shardid))
		manage_txns.list_shard[sender_shardid].txns[receiver_shardid] += 1

if __name__ == '__main__':
	#打开数据库
	conn = sqlite3.connect('etherscan.db')
	print("Opened database successfully")
	c = conn.cursor()
	#获得数据库中最后一个区块号
	# latest_blockid = get_latest_blockid(c)
	# print("The latest block_id is: {}".format(latest_blockid))
	#获得数据库中最早的区块号
	# earliest_blockid = get_earliest_blockid(c)
	# print("The earliest block_id is: {}".format(earliest_blockid))

	#计算6600001-6900000共计30w个区块
	latest_blockid = 6900000
	#取不同长度位的分片方法
	for n in range(1, 5):
		filename = '{}_bits_v3.json'.format(n)
		#列表：同一长度位的分片方法的多组数据
		dict_manage_pieces = {}

		blocknum = 300000
		for p in range(1):
			#管理一种长度位的分片方法的一组数据的结果
			dict_manage_shards = {}
			manage_txns = ManageTxns(n)
			end_blockid = latest_blockid-p*blocknum
			analyse_etherscan(n, manage_txns, c, end_blockid, blocknum)
			print("Analysis done successfully from block_id: {} to {}".format(end_blockid-blocknum+1, end_blockid))
			
			for i in range(2**n):
				#print("Shard_id: {}'s intra_txns number is {}".format(i, manage_txns.list_shard[i].intra_txns))
				#print("Shard_id: {}'s inter_txns number is {}".format(i, manage_txns.list_shard[i].inter_txns))
				#print("Shard_id: {}'s Epsilon(i, i) is {}".format(i, manage_txns.list_shard[i].get_intra_epsilon()))
				#print("Shard_id: {}'s Epsilon(j, i) is {}".format(i, manage_txns.list_shard[i].get_inter_epsilon()))
				#print("Shard_id: {}'s Theta(i) is {}".format(i, manage_txns.get_theta(i)))
				dict_manage_shards['shard_'+str(i)] = {\
				'theta': manage_txns.get_theta(i),
				'epsilon': manage_txns.list_shard[i].get_epsilon()
				}

			dict_manage_pieces['piece_'+str(p)] = dict_manage_shards
		
		print('\n')
		print(dict_manage_pieces)
		print('\n')

		with open(filename, 'w') as f_json:
			json.dump(dict_manage_pieces, f_json)

	conn.close()