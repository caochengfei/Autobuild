#!usr/bin/evn python
import os
import subprocess

# 1.简易打包方式 将.app文件快速打包成ipa
# .app文件路径，在xcode中拖到此处即可、
APP_FILE_FULL_PATH = '/Users/caochengfei/Library/Developer/Xcode/DerivedData/FFQRCode-cznhijxpwiexfcbbcngerpvfkwqo/Build/Products/Debug-iphonesimulator/FFQRCode.app'
# PayLoad文件夹路径 按需要改成自己的路径
PAYLOAD_PATH = '/Users/xxxx/Desktop/Payload'
# 存放ipa文件的文件夹路径 按需要改成自己的路径
PACK_BAG_PATH = '/Users/xxxx/Desktop/iOSPack'

FIR_CLI_TOKEN = 'xxxxxxxxxxxxxxxxxxxxx'

class FastBuild():
	"""docstring for ClassName"""
	def __init__(self):
		pass

	def bulidIPA(self):
		os.mkdir(PAYLOAD_PATH)
		#将app 拷贝到PayLoadPath路径下
		subprocess.getoutput('cp -r %s %s'%(APP_FILE_FULL_PATH,PAYLOAD_PATH))
		#在桌面上创建packBagPath文件夹
		subprocess.getoutput('mkdir -p %s'%PACK_BAG_PATH)
		#将PayLoadPath文件拷贝到packBagPath文件夹中
		subprocess.getoutput('cp -r %s %s'%(PAYLOAD_PATH,PACK_BAG_PATH))
		#删除PayLoadPath文件夹
		subprocess.getoutput('rm -rf %s'%(PAYLOAD_PATH))
		#切换到packBagPath
		os.chdir(packBagPath)
		#压缩 zip
		subprocess.getoutput('zip -r Payload.zip Payload')
		#重命名为ipa
		subprocess.getoutput('mv Payload.zip Payload.ipa')
		subprocess.getoutput('rm -rf Payload')
		print('\n**************** 打包成功 ******************\n')


	def install_fir_cli(self):
		print('********************判断是否安装fir-cli**********************')
		fir_process = subprocess.getoutput('fir --version')
		if 'fir-cli' in fir_process:
			print('******安装 fir-cli 成功******')
			return True
		
		print('***********************开始安装fir-cli************************')
		fir_process = subprocess.Popen('sudo gem install fir-cli',shell = True)
		fir_process.wait()
		if fir_process.returncode == 0:
			print('******安装 fir-cli 成功******')
			return True
		else:
			print('******安装 fir-cli 失败******')
			return False
			
			

	def upload_fir(self):
		print('开始上传')
		if self.install_fir_cli() == True:
			fir_process = subprocess.Popen('fir login %s'%(FIR_CLI_TOKEN),shell = True)
			fir_process.wait()
			if fir_process.returncode == 0:
				fir_process = subprocess.Popen('fir publish %s/%s'%(PACK_BAG_PATH,'Payload' + '.ipa'),shell = True)
				fir_process.wait()
				if fir_process.returncode == 0:
					print('上传成功')
			else:
				print('登录fir失败')
		

fastbuild = FastBuild()
fastbuild.bulid_ipa()
	


