#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : ${DATE} ${TIME}
# @Author : net
import time,os,sys,shutil
from tqdm import tqdm

def check(t):
	'''判断给定的文件夹t是否为效果图项目'''
	num = 0
	for i in os.listdir(t):
		if i == 'map' or i == 'maps':
			num += 1
	if num >= 1 and os.path.split(t)[1] not in ['map','maps']:
		return True
	else:
		return False
		


def kill_double(a,b):
	'''数据a去重，输出到b'''
	print('数据库优化耗时较长，请耐心等待......')
	if len(a) == 0 and len(b) == 0:
		b = []	
	else: #a,b都含有数据,更新b
		# print('监测点+++++')
		s = []
		a2 = a[:]
		for i in a+b:
			if i[0] not in s:
				s.append(i[0]) #[1.jpg,2.jpg]
		for i in b:
			a.append(i)
		del b[:]
		for i in s:
			b.append([i,'0','']) #初始化[[1.jpg,'1',d:\\],[2.jpg,'1',c:\\]]
		for i2 in b:
			s2 = []
			for i in range(len(a)):
				if a[i][0] == i2[0]:
					s2.append(eval(a[i][1]))
			i2[1] = str(sum(s2))
		for i in tqdm(a): #贴图路径变更
			for i2 in b:
				if i[0] == i2[0]:
					i2[2] = i[2]
		a = a2[:]


def del_wrong_name(a):
	'''清楚含有特殊符号的文件名'''
	for i in a:
		for j in '，,':
			if j in i:
				a.remove(i)

	
	
			
def check_dir(filepath,folder_list,files_list):
	'''遍历filepath下所有文件夹，包括子目录'''
	files = os.listdir(filepath)
	for fi in files:
		fi_d = os.path.join(filepath,fi)
		if os.path.isdir(fi_d):
			check_dir(fi_d,folder_list,files_list)
			folder_list.append(fi_d)
		else :
			files_list.append(fi_d)

			
		

def list_sort(a):
	'''数据排序从大到小'''
	for i in tqdm(range(len(a)-1)):
		for j in range(i+1,len(a)):
			if eval(a[i][1]) < eval(a[j][1]):
				a[i],a[j] = a[j],a[i]

			
def clean_db(db):
	'''清洗不符合要求的数据'''
	try:
		for i in db:
			if i[0].split('.')[-1] not in ['jpg','tga','png'] or eval(i[1]) not in range(9999):
				db.remove(i)
	except NameError:
				print('{}数据格式不正确，已清理'.format(i))
	
					

def load_db(ls,f): #加载数据库文件
	'''ls 是字典  output_csv 是数据库文件'''
	if os.path.exists(f) != False: #判断数据库文件是否存在
		fo = open (f,'r')
		file_1 = fo.readlines()	
		for i in file_1:
			ls.append(i)
		for i in range(len(ls)):
			ls[i] = ls[i].replace('\n','').split(',')
		# if len(ls) > 0:
			# print('{:-^50}'.format('数据库【'+ f + '】已加载'))	
	else:
		fo = open(f,'w')
		load_db(ls,f)
		fo.close()

	
def write_db(ls,f):
	'''将字典变量ls写入到本地文件f'''
	with open(f,'w')as file_1:
		for i in ls:
			i = ','.join(i)
			file_1.writelines(i + '\n')
	# print('\n数据库更新后为【{}】'.format(len(ls)))


def load_Cu_list(ls,f):
	'''加载已经整理项目的列表'''
	ls.clear()
	if os.path.exists(f): #判断数据库文件是否存在
		with open(f,'r')as file_1:
			txt = file_1.read()
			txt = txt.split('\n')
		for i in txt:
			if i not in ls and i != "":
				ls.append(i)
	else:
		fo = open(f,'w')
		load_Cu_list(ls,f)
		fo.close()


def write_Cu_list(ls,f):
	'''将整理过的项目列表写入到本地'''
	with open(f,'w')as file_1:
			file_1.write('\n'.join(ls))
	print('整理列表已更新【{}】'.format(len(ls)))


	
def check_count(f,ls):
	'''统计项目文件夹path中的贴图数量并写入到列表s'''
	bn = ()
	if os.path.isdir(f + r'\map'):
		tmp_folder = f + r'\map'
	else:
		tmp_folder = f + r'\maps'
	files_list = []
	folder_list = []
	list_b = []
	check_dir(tmp_folder,folder_list,files_list)
	files_list = list(set(files_list))
	del_wrong_name(files_list)
	for i in files_list:
		bn = os.path.split(i)
		i = bn[1] + ',' + '1' + ',' + bn[0]
		ls.append(i.split(','))


def creat_db(f):
	'''创建指定文件夹的数据库文件'''
	tmp_ls = []
	tmp_ls2 = []
	check_dir(f,tmp_ls,tmp_ls2)
	for i in range(len(tmp_ls2)):
		tmp_ls2[i] = list(os.path.split(tmp_ls2[i]))
		tmp_ls2[i][0],tmp_ls2[i][1] = tmp_ls2[i][1],tmp_ls2[i][0] #互换文件名和路径
		# print(tmp_ls2[i][:])
	bitmap_db_f = f + '.csv'
	with open(bitmap_db_f,'w')as file2:
		for i in tmp_ls2:
			file2.writelines(','.join(i) + '\n') #贴图库数据库新建完成
	print('贴图库数据库创建完成,文件名为{}'.format(bitmap_db_f))
		
		
def rebuild_db (load_csv,output_num,output_path):
	'''重建贴图库另存为备份,output_path是贴图库文件夹'''
	ids = [] #数据库变量
	tmp_list = [] #数据库临时变量
	folder_list = [] #临时变量
	files_list = [] #贴图列表变量
	bitmap_db_f = output_path + '.csv'
	num = len(output_path.split('\\'))-1
	load_db(ids,load_csv) #加载整理数据库.csv
	clean_db(ids)
	for i in ids:
		if i[1] >= output_num and i not in tmp_list:
			tmp_list.append(i)
	# print('本次整理共{}个贴图'.format(tmp_list)) #tmp_list是项目整理出的数据库，用户指定使用频率后的需要重建的数据
	for i in range(len(tmp_list)):
		del tmp_list[i][1]
		# print(tmp_list[i])
	# print(len(tmp_list)) #tmp_list是项目整理出的数据库，用户指定使用频率后的需要重建的数据
	tmp_list2 = [] #贴图库文件夹数据库
	if os.path.exists(bitmap_db_f):
		load_db(tmp_list2,bitmap_db_f)
		# print('贴图库数据库已经加载,后三位：',tmp_list2[-3:])
	else: #如果贴图库的数据库不存在，需要创建
		creat_db(output_path)
		load_db(tmp_list2,bitmap_db_f) #加载贴图数据库
	# print('原贴图库的数量',len(tmp_list2))
	# print('原贴图库后三位的内容是\n',tmp_list2[-3:])
	time.sleep(0.2)
	bitmap_new_list = [] #贴图名的列表
	for i in tmp_list2: #贴图库文件夹db
		if i[0] not in bitmap_new_list:
			bitmap_new_list.append(i[0])
	# print('bitmap_new_list 的数量',len(bitmap_new_list))
	# print('bitmap_new_list 后三位的内容是\n',bitmap_new_list[-3:])
	# time.sleep(1)
	for btm1 in tqdm(range(len(tmp_list))): #需要重建的数据
		old_path = os.path.join(tmp_list[btm1][1],tmp_list[btm1][0]) #拷贝的源文件
		# print('拷贝的源文件目录为：',tmp_list[btm1][1])
		# print('拷贝的源文件为：',old_path)
		if tmp_list[btm1][0] in bitmap_new_list:
			for btm2 in range(len(tmp_list2)):
				if tmp_list2[btm2][0] == tmp_list[btm1][0]:
					# print('标记++')
					new_path = tmp_list2[btm2][1]
					new_path2 = new_path.split('\\')
					new_path2[num] += 'copy' 
					new_path2 = '\\'.join(new_path2) #拷贝的目标目录
					# print('拷贝的目标文件夹为 ',new_path2)
					new_path = os.path.join(new_path2,tmp_list2[btm2][0]) #拷贝的目标文件
					# print('目标文件为 ',new_path)
					# time.sleep(0.1)
		else:
			# print('{}不存在于贴图库列表中'.format(tmp_list[btm1][0]))
			new_path2 = os.path.join(output_path + 'copy' ,'未分类贴图') #拷贝的目标目录
			new_path = os.path.join(new_path2,tmp_list[btm1][0]) #拷贝的目标文件
			# print('目标文件为 ',new_path)
		if os.path.exists(new_path2) == False:
			os.makedirs(new_path2)
			# print('创建目标文件夹 {}'.format(new_path2))
		try:
			shutil.copyfile(old_path,new_path)
		except FileNotFoundError:
			file_notfound.append(old_path)
	print('本次共{}个文件无法拷贝,数据可能存在其他电脑上,请检查'.format(len(old_path)))
			
			
			

def Arrangement():
	'''主程序，用于循环执行'''
	output_csv = r'd:\测试\数据库.csv'
	exist_A = input('【完成★退出】请按数字键 0\n\
【数据库排序】请按数字键 1 ——此项比较耗时，请耐心等待。\n\
【贴图库重生】请按数字键 2 ——贴图库重生会拷贝原贴图文件。\n\
【请输入需要整理的文件夹或者输入数字并回车】拖拽文件夹到此______').strip("\"") #用户输入项
	all_folder_list = [] #目录内所有文件夹的集合
	all_files_list = [] #目录内所有文件的集合
	T_list = [] #确认为效果图项目的文件夹
	if os.path.isdir(exist_A):
		check_dir(exist_A,all_folder_list,all_files_list) #step1检测文件夹中的所有子文件夹
		for i in all_folder_list: #遍历子文件夹,判断项目文件夹是否符合规范
			if check(i):
				T_list.append(i) #T_list为即将整理的文件夹
		print('本次整理的项目数量：{}'.format(len(T_list))) #step2 项目文件夹列表
		# print('    本次整理目录：',T_list[-3:])
		# print('首次整理将新建数据库名为 d:\测试\整理列表.csv  ')
		Cu_list = [] #整理列表变量from 整理列表.csv
		fold_name_list = []
		Cu_csv = r'd:\测试\整理列表.csv'
		# print('加载已整理过的目录......')
		load_Cu_list(Cu_list,Cu_csv) #step3 加载存档的项目文件夹
		if len(Cu_list) > 0:
			for i in Cu_list:
				fold_name_list.append(os.path.split(i)[1])
		print('加载已整理过的目录数量',len(Cu_list))
		t_list2 = []
		if len(T_list) > 0: #如果项目文件夹列表大于0,且不存在于加载的项目文件夹中,则继续
			for i in range(len(T_list)):
				if T_list[i] not in Cu_list and os.path.split(T_list[i])[1] not in fold_name_list:				
					t_list2.append(T_list[i])
				else:
					print('\r{:<30}'.format(T_list[i] + ' 已整理,飘过~',end=''))
					time.sleep(0.1)
			if len(t_list2) == 0:
				print('\n{:-^30}'.format('本次没有需要整理的项目，都已经整理过了'))
		else:
			print('\n{:-^30}'.format('没有定义中的项目'))
		# print('本次整理项目：',t_list2[-3:])
		tmp_db = []
		load_db(tmp_db,output_csv) #step 1 加载已有数据库
		clean_db(tmp_db)
		# print('加载数据库：   ',tmp_db[-3:])
		print('加载已有数据{},贴图数为:{}'.format(output_csv,len(tmp_db)))
		ds_db = [] #项目内贴图
		num = 0
		for i in range(len(t_list2)): #遍历本轮需要检测的效果图项目文件夹
			num += 1
			tmp_db2 = [] #临时列表
			check_count(t_list2[i],tmp_db2) #获取项目的贴图数据并写入变量
			print('\r第【 {} 】个项目,项目名:   {},贴图数为【{}】个'.format(num,t_list2[i],len(tmp_db2)))
			# print('监测点+++:',tmp_db2[:])
			# time.sleep(0.01)
			ds_db += tmp_db2 #本轮整理效果图项目的数据合并
		print('本轮整理数据{}'.format(len(ds_db)))
		ds_db += tmp_db #数据库数据与本轮整理的数据合并
		print('数据库数据更新为{}'.format(len(ds_db)))
		clean_txt = input('是否清洗数据?是请按【Y】,否请按【N】,自动保存请按任意键\n\
注意：清洗数据库会清除除【jpg】,【tga】,【png】以外的贴图数据。')
		tmp_db_new2 = []
		if clean_txt in ['Y','y']:
			print('清除图片格式前{}'.format(len(ds_db)))
			clean_db(ds_db)
			print('清除图片格式后{}'.format(len(ds_db)))
			write_db(ds_db,output_csv)
			kill_double(ds_db,tmp_db_new2) #融合重复贴图元素
			print('优化数据后{}'.format(len(tmp_db_new2)))
			write_db(tmp_db_new2,output_csv)
			print('数据已存档')
		elif clean_txt == 'N' or clean_txt == 'n':
			print('清除图片格式前{}'.format(len(ds_db)))
			# kill_double(ds_db,tmp_db_new2)
			clean_db(ds_db)
			print('清除图片格式后{}'.format(len(ds_db)))
			write_db(ds_db,output_csv)
			print('数据已存档')
		else:
			print('其他输入......')
			print('数据即将存档')
			write_db(ds_db,output_csv)
		# print('标记000',Cu_list2[:])
		write_Cu_list(t_list2 + Cu_list ,Cu_csv) #更新文件整理列表.csv
	elif exist_A == '0': #退出开关
		exit()
	elif exist_A == '2': #重生成数据库文件夹
		load_csv = input('请加载数据库___')
		output_num = input('输出的图片频次需要大于___ ')
		output_path = input('您的贴图数据库根目录___')
		rebuild_db (load_csv,output_num,output_path)
	elif exist_A == '1':#数据库文件排序
		input_name = input('输入需要排序的文件：')
		tmp_db_new = []
		load_db(tmp_db_new,input_name)
		list_sort(tmp_db_new)
		write_db(tmp_db_new,input_name)
		print('【根据贴图使用频率排序完成】')
	else:
		print('WANNING!您输入的文件夹名称不存在请重新输入,退出请按0')
	
		
		
print('{:*^111}'.format('项目贴图整理工具'))
print('{: <100}'.format('* 作者：net'))
print('{: <100}'.format('* 版本：0.08'))
print('{: <100}'.format('* 测试平台：windows10'))
print('{: <100}'.format('* 更新日期：2019-3-26'))
print('{: <50}'.format('* 功能介绍：输入你需要统计贴图的项目目录，本工具会自动统计出项目用到的贴图'))
print('{: <50}'.format('* 并记录在数据库文件中,默认数据库文件为d:\测试\数据库.csv\
整理过的项目会保存在另一个数据库d:\测试\整理列表.csv中'))
# print('{: <50}'.format('* 更新日志：2019-3-26 增加数据库前N个贴图的输出功能,输出路径保持为用户贴图库的分类,\
# 不改变用户查找贴图的习惯'))
print('{:*^119}'.format('*'))
check_i = 0
while check_i < 10: #限制单次启动整理文件夹的次数
	Arrangement()
	check_i += 1
print('即将关闭,你该歇歇了,付费解除限制')
for i in range(10,0,-1):
	print('\r{: >2}'.format(i),end='')
	time.sleep(0.8)	

	

