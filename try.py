# from file_io_emulation.Server import Server as FS_server
# import fs
# from fs.smbfs import smbfs
# import configparser

# conf = configparser.ConfigParser()
# conf.read('setting.ini', encoding="utf8")
    
# smb_fs = smbfs.SMBFS(
#     conf['smb']['ip'],
#     username = conf['smb']['username'],
#     passwd = conf['smb']['passwd'],
#     timeout = 5,
#     port = int(conf['smb']['port']),
#     direct_tcp = int(conf['smb']['direct_tcp'])
# )
# smb_fs = smb_fs.opendir(conf['smb']['enter_path'])
# smb_fs.tree()
# # print(smb_fs)
# print(smb_fs.listdir('/'))

# for walk_path in smb_fs.walk.dirs(conf['smb']['enter_path'], max_depth = 1):
#     print(walk_path)