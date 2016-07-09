此为抽取出的MES的公共框架源码，尽量不要改动。

此目录下有 dist 目录，该目录下有rpm文件用于直接在 centos系统上安装此公共框架。目录下有 install_guide 引导安装的具体步骤。


打包rpm 使用的命令是在当前目录下运行： python setup.py bdist_rpm. 会将整个框架代码打包成rpm 文件到 dist目录下。

打包的rpm 中不包含 根目录下的addons目录，此目录下的模块需要随同公司编写的模块一同发布。

请知！
