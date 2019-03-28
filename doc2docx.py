#!/usr/bin/python
#coding=utf-8
import wordcloud,jieba,os
import docx
from docx import Document
from win32com.client import Dispatch
from scipy.misc import imread
import win32com


def doc2docx(path):
	'''转换doc文件为docx格式'''
	w = win32com.client.Dispatch('Word.Application')
	w.Visible = 0
	w.DisplayAlerts = 0
	doc = w.Documents.Open(path)
	newpath = os.path.splitext(path)[0] + '.docx'
	doc.SaveAs(newpath, 12, False, "", True, "", False, False, False, False)
	doc.Close()
	w.Quit()
	os.remove(path)
	return newpath


fold = input('请输入文件夹名称')
ls = []
if os.path.isdir(fold): #对文件夹中的每个doc文件进行转换
	for i in os.listdir(fold):
		i = os.path.join(fold,i)
		ls.append(i)
	print(len(ls))
	for i in range(len(ls)):
		if ls[i].split('\\')[-1][-3:] == 'doc':
			print(ls[i])
			doc2docx(ls[i])
elif os.path.isfile(fold):
	doc2docx(fold)
else:
	print('道路千万条，安全第一条。文件损坏，请确认后转换')


	
	
