import sys 
import requests
from PyQt5.QtWidgets import( QApplication, QWidget, QLabel, QLineEdit, QPushButton , QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from openai import OpenAI
class weatherapp(QWidget):
    def __init__(self,):
        super().__init__()
        self.city_label = QLabel('Enter the city name: ',self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton('Get Weather',self)
        self.history_button = QPushButton("Show History", self)
        self.ai_button = QPushButton('Suggestion', self)
        self.temperature = QLabel( self)
        self.humidity = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(  self)
        self.iniUI()
        

         
    def iniUI(self):    
        self.setWindowTitle('Weather App')
        

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.humidity)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.history_button)
        vbox.addWidget(self.ai_button)
        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.humidity.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)


        self.city_label.setObjectName('city_label')
        self.city_input.setObjectName('city_input')
        self.temperature.setObjectName('temperature')
        self.humidity.setObjectName('humidity')
        self.emoji_label.setObjectName('emoji_label')
        self.description_label.setObjectName('description_label')
        self.get_weather_button.setObjectName('get_weather_button')
        self.ai_button.setObjectName('ai_button')
        
        self.setStyleSheet("""
            QLabel, QPushButton { 
                font-family: calibri; 
            }       
            QLabel#city_label {
                font-size: 25px; 
                font-style: italic;           
            }
            QLineEdit#city_input {
                font-size: 20px;
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
            QPushButton#get_weather_button {
                font-size: 20px;  
                font-weight: bold;
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton#get_weather_button:hover {
                background-color: #45a049;
            }
            QLabel#temperature {
                font-size: 75px;           
            }
            QLabel#humidity{
                font-size: 25px
                           }
            QLabel#emoji_label {
                font-size: 60px;
                font-family: Segoe UI emoji
            }
            QLabel#description_label {
                font-size: 30px;
            }
            QPushButton#ai_button {
                font-size : 20px ;
                font-weight: bold
                padding: 10px; 
                
                           
                           }
            
        """)

        self.get_weather_button.clicked.connect(self.get_weather)
        self.history_button.clicked.connect(self.show_history)
        self.ai_button.clicked.connect(self.handle_ai_request)
        

    def get_weather(self):
        API_key = 'YOUR_API_HERE'
        city = self.city_input.text()
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}'
    
    
        try:
            response = requests.get(url)
            response.raise_for_status( )
            data = response.json()

            if data['cod'] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error('bad request:\nPlease check your input ')
                case 401:
                    self.display_error('unauthorize:\nInvalid Api key ')
                case 403:
                    self.display_error('forbidden:\nAccess is denied')
                case 404:
                    self.display_error('not found:\nCity not found ')
                case 500:
                    self.display_error('internal server error:\nPlease try again later')
                case 502:
                    self.display_error('bad gateway:\nInvalid response from the server')
                case 503:
                    self.display_error('service unavaiable:\nServer is down')
                case 504:
                    self.display_error('gateway timeout:\nNo response from server')
                case _:
                    self.display_error(f'Http error occured:\n{http_error}')

        

        except requests.exceptions.ConnectionError:
            self.display_error('conection error:\n check your connection')
        except requests.exceptions.Timeout:
            self.display_error('timeout error:\n The request timed out')
        except requests.exceptions.TooManyRedirects:
            self.display_error('too many redirects:\n check the url ')
        except requests.exceptions.RequestException as req_error:
            self.display_error(f'request error: \n{req_error}')         


    def display_error(self, message):
        self.humidity.setStyleSheet('font-size: 30px;')
        self.temperature.setStyleSheet('font-size: 30px;')
        self.temperature.setText(message) 
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        humidity = data['main']['humidity']
        temperature_k = data['main']['temp']
        temperature_c = temperature_k - 273.15
        weather_description  = data['weather'][0]['description']
        weather_id = data['weather'][0]['id']

        self.humidity.setText(f'humidity: {humidity}%')
        self.temperature.setText(f'{temperature_c:.0f}°C ')
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)
        
        self.save_history(
            self.city_input.text(),
            f'{temperature_c:.0f}°C',
            weather_description,
            f'{humidity}%'
        )
        
   
    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return '⛈️'
        elif 300 <= weather_id <= 321: 
            return '🌦️'
        elif 500 <= weather_id <= 521:
            return '🌧️'
        elif 600 <= weather_id <= 622:
            return '☃️'
        elif 701 <= weather_id <= 741:
            return '😶‍🌫️'
        elif weather_id == 762: 
            return '🌋'
        elif weather_id == 771:
            return '🍃'
        elif weather_id == 781:
            return '🌪️'
        elif weather_id == 800:
            return '☀️'
        elif 801 <= weather_id <= 804:
            return '☁️'
        else:
            return ''

    def save_history(self, city, temperature, description, humidity):
        with open("C:\\Users\\Viet\\OneDrive\\Máy tính\\python\\weather_history.txt", "a", encoding='utf-8') as f : 
            f.write(f'{city} - {temperature} - {description}-{humidity}\n')    
            f.close()
    


    def show_history(self):
        try: 
            with open("C:\\Users\\Viet\\OneDrive\\Máy tính\\python\\weather_history.txt", 'r' , encoding = 'utf-8') as f: 
                history = f.read()
                f.close()

        except FileNotFoundError:
            history = 'No history available'
        
        msg = QMessageBox(self)
        msg.setWindowTitle('weather history')
        msg.setText(history)
        font = msg.font()
        font.setPointSize(16)
        msg.setFont(font)
        msg.exec_()

    def handle_ai_request(self):
        city = self.city_input.text()
        temp = self.temperature.text()
        desc = self.description_label.text()
        hum = self.humidity.text()


        if not city or not temp or not desc : 
            self.show_ai_message('Bạn phải tra thời tiết trước khi hỏi AI!')
            return
        
        ai_text = self.ask_ai(city, temp, desc)
        self.show_ai_message(ai_text)
    
    def ask_ai(self, city, temp, desc):
        try:
            client = OpenAI(api_key="your_ai_api_here")

            prompt = f"""
            Bạn là trợ lý thời tiết. Hãy đưa ra lời nhận xét thân thiện , ngắn gọn về thời tiết:
             thành phố : {city}
             nhiệt độ : {temp}
             thời tiết : {desc}
            Hãy đưa ra lời khuyên phù hợp
            """
            response = client.responses.create(
                model= 'gpt-4.1-mini',
                input= prompt
            )

            return response.output_text

        except Exception as e:
            return f"AI error: {e}"
    def show_ai_message(self, text):
        msg = QMessageBox(self)
        msg.setWindowTitle("AI Weather Assistant")
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)

        font = msg.font()
        font.setPointSize(16)
        msg.setFont(font)

        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()



if __name__ == '__main__' :
    app = QApplication(sys.argv)
    weather_app = weatherapp()
    weather_app.show()
    sys.exit(app.exec_())