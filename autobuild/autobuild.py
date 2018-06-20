#!usr/bin/evn python
import os
import subprocess
import time
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart

#工程名字（Target名字）
PROJECT_NAME = "xxxx"
#工程根目录 需要改为自己的路径
PROJECT_PATH = "/Users/xxxx/Desktop/xxxx/"
#archive 根路径 需要改为自己的路径
ARCHIVE_BASE_PATH = "/Users/xxxx/Desktop/App/Archive/"
#ipa根路径 需要改为自己的路径
IPA_BASE_PATH = "/Users/xxxx/Desktop/App/Ipa/"
#上传到fir需要的token fir官网获取
FIR_CLI_TOKEN = "xxxx"
#蒲公英ukey 蒲公英官网获取
PGYER_UKEY = "xxxx"
#蒲公英apikey 蒲公英官网获取
PGYER_API_KEY = "xxxx"

#AdHoc版本的 Bundle ID
ADHOC_BUNDLE_ID = "xxxx"
#ADHOC证书名&描述文件
ADHOC_CODE_SIGN_IDENTITY = "xxxx"
ADHOC_PROVISIONING_PROFILE_NAME = "xxxx"
#Target名字
ADHOC_TARGET_NAME = "xxxx"
#Scheme名字
ADHOC_SCHEME_NAME = "xxxx"
#导出ipa需要的plist文件
ADHOC_EXPORT_OPTIONS = "~/Desktop/autobuild/Adhoc_ExportOptions.plist"

#AppStore版本的 Bundle 
APPSTORE_BUNDLE_ID = "xxxx"
#APPSTORE证书名&描述文件
APPSTORE_CODE_SIGN_IDENTITY = "xxxx"
APPSTORE_PROVISIONING_PROFILE_NAME = "xxxx"
#Target名字
APPSTORE_TARGET_NAME = "xxxx"
#Scheme名字
APPSTORE_SCHEME_NAME = "xxxx"
#导出ipa需要的plist文件
APPSTORE_EXPORT_OPTIONS = "~/Desktop/autobuild/Appstore_ExportOptions.plist"


#企业版本的 Bundle ID
ENTERPRISE_BUNDLE_ID = "xxxx"
#企业证书名&描述文件
ENTERPRISE_CODE_SIGN_IDENTITY = "xxxx"
ENTERPRISE_PROVISIONING_PROFILE_NAME = "xxxx"
#Target名字
ENTERPRISE_TARGET_NAME = "xxxx"
#Scheme名字
ENTERPRISE_SCHEME_NAME = "xxxx"
#导出ipa需要的plist文件
ENTERPRISE_EXPORT_OPTIONS = "~/Desktop/autobuild/Enterprise_ExportOptions.plist"

SDK = "iphoneos"


class AutoBuild():
	def __init__(self):
		print("************** 选择打包方式,默认AppStore ***************")
		self.way = input('Please select the packing type: (1.appstore 2.adhoc 3.enterprise) \n')
		if self.way == '2':
			self.bundle_id = ADHOC_BUNDLE_ID
			self.code_sign_identity = ADHOC_CODE_SIGN_IDENTITY
			self.provisioning_profile = ADHOC_PROVISIONING_PROFILE_NAME
			self.scheme_name = ADHOC_SCHEME_NAME
			self.target_name = ADHOC_TARGET_NAME
			self.export_options = ADHOC_EXPORT_OPTIONS

		elif self.way == '3':
			self.bundle_id = ENTERPRISE_BUNDLE_ID
			self.code_sign_identity = ENTERPRISE_CODE_SIGN_IDENTITY
			self.provisioning_profile = ENTERPRISE_PROVISIONING_PROFILE_NAME
			self.scheme_name = ENTERPRISE_SCHEME_NAME
			self.target_name = ENTERPRISE_TARGET_NAME
			self.export_options = ENTERPRISE_EXPORT_OPTIONS

		else:
			self.bundle_id =  APPSTORE_BUNDLE_ID
			self.code_sign_identity = APPSTORE_CODE_SIGN_IDENTITY
			self.provisioning_profile = APPSTORE_PROVISIONING_PROFILE_NAME
			self.scheme_name = APPSTORE_SCHEME_NAME
			self.target_name = APPSTORE_TARGET_NAME
			self.export_options = APPSTORE_EXPORT_OPTIONS

		print("********* 请选择configuration类型，默认Release *********")
		if input('**** Please select the configuration type (1.Release 2.Debug) \n') == '2':
			self.configuration = "Debug"
		else:
			self.configuration = "Release"

		#设置Archive_Path
		self.time = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime())

		self.archive_path = ARCHIVE_BASE_PATH + self.bundle_id + "/" + self.time + "/" + self.scheme_name   

		#设置导出的ipa文件路径
		self.ipa_path = IPA_BASE_PATH + self.bundle_id + "/" + self.time + "/" + self.scheme_name

		self.upload_channel = input('**** Please select the upload_channel type (1.Pgyer 2.Fir ) \n')


	def build(self):
		if input("Please select the Project type: (1.Use Cocoapods 2.Don't use Cocoapods) \n") == '1':
			self.clear_build()
			return self.build_workspace()
		else:
			self.clear_build()
			return self.build_xcodeproj()


	def build_xcodeproj(self):
		print('*****************开始打包******************')

		archive_cmd = "xcodebuild archive -archivePath %s \
		-project %s.xcodeproj \
		-scheme %s \
		-configuration %s  \
		-sdk %s  \
		CODE_SIGN_IDENTITY='%s'  \
		PROVISIONING_PROFILE='%s' "%(self.archive_path,PROJECT_NAME,
			self.scheme_name,
			self.configuration,
			SDK,
			self.code_sign_identity,
			self.provisioning_profile)

		print(archive_cmd)

		os.chdir(PROJECT_PATH)
		process = subprocess.Popen(archive_cmd,shell=True)
		process.wait()

		if process.returncode != 0:
			print('********* archive失败 ***********')
			return False
		else:
			print('********* archive成功 ***********')
			return True

	def build_workspace(self):

		print('*****************开始打包******************')
		archive_cmd= "xcodebuild archive -archivePath %s \
		-workspace %s.xcworkspace \
		-scheme %s \
		-configuration %s  \
		-sdk %s \
		CODE_SIGN_IDENTITY='%s' \
		PROVISIONING_PROFILE_SPECIFIER='%s' \
		"%(self.archive_path,
			PROJECT_NAME,
			self.scheme_name,
			self.configuration,
			SDK,
			self.code_sign_identity,
			self.provisioning_profile)

		print(archive_cmd)
		#切换到工程目录
		os.chdir(PROJECT_PATH)
		process = subprocess.Popen(archive_cmd,shell=True)
		process.wait()

		if process.returncode != 0:
			print('*************archive失败************')
			return False
		else:
			print('*************archive成功************')
			return True


	def bulid_ipa(self):
		print('**************开始编译ipa*************')

		archivePath = self.archive_path + ".xcarchive"
		export_cmd = "xcodebuild -exportArchive \
		-archivePath %s \
		-exportPath %s \
		-exportOptionsPlist %s "%(archivePath,self.ipa_path,self.export_options)
		print(export_cmd)

		process = subprocess.Popen(export_cmd,shell=True)
		process.wait()

		if process.returncode != 0:
			print('**************编译ipa失败*************')
			return False
		else:
			print('**************编译ipa成功*************')
			return True

	def clear_build(self):
		print('**********************clean***********************')
		os.chdir(PROJECT_PATH)
		subprocess.getoutput('xcodebuild clean')
		
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
				fir_process = subprocess.Popen('fir publish %s/%s'%(self.ipa_path,self.scheme_name + '.ipa'),shell = True)
				fir_process.wait()
				if fir_process.returncode == 0:
					print('上传Fir成功')
				else:
					print('上传Fir失败')
			else:
				print('登录fir失败')

	def upload_pgyer(self):
		print('********************开始上传到蒲公英**********************')

		# test_path = '/Users/caochengfei/Desktop/djcInhouse.ipa'
		# test_curl = "curl \
		# -F 'file=@%s' \
		# -F 'uKey=%s' \
		# -F '_api_key=%s'\
		# https://www.pgyer.com/apiv1/app/upload"%(test_path,PGYER_UKEY,PGYER_API_KEY)

		curl_str = "curl \
		-F 'file=@%s/%s' \
		-F 'uKey=%s' \
		-F '_api_key=%s'\
		https://www.pgyer.com/apiv1/app/upload"%(self.ipa_path,self.scheme_name+'.ipa',PGYER_UKEY,PGYER_API_KEY)

		process = subprocess.Popen(curl_str,shell=True,stdout=subprocess.PIPE)
		for line in process.stdout:
			result = json.loads(line)
		process.wait()
		if process.returncode == 0:
			print('上传成功')
			app_qrcode_url = result['data']['appQRCodeURL']
			self.send_email(app_qrcode_url)
		else:
			print('上传失败')

	def send_email(self,url=None):

		print('****************发送邮件通知**********************')
		main_host = 'smtp.qq.com'
		# 发件邮箱
		sender = 'xxxx@qq.com'
		# 授权码 || 密码
		sender_pwd = 'xxxx'
		# 收件人列表
		receivers = '''xxxx@qq.com,
					 xxxx@qq.com,
					 xxxx@qq.com,
					 xxxx@qq.com,
					 xxxx@qq.com'''

		#设置邮件标题,此处自己随意填写
		title = '虫娘又有新版本了'

		to_addrs = receivers.split(',')

		message = MIMEMultipart()
		message['from'] = Header(sender)
		message['to'] = Header(','.join(to_addrs))
		message['Subject'] = Header(title 'utf-8')

		html = """ 
		<html> 
		  <head></head> 
		  <body> 
		    <p>您的内测包已到，请点击查收<br> 
		       请点击这里 <a href="%s">点击获取二维码</a>. 
		    </p> 
		  </body> 
		</html> 
		"""%(url)

		message.attach(MIMEText(html,'html','utf-8'))

		try:
			smtp = smtplib.SMTP()
			smtp.connect(host=main_host,port=587)
			smtp.ehlo()
			smtp.starttls()
			smtp.login(sender,sender_pwd)
			smtp.sendmail(sender,to_addrs,message.as_string())
		except smtplib.SMTPHeloError:
			print(smtplib.SMTPException)
			print('Error: 无法发送邮件SMTPException')
		except smtplib.SMTPConnectError:
			print('Error: 无法发送邮件SMTPConnectError')
		except smtplib.SMTPAuthenticationError:
			print('Error: 无法发送邮件SMTPAuthenticationError')
		except smtplib.SMTPHeloError:
			print('Error: 无法发送邮件SMTPHeloError')
		except smtplib.SMTPDataError:
			print('Error: 无法发送邮件SMTPDataError')

build = AutoBuild()
if build.build() == False:
	exit()

if build.bulid_ipa() == False:
	exit()

if build.upload_channel == '2':
	build.upload_fir()
else:
	build.upload_pgyer()

















