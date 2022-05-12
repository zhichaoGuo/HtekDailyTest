# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import time
from time import sleep

from HtekLib.TestUtils import hl_request


def print_hi(name):
    for i in range(60):
        sleep(5)
        r = hl_request('GET','http://10.20.0.22/index.htm',auth=('admin','admin'),timeout=15)
        print(str(i) +'  '+r.text[:95])


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print(int(time.time()))

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
