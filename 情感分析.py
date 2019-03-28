# from aip import AipOcr #自动图片转文字
from aip import AipNlp #情感分析
from docx import Document
import re,os

# filepath = input('请输入图片：') #这是读取的图片存放的文件夹的路径，可以改为要读取的文件夹
input_txt = '王志学爱张本丽' #input('请输入文本信息：')

def get_file_content(filePath):
	with open(filePath, 'rb') as fp:
			return fp.read()


def check_txt(text):
	""" 调用情感倾向分析 """
	APP_ID = '15674997'
	API_KEY = 'ZRDmpx1cTtlhKaOdz8DdwF1r'
	SECRET_KEY = 'yKnYtkceM9NllGVkSDwCQrplGCrDNhQi'
	client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
	a = client.sentimentClassify(text) #调用情感分析
	# for key,value in a.items():
		# print(key,value)
	output = a["items"]
	positive_prob = output[0]['positive_prob'] #积极概率
	confidence = output[0]['confidence'] #置信度
	negative_prob = output[0]['negative_prob'] #消极概率
	sentiment = output[0]['sentiment'] #情感倾向
	print('{}:{}\n{}:{}\n{}:{}\n{}:{}'.format('积极概率',positive_prob,'置信度',confidence,\
	'消极概率',negative_prob,'情感倾向',sentiment))




# file_name = input('请输入您要分析的文本')
# file_name = os.path.normpath(file_name)
# # print(file_name)
# ls = Document(file_name).paragraphs
# txt1 = ''
# for i in ls:
	# txt1 += i.text
# txt1.replace('\n',' ') #删除所有回车空行
# print('备注：情感极性分类, 0:负向，1:中性，2:正向')
# print('文本字数:',len(txt1))
# if len(txt1) >= 1023:
	# for i in range(len(txt1)//1023-1):
		# txt2 = txt1[1024*i:1023*(i+1)]
		# print('本次分析字数：',len(txt2))
		# check_txt(txt2)
	# start_n = len(txt1)//1023
	# txt2 = txt1[1024*start_n:]
	# print('本次分析字数：',len(txt2))
	# check_txt(txt2)
	# #这里进行加权平均或者让百度取消字数限制--功能待定
# else:
	# check_txt(txt1)
	
	
def jpg2txt(filepath):
	'''图片转文字'''
	APP_ID = '15670439'
	API_KEY = 'GvGxsguvXNzf6QzYBD7j4A4X'
	SECRET_KEY = 'FBKURK9y96r2UrzcZUj6El82USrjhLdP'
	client = AipOcr(APP_ID, API_KEY, SECRET_KEY)	
	image = get_file_content(filepath)
	message = client.basicGeneral(image)
	txts = ''
	for i in message.get('words_result'):
		txts += i.get('words') + '\n'
	return txts


# a = jpg2txt(filepath) 
# print(a)
t = '张本丽爱王志学'
check_txt(t)
