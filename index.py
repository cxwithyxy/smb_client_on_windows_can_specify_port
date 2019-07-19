# from file_io_emulation.Server import Server as FS_server

# FS_server().start()
# while(True):
#     a = input("==>\n")
#     if(a == "stop"):
#         FS_server().stop()
#     if(a == "q"):
#         break
import fs
import fs.smbfs
import configparser

conf = configparser.ConfigParser()
conf.read('setting.ini', encoding="utf8")

smb_fs = fs.smbfs.SMBFS(
    conf['smb']['ip'],
    username = conf['smb']['username'],
    passwd = conf['smb']['passwd'],
    timeout = 15,
    port = int(conf['smb']['port']),
    direct_tcp = int(conf['smb']['direct_tcp'])
)

print(smb_fs)
print(smb_fs.listdir(conf['smb']['enter_path']))