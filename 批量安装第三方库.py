import os
ls_n = []
ls_m = []
os.system('python -m pip install --upgrade pip')
for i in os.popen('pip list'):
	i = i.split('\n')
	ls_n.append(i)
for i in range(2,len(ls_n)):
	ls_m.append(ls_n[i][0])
ls_n.clear()
for i in range(len(ls_m)):
	ls_m[i] = ls_m[i].split(' ')[0]
	ls_n.append(ls_m[i])
libs = {'requests','scrapy','pyspider','pyinstaller','imageio',\
		'numpy','pandas','matplotlib','scipy','seaborn',\
		'pdfminer3','pypdf2','openpyxl','pyopengl','docopt',\
		'xlsxwriter','xlrd','python-docx','pdfkit','xlwt','docx',\
		'beautifulsoup4','wheel','networkx','sympy',\
		'django','flask','werobot','pillow','tornado',\
		'wordcloud','jieba','ghostscript','baidu-aip','tqdm',\
		'PyQt5','opencv-python','scikit-learn','tensorflow','mxnet'\
		'pygame'}
try:
	for lib in libs:
		if lib not in ls_n:
			os.system('pip install ' + lib)
	print('Successful')
except:
	print('Faild Somehow')
