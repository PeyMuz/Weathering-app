import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter a city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_Label = QLabel(self)

        self.emoji_Label = QLabel(self)
        self.description_Label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_Label)
        vbox.addWidget(self.emoji_Label)
        vbox.addWidget(self.description_Label)


        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_Label.setAlignment(Qt.AlignCenter)
        self.emoji_Label.setAlignment(Qt.AlignCenter)
        self.description_Label.setAlignment(Qt.AlignCenter)
        
        # setObjectName() ginagamit mo para lagyan ng pangalan ang isang widget (gaya ng button) sa PyQt/PySide.          

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_Label.setObjectName("temperature_Label")
        self.emoji_Label.setObjectName("emoji_Label")
        self.description_Label.setObjectName("description_Label")




        self.setStyleSheet("""
    QLabel, QPushButton {
        font-family: Calibri;
    }
                       
    QLabel#city_label {  
        font-size: 40px;
        font-style: italic;
    } 

    QLineEdit#city_input {
        font-size: 40px;
    }

    QPushButton#get_weather_button {
       font-size: 30px;
       font-weight: bold;                       
    }              

    QLabel#temperature_Label {
       font-size: 75px;             
    }

    QLabel#emoji_Label {
        font-size: 100px;
        font-family: Segoe UI Emoji;    
    }

    QLabel#description_Label {
        font-size: 50px; 
        
    }
""")


    #Para gumana yung buttons

        self.get_weather_button.clicked.connect(self.get_weather)


#200 means OK, 404 means not found, 500 means server error, 403 means forbidden, 401 means unauthorized

    def get_weather(self):
        
        api_key = "5200fa1d65d1b9ca2bacee5a482bbf03"
        city = self.city_input.text().strip()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status() # Raises an HTTPError for bad responses (4xx and 5xx)
            data = response.json()

            print(data)

            if response.status_code == 200:
                self.display_weather(data)

        except requests.exceptions. HTTPError as e:
            status_code = e.response.status_code
            if status_code == 404:
                self.show_error("City not found!!")
            elif status_code == 401:
                self.show_error("Invalid API key!!")
            elif status_code == 403:
                self.show_error("Access forbidden!!")
            elif status_code == 500:
                self.show_error("Server error!!")
            elif status_code == 503:
                self.show_error("Sevice unavailable!!")
            elif status_code == 502:
                self.show_error("Bad gateway!!")
            elif status_code == 504:
                self.show_error("Gateway timeout!!")
            else:
                self.show_error("Please input a valid city name")
        
            
        except requests.exceptions.ConnectionError:
            self.show_error("Connection error\n Please try again later.")
        except requests.exceptions.Timeout:
            self.show_error("Request timed out\n Please try again later.")
        except requests.exceptions.TooManyRedirects:
            self.show_error("Too many redirects\n Please try again later.")
        except requests.exceptions.RequestException as e:
            self.show_error(f"Request Error: {e}\n Please try again later.")


    def show_error(self, message):
        self.temperature_Label.setStyleSheet("font-size: 30px; color: red;")
        self.temperature_Label.setText(message)
        self.emoji_Label.setText("")
        self.description_Label.clear()

    def display_weather(self, data):
        temp_kelvin = data["main"]["temp"]
        temp_celsius = temp_kelvin - 273.15  # Convert Kelvin to Celsius
        weather_id = data['weather'][0]['id']
        weather_description = data["weather"][0]["description"]

        print(f"Weather ID: {weather_id}, Description: {weather_description}") # Debugging: I-print ang weather_id

        self.temperature_Label.setStyleSheet("font-size: 75px; color: black;")
        self.emoji_Label.setText(self.get_emoji(weather_id, temp_celsius))  # Gamitin ang weather_id
        self.temperature_Label.setText(f"{temp_celsius:.0f}°C")
        self.description_Label.setText(weather_description.capitalize())


    def get_emoji(self, weather_id, temp_celsius):
        if temp_celsius <= 0:  # Kung malamig (0°C o mas mababa)
            return "❄️"  # Snow emoji
        if 200 <= weather_id < 232:
            return "⛈️"
        elif 300 <= weather_id < 321:
            return "🌦️"
        elif 500 <= weather_id < 531:
            return "🌧️"
        elif 600 <= weather_id < 622:
            return "❄️"
        elif 701 <= weather_id < 781:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id < 804:
            return "☁️"
        else:
            return "❓"
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())