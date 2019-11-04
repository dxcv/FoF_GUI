from WindPy import *

w.start(); # 命令超时时间为120秒
# w.start(waitTime=60); # 命令超时时间设置成60秒
#
# w.stop()  # 当需要停止WindPy时，可以使用该命令
#           注： w.start不重复启动，若需要改变参数，如超时时间，用户可以使用w.stop命令先停止后再启动。
#           退出时，会自动执行w.stop()，一般用户并不需要执行w.stop
#
# w.isconnected() # 即判断WindPy是否已经登录成功

df = w.edb("M5541321", "2000-01-01", "2019-11-04","Fill=Previous")