import time
import fs.zipfs as zipfs
import fs.mountfs as mountfs
from  fs.expose import dokan

a = zipfs.ZipFS("PanDownload_v2.1.2.zip")

print(a.listdir("PanDownload"))

b = mountfs.MountFS()
b.mount("g:", a)

time.sleep(10)