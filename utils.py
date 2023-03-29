import requests
from tkinter import *
from tkinter import messagebox
import urllib.request
from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        self.master.title("myapplication")
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
        self.open_window_button2 = Button(self,text="weather",command=self.weather_window)
        self.open_window_button2.pack(side='bottom')

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
    def weather_window(self):
        # 创建 tkinter 窗口
        temperature_min = []
        temperature_max = []
        days = []
        header = "application/x-www-form-urlencoded"

        def generate_ai_response(user_input):
            # return {'reason': '查询成功!', 'result': {'city': '深圳', 'realtime': {'temperature': '21', 'humidity': '75', 'info': '多云', 'wid': '01', 'direct': '北风', 'power': '2级', 'aqi': '28'}, 'future': [{'date': '2023-03-29', 'temperature': '18/21℃', 'weather': '阵雨', 'wid': {'day': '03', 'night': '03'}, 'direct': '东风'}, {'date': '2023-03-30', 'temperature': '20/23℃', 'weather': '阵雨', 'wid': {'day': '03', 'night': '03'}, 'direct': '持续无风向'}, {'date': '2023-03-31', 'temperature': '21/24℃', 'weather': '阵雨', 'wid': {'day': '03', 'night': '03'}, 'direct': '持续无风向'}, {'date': '2023-04-01', 'temperature': '22/25℃', 'weather': '多云', 'wid': {'day': '01', 'night': '01'}, 'direct': '持续无风向'}, {'date': '2023-04-02', 'temperature': '22/27℃', 'weather': '多云', 'wid': {'day': '01', 'night': '01'}, 'direct': '持续无风向'}]}, 'error_code': 0}
            playload = {"city": user_input, "key": "fcf4300caa7b5661d26de55c25eb8195"}
            response = requests.get("http://apis.juhe.cn/simpleWeather/query", params=playload)
            data = json.loads(response.text)
            print(data)
            return data

        def handle_send_button_click():
            user_input = input_box.get("1.0", "end-1c")
            print(user_input)
            data = generate_ai_response(user_input)["result"]
            weather_now = data["realtime"]
            weather_future = data["future"]
            days.append("today")
            temperature_min.append(int(weather_now["temperature"]))
            temperature_max.append(int(weather_now["temperature"]))
            for i in weather_future:
                days.append(i["date"])
                te = i["temperature"]
                temp = te.split("/")
                print(temp)
                temp2 = temp[1].split('℃')
                num1 = int(temp[0])
                num2 = int(temp2[0])
                temperature_min.append(num1)
                temperature_max.append(num2)
            y_values = [d for d in temperature_max]
            y2_values = [d for d in temperature_min]

            # 使用 matplotlib 将数据绘制成函数图像
            canvas_frame = Frame(weather_window, width=20, height=20)
            canvas_frame.pack(side=TOP, fill=BOTH, expand=True)
            fig = plt.figure(figsize=(2, 3), dpi=100)
            plt.plot(days, y_values, label="Highest Temperatures", color='red')
            plt.plot(days, y2_values, label="Lowest Temperatures", color='blue')
            plt.xlabel("X")
            plt.ylabel("Y")
            plt.title("temperaturn today and future")

            # 在 tkinter 窗口中展示图像
            canvas = FigureCanvasTkAgg(fig, canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH)

            input_box.delete("1.0", END)
            output_box = Text(weather_window, height=20, width=150)
            output_box.pack(side="top")
            humidity = data['realtime']['humidity']
            info = data['realtime']['info']
            wid = data['realtime']['wid']
            direct = data['realtime']['direct']
            power = data['realtime']['power']
            aqi = data['realtime']['aqi']
            output_box.insert(END,
                              "城市名称:%s\n今日天气：\n温度：%d\n湿度：%s\n天气：%s\n天气标识：%s\n风向：%s\n风力：%s\n空气质量：%s\n" % (
                                  data['city'], temperature_min[0], humidity, info, wid, direct, power, aqi))
            output_box.insert(END, "未来天气温度(℃):\n")
            for i in range(1, 6):
                output_box.insert(END, days[i] + ":" + str(temperature_min[i]) + "/" + str(temperature_max[i]) + "   ")
            temperature_min.clear()
            temperature_max.clear()
            days.clear()

        weather_window = Tk()
        weather_window.title("weather")
        welcome_label = Label(weather_window, text="欢迎使用天气查询！", font=("Arial", 16))
        welcome_label.pack(side="top")
        send_button = Button(weather_window, text="查询", command=handle_send_button_click)
        send_button.pack(side="bottom")
        input_box = Text(weather_window, height=1, width=150)
        input_box.pack(side="bottom")
        weather_window.mainloop()

