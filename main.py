# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。


from utils import *

# 创建Tk对象
root = Tk()

# 创建应用程序对象
app = MyApplication(master=root)
app.add_text("this is my application")

# 进入主循环
app.mainloop()
