import requests
from tkinter import *
from tkinter import messagebox
import urllib.request
from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk


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
        self.hello_label = Label(self, text="Welcome to use my Application!", bg="yellow", fg="red",
                                 font=('Times', 20, 'bold italic'))
        self.hello_label.pack(side="top")
        self.quit_button = Button(self, text="Quit", command=self.master.destroy)
        self.quit_button.pack(side='bottom')
        self.open_window_button = Button(self, text="use chatGPT", command=self.GPT_window)
        self.open_window_button.pack(side="bottom")
        self.open_window_button2 = Button(self, text="weather", command=self.weather_window)
        self.open_window_button2.pack(side='bottom')
        self.open_window_button3 = Button(self, text="province&city", command=self.province_window)
        self.open_window_button3.pack(side='bottom')
        self.open_window_button4 = Button(self, text='scientist\'s passage', command=self.cel_window)
        self.open_window_button4.pack(side='bottom')
        self.open_window_button5 = Button(self, text='date of history', command=self.history_window)
        self.open_window_button5.pack(side='bottom')

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
        new_windom1.title("GPT AI")
        new_windom1.geometry("1100x900")  # the size of window is 600x800
        # a label to show welcome
        welcome_label = Label(new_windom1, text="欢迎使用ChatGPT！", font=("Arial", 16))
        welcome_label.pack(side="top")
        send_button = Button(new_windom1, text="发送", command=handle_send_button_click)
        send_button.pack(side="bottom")
        # a textbox to let user input questions
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
            plt.legend()
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

    def province_window(self):
        def get_information():
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/58.0.3029.110 Safari/537.3',
                'Referer': 'https://www.google.com/',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.8',
            }
            city = input_box.get("1.0", "end-1c")
            url = 'https://www.mca.gov.cn/article/sj/xzqh/2020/20201201.html'
            html = urllib.request.urlopen(url)
            bsObj = BeautifulSoup(html.read(), "html.parser")
            alphabet = bsObj.find_all("td")
            id = ""
            for i in alphabet:
                if i.text.strip() == city + '省':
                    print(i.text.strip(), "'s ID is", id)
                    break
                else:
                    id = i.text.strip()
            output_box.insert(END, "你所查询的区域为：%s\n其区域id是：%s\n" % (city, id))
            url = 'https://apis.juhe.cn/fapigw/globalarea/areas'
            playload = {"province": city, "key": "8405fcc8fb49a699427de721bc8c81e1"}
            response = requests.get(url, params=playload)

            response_dict = json.loads(response.text)
            return response_dict

        def handle_send_button_click():
            response = get_information()
            output_box.insert(END, f"country{response['result'][0]['country']}\n")
            output_box.insert(END, f"province{response['result'][0]['province']}\n")
            output_box.insert(END, 'city:')
            for i in response['result']:
                output_box.insert(END, i['city'] + ',')

        new_windom = Tk()
        new_windom.title("search for province")
        new_windom.geometry("800x500")  # 窗口大小为600x800像素
        welcome_label = Label(new_windom, text="欢迎使用行政区划查询！", font=("Arial", 16))
        welcome_label.pack(side="top")
        send_button = Button(new_windom, text="查询", command=handle_send_button_click)
        send_button.pack(side="bottom")
        input_box = Text(new_windom, height=1, width=150)
        input_box.pack(side="bottom")
        read_label = Label(new_windom, text="请输入省份完整名称！", font=("Arial", 16))
        read_label.pack(side="bottom")
        output_box = Text(new_windom, height=20, width=100, font=("宋体", 12))
        output_box.pack(side="top")

    def cel_window(self):
        def get_url():
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/58.0.3029.110 Safari/537.3',
                'Referer': 'https://www.google.com/',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.8',
            }
            person = input_box.get("1.0", "end-1c")
            person = person.replace(' ', '%20')
            url = 'https://dblp.org/search?q='+person
            html = urllib.request.urlopen(url)
            bsObj = BeautifulSoup(html.read(), "html.parser")
            alphabet = bsObj.find(attrs={"class": 'result-list'})
            nn = alphabet.find("a")
            print(nn.attrs['href'])
            url = nn.attrs['href']
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            output_box.insert(END, f'{person}的所有文章的题目如下:\n')
            output_box.insert(END, '可以前往:' + url + '查看\n')

            titles = soup.find_all(class_='title')
            for title in titles:
                output_box.insert(END, title.text.strip() + '\n')

        new_windom = Tk()
        new_windom.title("search for scientist")
        new_windom.geometry("900x800")
        welcome_label = Label(new_windom, text="欢迎科学家查询！", font=("Arial", 16))
        welcome_label.pack(side="top")
        send_button = Button(new_windom, text="查询", command=get_url)
        send_button.pack(side="bottom")
        input_box = Text(new_windom, height=1, width=150)
        input_box.pack(side="bottom")
        read_label = Label(new_windom, text="科学家名称！", font=("Arial", 16))
        read_label.pack(side="bottom")
        output_box = Text(new_windom, height=40, width=100, font=("宋体", 12))
        output_box.pack(side="top")

    def history_window(self):

        new_windoms = Tk()
        new_windoms.geometry("400x300")
        new_windoms.title("search for the date in history")
        welcome_label = Label(new_windoms, text="查询历史上的这一天发生了什么大事", font=("Arial", 16))
        welcome_label.pack(side="top")
        mouth_var = StringVar()
        mouth_choices = [str(year) for year in range(1, 13)]
        mouth_dropdown = ttk.Combobox(new_windoms, textvariable=mouth_var, values=mouth_choices)
        date_var = StringVar()
        date_choices = [str(year) for year in range(1, 32)]
        day_dropdown = ttk.Combobox(new_windoms, textvariable=date_var, values=date_choices)
        mouth_dropdown.pack(pady=10)
        mouth_label = Label(new_windoms, text='月', font=("Arial", 14))
        mouth_label.pack(padx=10)
        day_dropdown.pack(pady=10)
        day_label = Label(new_windoms, text='日', font=("Arial", 14))
        day_label.pack(padx=10)

        def submit():
            m = mouth_dropdown.get()
            d = day_dropdown.get()
            print(m, d)
            result = m + '/' + d
            print(result)
            url = 'http://v.juhe.cn/todayOnhistory/queryEvent.php'
            playload = {'key': '4e672e3a35f5dd2eeb9f7877451a62ad', 'date': result}
            response = requests.get(url, params=playload)
            response_dict = json.loads(response.text)
            print(response_dict)
            # Create a Tkinter window
            root = Tk()
            root.title("things happened on "+result)
            # Define columns for the table
            columns = ('date', 'happening', 'e_id')
            tree = ttk.Treeview(root, columns=columns, show='headings')
            # Define column headings
            tree.heading('date', text='date')
            tree.heading('happening', text='happening')
            tree.heading('e_id', text='e_id')
            for i in response_dict['result']:
                tree.insert('', '0', values=(i['date'], i['title'], i['e_id']))
                print(i)
            tree.pack()

        button = Button(new_windoms, text="Submit", command=submit)
        button.pack(pady=10)
