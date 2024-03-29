# smb_client_on_windows_can_specify_port
a SMB client can be specify port on Windows

一个windows上能够定义端口的smb客户端



当前版本：v0

该版本存在各种 bug、用户体验差 ，并不能百分百保证正常运行

已知问题:

1. 新建的xlsx文档打开提示文件有损坏(或错误)
2. 速度很慢，应该是没有缓存而导致的问题



## 使用

#### 驱动安装

1. 下载驱动 [dokan 1.2.2驱动](https://github.com/dokan-dev/dokany/releases/download/v1.2.2.1000/DokanSetup_redist.exe)
2. 安装驱动

#### 客户端使用

1. 下载客户端，客户端是7z格式的压缩文件。 [客户端下载页面](https://github.com/cxwithyxy/smb_client_on_windows_can_specify_port/releases)
2. 用解压工具解压7z格式的客户端
3. 打开解压出来的文件夹
4. 把 setting.ini.demo 重命名成 setting.ini
5. 用支持utf8文本编码格式的编辑器编辑 setting.ini 文件
6. 修改 setting.ini 文件中的 ip、username、passwd，对应为smb服务器ip地址，smb账号、密码
7. 运行 smb_client.exe

#### setting.ini 配置说明

| smb项            | 说明                     |
| ---------------- | ------------------------ |
| ip               | ip地址                   |
| username         | smb用户名                |
| passwd           | 密码                     |
| port             | 端口                     |
| direct_tcp       | 0为默认连接, 1为直接连接 |
| enter_path       | 共享文件夹名字           |
| thread           | 线程数                   |
| connection_count | 连接数                   |

| disk项      | 说明     |
| ----------- | -------- |
| mount_point | 挂载盘符 |
| volume_name | 盘的名字 |



## 开发

#### 安装依赖

```
pip install -r requirements.txt
```

由于 fs.smbfs 对 linux 的 smb 服务器有些问题，因此请移除旧的 fs.smbfs 并安装我修改后的。

移除旧的 fs.smbfs

```
pip uninstall fs.smbfs
```

安装我修改后的 fs.smbfs

```
pip install git+https://github.com/cxwithyxy/fs.smbfs.git
```

> 注：请自行配置代理服务已避免出现404等无法访问的相关问题，建议用环境变量的方式配置
>
> https_proxy=http://127.0.0.1:1080
>
> http_proxy=http://127.0.0.1:1080

#### 打包EXE

```
pyinstaller index.spec
```



