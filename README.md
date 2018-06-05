# Python iOS自动打包脚本

## 使用说明  
1.1 使用python3编写，没有python3 环境的需要下载python3  
[python官网下载](https://www.python.org/downloads/)  
1.2 通过Homebrew安装Python3  
1.2.1 先搜索  

```
$ brew search python
 
输出：
app-engine-python          micropython                python3
boost-python               python                     wxpython
gst-python                 python-markdown            zpython
Caskroom/cask/awips-python               Caskroom/cask/mysql-connector-python
Caskroom/cask/kk7ds-python-runtime
```

1.2.2 安装,等待.....

```
$ brew install python3
```

1.2.3 安装完成

```
python3 --version
Python 3.6.3
```

1.3 打开autobuild文件，编辑下面的信息为自己的

```python
#工程名字（Target名字）
PROJECT_NAME = "xxxx"
#工程根目录 需要改为自己的路径
PROJECT_PATH = "/Users/xxxx/Desktop/xxxx/"
#archive 根路径 需要改为自己的路径
ARCHIVE_BASE_PATH = "/Users/xxxx/Desktop/App/Archive/"
#ipa根路径 需要改为自己的路径
IPA_BASE_PATH = "/Users/xxxx/Desktop/App/Ipa/"
#是否需要上传到fir 不需要则修改为False
NEED_UPLOAD_FIR = True
#上传到fir需要的token 可登陆fir获取
FIR_CLI_TOKEN = "xxxxxxxxxxxxxxxx"
```

```python
#AdHoc版本的 Bundle ID
ADHOC_BUNDLE_ID = "xxxx"
#ADHOC证书
ADHOC_CODE_SIGN_IDENTITY = "xxxx"
#描述文件
ADHOC_PROVISIONING_PROFILE_NAME = "xxxx"
#Target名字
ADHOC_TARGET_NAME = "xxxx"
#Scheme名字
ADHOC_SCHEME_NAME = "xxxx"
#导出ipa需要的plist文件 需要做对应修改
ADHOC_EXPORT_OPTIONS = "~/Desktop/autobuild/Adhoc_ExportOptions.plist"

#AppStore版本的 Bundle 
APPSTORE_BUNDLE_ID = "xxxx"
#APPSTORE证书
APPSTORE_CODE_SIGN_IDENTITY = "xxxx"
#描述文件
APPSTORE_PROVISIONING_PROFILE_NAME = "xxxx"
#Target名字
APPSTORE_TARGET_NAME = "xxxx"
#Scheme名字
APPSTORE_SCHEME_NAME = "xxxx"
#导出ipa需要的plist文件
APPSTORE_EXPORT_OPTIONS = "~/Desktop/autobuild/Appstore_ExportOptions.plist"


#企业版本的 Bundle ID
ENTERPRISE_BUNDLE_ID = "xxxx"
#企业证书
ENTERPRISE_CODE_SIGN_IDENTITY = "xxxx"
#描述文件
ENTERPRISE_PROVISIONING_PROFILE_NAME = "xxxx"
#Target名字
ENTERPRISE_TARGET_NAME = "xxxx"
#Scheme名字
ENTERPRISE_SCHEME_NAME = "xxxx"
#导出ipa需要的plist文件
ENTERPRISE_EXPORT_OPTIONS = "~/Desktop/autobuild/Enterprise_ExportOptions.plist"
```

### ExportOptions.plist文件 获取
配置好xcode环境 选择好证书&配置文件 Archive 以后 export 对应的ipa到桌面(adhoc,appstore,enterprise) 分别将对应的ExportOptions.plist 文件拷贝到autobuild目录中,根据类型,重命名为 以上的文件名称

``` python
ADHOC_EXPORT_OPTIONS = "~/Desktop/autobuild/Adhoc_ExportOptions.plist"
APPSTORE_EXPORT_OPTIONS = "~/Desktop/autobuild/Appstore_ExportOptions.plist"
ENTERPRISE_EXPORT_OPTIONS = "~/Desktop/autobuild/Enterprise_ExportOptions.plist"
```


### 修改完以上的xxxx之后 打开终端

```
cd Desktop/autobuild/
```
切换好之后执行

```
python3 autobuild.py
```

之后就是漫长的等待......
