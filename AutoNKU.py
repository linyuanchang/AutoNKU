#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import path, system
import sys
import urllib
import requests
import json
import configparser
import browser_cookie3
import webbrowser
from time import time
from tkinter import Tk, Canvas, messagebox, YES

from PIL import Image, ImageTk


class Nankai():

	"""docstring for ClassName"""
	def __init__(self):
		
		self.cookie = None

		self.config = None

		self.data = {
			"q1": "36.5",
			"q16": "36.4",
			"q17": "36.6",
			"q2": "天津",
			"q10_show": "天津市/天津市/南开区",
			"q10": "120000/120000/120104",
			"q9": "宿舍",
			"q14": "13820912345",
			"q15": "从前有座庙",
			"q4": "N",
			"q5": "N",
			"q20": "N",
			"q11": "N",
			"q12": "N",
			"q13": "green",
			"q22": "green",
			"q24": "N",
			"q23": "2",
			"q18": "3",
			"q19": "2",
			"q8": ""
		}
		
	# 获取登录信息
	def get_cookie(self):
		if not self.cookie:
			try:
				self.cookie = browser_cookie3.firefox(domain_name='jkcj.nankai.edu.cn')
			except Exception as e:
				pass

		if not self.cookie:
			try:
				self.cookie = browser_cookie3.edge(domain_name='jkcj.nankai.edu.cn')
			except Exception as e:
				pass

		if not self.cookie:
			try:
				self.cookie = browser_cookie3.chrome(domain_name='jkcj.nankai.edu.cn')
			except Exception as e:
				pass

		
		return self.cookie

	# 打开登录授权页面
	def open_browser(self):
		browser = None
		opened = False

		if not browser:
			try:
				browser = webbrowser.get('firefox')
				opened = browser.open('https://feishu.nankai.edu.cn/?appid=229')
			except Exception as e:
				pass


		if not browser:   
			r = system('start msedge https://feishu.nankai.edu.cn/?appid=229')
			if r ==0 :
				opened = True
		
		if not browser:
			try:
				browser = webbrowser.get('chrome')
				opened = browser.open('https://feishu.nankai.edu.cn/?appid=229')
			except Exception as e:
				pass

		return opened

	def get_data(self, config_file='data.txt'):
		self.config = configparser.ConfigParser()
		self.config.read(config_file, encoding='utf-8')

		temperature = self.config['Temperature']
		person = self.config['Person']
		dormitory = self.config['Dormitory']
		other = self.config['Other']

		self.data['q1'] = temperature.get('night')
		self.data['q16'] = temperature.get('morning')
		self.data['q17'] = temperature.get('noon')
		self.data['q14'] = person.get('mobile')
		self.data['q15'] = person.get('address')
		self.data['q18'] = dormitory.get('ventilation')
		self.data['q19'] = dormitory.get('disinfection')
		self.data['q8'] = other.get('feedback')
		

	def submit(self):
		url = "https://jkcj.nankai.edu.cn/healthgather/Inschool/addInschoolGather?time=%d" % (int(time())*1000) # 接口地址


		# 消息头数据
		headers = {
			'Accept': '*/*',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
			'Connection': 'keep-alive',
			'Content-Length': '734',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'DNT': '1',
			'Host': 'jkcj.nankai.edu.cn',
			'Origin': 'https://jkcj.nankai.edu.cn',
			'Referer': 'https://jkcj.nankai.edu.cn/mobile/register/inschool.html?time=%d' % int(time()),
			'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
			'sec-ch-ua-mobile': '?0',
			'sec-ch-ua-platform': '"Linux"',
			'Sec-Fetch-Dest': 'empty',
			'Sec-Fetch-Mode': 'cors',
			'Sec-Fetch-Site': 'same-origin',
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
			'X-Requested-With': 'XMLHttpRequest',
		}

		payload = {
			'data': json.dumps(self.data),
			'status': 1,
		}

		response = requests.post(url, data=payload, headers=headers, cookies=self.cookie, verify=True)
		response = json.loads(response.text)

		return response



if __name__ == '__main__':
	# print("防疫信息填写结果，如有错误打开网页版重试：https://feishu.nankai.edu.cn/?appid=229")

	# exe根目录
	pwd = path.dirname(path.realpath(sys.executable)) # pyinstaller打包
	# pwd = path.dirname(path.realpath(__file__)) # python脚本
	
	nankai = Nankai()
	cookie = nankai.get_cookie()
	if not cookie:
		tk = Tk()
		tk.withdraw()  # 退出默认 tk 窗口
		tk.iconbitmap(path.join(pwd, 'image', 'nku.ico'))
		result = messagebox.showinfo('提示', 'AutoNKU检测到您未登录，请登录后手动运行程序。\n现在转入登录页面。')
		if result == 'ok':
			opened = nankai.open_browser()
			if not opened:
				messagebox.showinfo('提示', 'AutoNKU无法打开Edge、Chrome或Firefox浏览器，请确认已经安装相应浏览器。')
		tk.destroy()
	else:	
		# 背景图片
		image = Image.open(path.join(pwd,'image', 'flower.jpg'))
		width = 400
		w_percent = width / float(image.size[0])
		height = int(float(image.size[1]) * float(w_percent))

		# GUI
		tk = Tk()
		tk.iconbitmap(path.join(pwd, 'image', 'nku.ico'))
		tk.title("南开大学防疫信息自动填报系统")
		tk.wm_attributes('-topmost', 1)

		ws = tk.winfo_screenwidth()
		hs = tk.winfo_screenheight()
		# 计算 x, y 位置
		x = (ws/2) - (width/2)
		y = (hs/2) - (height/2)
		tk.geometry('%dx%d+%d+%d' % (width, height, x, y))
		tk.resizable(0,0)

		# 画布渲染
		canvas = Canvas(tk, width = width, height = height, bd = 0)	 
		canvas.config(highlightthickness=0)

		# 背景图片渲染
		image = image.resize((width, height),  Image.Resampling.LANCZOS)
		photo = ImageTk.PhotoImage(image)
		canvas.create_image(width/2, height/2, image = photo)
		canvas.pack(expand = YES)

		# 提交数据
		nankai.get_data(config_file = path.join(pwd, 'data.txt'))
		response = nankai.submit()

		# 处理返回结果
		if response['code'] == '001':
			msg = '%s' % '提交成功'
			canvas.create_text(width/2, height-22, text = msg , fill = 'pink', font=('微软雅黑',18))
		elif response['code'] == '010':
			msg = '%s' % response['message']
			canvas.create_text(width/2, height-44, text = msg , fill = 'yellow', font=('微软雅黑',16))
			canvas.create_text(width/2, height-22, text = '请重新登录' , fill = 'yellow', font=('微软雅黑',16))
		else:
			msg = '%s' % response['message']
			canvas.create_text(width/2, height-22, text = msg , fill = 'yellow', font=('微软雅黑',16))

		tk.mainloop()

