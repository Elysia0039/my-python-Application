import requests
from tkinter import *
from tkinter import messagebox
import urllib.request
from bs4 import BeautifulSoup
import json

class DataProcessor:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path

    @property
    def read_data(self):
        # 读取数据并返回
        with open(self.data_file_path, 'r') as f:
            data = f.read()
        return data

    @staticmethod
    def write_to_file(data_file_path, message):
        with open(data_file_path, mode='w', encoding='utf-8') as f:
            f.write(message)

    @staticmethod
    def call_api(api_url, params):
        # 调用 API 并返回结果
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    @staticmethod
    def call_data(url='http://www.ustc.edu.cn/'):
        html = urllib.request.urlopen(url)
        bsObj = BeautifulSoup(html.read(), "html.parser")
        alphabet = bsObj.find(attrs={"class": 'news'})
        c = alphabet.find_all("a")
        g = []
        for i in c:
            g.append(i.text.strip())
        return [k + "\n" for k in g]

    def visualize_data(self, data):
        pass


class MyApplication(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        def QueryWindow():
            # 显示一个警告信息，点击确后，销毁窗口
            if messagebox.showwarning("warning", "You have QUITED the Application"):
                self.master.destroy()

        self.master = master
        self.pack()
        self.master.geometry("500x500")
        self.create_widgets()
        self.master.title("12321")
        self.master.relief = RAISED
        self.master["background"] = "#C9C9C9"
        self.master.protocol('WM_DELETE_WINDOW', QueryWindow)

    def create_widgets(self):
        self.hello_label = Label(self, text="Welcome to use my Application!", bg="yellow", fg="red", font=('Times', 20, 'bold italic'))
        self.hello_label.pack(side="top")
        self.quit_button = Button(self, text="Quit", command=self.master.destroy)
        self.quit_button.pack(side="bottom")
        self.open_window_button = Button(self, text="use chatGPT", command=self.GPT_window)
        self.open_window_button.pack(side="bottom")

    def add_text(self, text):
        self.massage_label = Label(self, text=text)
        self.massage_label.pack(side="top")

    def GPT_window(self):
        # 创建新窗口
        def generate_ai_response(user_input):
            url = "https://v1.apigpt.cn/"
            text = str(user_input)
            payload = {"q": text, "apitype": "sql"}

            response = requests.get(url, params=payload)

            response_dict = json.loads(response.text)
            question = response_dict["Questions"]
            answer = response_dict["ChatGPT_Answer"]
            return answer

        def handle_send_button_click():
            user_input = input_box.get("1.0", "end-1c")
            output_box.insert(END, "user:" + user_input + "\n")
            ai_response = generate_ai_response(user_input)
            output_box.insert(END, "AI: " + ai_response + "\n" * 3)
            input_box.delete("1.0", END)

        new_windom1 = Tk()
        new_windom1 .title("GPT AI")
        new_windom1 .geometry("1100x900")  # 窗口大小为600x800像素
        # 标签示例，用于显示欢迎消息和聊天记录
        welcome_label = Label(new_windom1, text="欢迎使用ChatGPT！", font=("Arial", 16))
        welcome_label.pack(side="top")
        send_button = Button(new_windom1, text="发送", command=handle_send_button_click)
        send_button.pack(side="bottom")
        # 文本框示例，用于输入用户问题
        input_box = Text(new_windom1, height=4, width=150)
        input_box.pack(side="bottom")
        output_box = Text(new_windom1, height=50, width=150)
        output_box.pack(side="top")
        assest_label = Label(new_windom1, text="请在这里提出问题", font=("Arial", 16))
        assest_label.pack(side="left")
