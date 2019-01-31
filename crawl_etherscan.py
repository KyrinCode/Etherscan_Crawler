import requests
from bs4 import BeautifulSoup
import bs4
import re
import sqlite3
import sys

def getHTMLtext(url):
    try:
    	headers = {'user-agent': 'Mozilla/5.0'}
    	r = requests.get(url, headers=headers, timeout=60)
    	r.raise_for_status()
    	r.encoding = r.apparent_encoding
    	return r.text
    except:
    	return "Error"

def get_current_blockid(url):
	"""得到当前最新区块的id"""
	html = getHTMLtext(url)
	soup = BeautifulSoup(html, 'html.parser')
	current_blockid = int(soup.find('tbody').find('a').string)
	print("Current newest block_id is: {}".format(current_blockid))
	return current_blockid

def crawl_single_block(url, blockid, c, itemnum=50):
	"""
	爬取一个区块的交易信息
	itemnum: 一个页面默认最多存放的交易数
	"""
	url_temp = url + str(blockid)
	html = getHTMLtext(url_temp)
	match = re.search(r'Page\s\<b\>1\<\/b\>\sof\s\<b\>\d+', html)
	depth = int(match.group(0).split('>')[-1])

	print("*Block_id: {}'s page number = {}".format(blockid, depth))
	print("--------------------Start crawling block_id: {}--------------------".format(blockid))
	Txnscount = 0
	for page in range(1,depth+1):
		url_temp_page = url_temp + "&p={}".format(page)
		#print(url_temp_page)
		html = getHTMLtext(url_temp_page)
		soup = BeautifulSoup(html, 'html.parser')
		trs = soup.find('tbody').contents
		for tr in trs:
			if type(tr) == bs4.element.Tag:
				tds = tr.contents
				if len(tds) != 8:
					break
				td_tx_sender = tds[3]
				tx_sender = td_tx_sender.find('a').get('href').split('/')[-1]
				td_tx_receiver = tds[5]
				tx_receiver = td_tx_receiver.find('a').get('href').split('/')[-1]
				c.execute("INSERT INTO ETHERSCAN (BLOCK_ID, SENDER, RECEIVER) \
					VALUES (?, ?, ?)", (blockid, tx_sender, tx_receiver))
				#print("Sender: {} -> Receiver: {}".format(tx_sender, tx_receiver))
				Txnscount += 1
	print("A total of {} Txns found".format(Txnscount))
	print("--------------------Finish crawling block_id: {}-------------------".format(blockid))


def crawl_etherscan(url, current_blockid, blocknum, c):
	"""爬取从当前区块往前多少个区块的交易信息"""
	for i in range(blocknum):
		blockid = current_blockid - i
		try:
			crawl_single_block(url, blockid, c)
		except:
			with open('blocks_missed.txt','w') as f:
				f.write(str(blockid))
			print("Error: block_id: {} failed".format(blockid))
			return
	with open('blocks_missed.txt','w') as f:
		f.write(str(blockid - 1))
	print("------------Finish crawling {} blocks till block_id: {}-------------".format(blocknum, current_blockid))

def get_earliest_blockid(c):
	cursor = c.execute("SELECT min(block_id) from ETHERSCAN")
	for row in cursor:
		return row[0]

def get_last_missed_blockid(c):
	"""读取文件中上一次出错的block_id并返回，同时删除数据库中小于等于block_id的记录"""
	with open('blocks_missed.txt','r') as f:
		blockid = f.read()
	i = int(blockid)
	earliest_blockid = get_earliest_blockid(c)
	flag = 0#标记是否数据库中存在上次出错时的block_id
	while i >= earliest_blockid:
		flag = 1
		c.execute("DELETE from ETHERSCAN where BLOCK_ID = '"+ str(i) +"';")
		i -= 1
	if flag == 1:
		print("------------Delete block_id: {} to block_id: {}------------".format(earliest_blockid, blockid))
	return int(blockid)

if __name__ == '__main__':
	#打开数据库，操作ETHERSCAN表
	conn = sqlite3.connect('etherscan.db')
	print("Opened database successfully")
	c = conn.cursor()
	try:
		c.execute('''CREATE TABLE ETHERSCAN
			(BLOCK_ID INT NOT NULL,
			SENDER TEXT NOT NULL,
			RECEIVER TEXT NOT NULL);''')
	except:
		print("Table ETHERSCAN already exists")
	else:
		print("Table created successfully")

	#获得当前最新区块号
	#url = "https://etherscan.io/blocks"
	#current_blockid = get_current_blockid(url)

	#允许100次出错机会
	for i in range(1):
		#从文件中读取上次抓取出错的区块
		blockid = get_last_missed_blockid(c)
		conn.commit()
		print("Updated database successfully")

		#抓取区块将交易写入数据库
		url = "https://etherscan.io/txs?block="
		blocknum = 1
		crawl_etherscan(url, blockid, blocknum, c)
		conn.commit()
		print("Updated database successfully")

	conn.close()

