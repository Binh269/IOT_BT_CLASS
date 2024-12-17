from flask import Flask, render_template
from sense_emu import SenseHat
import time
import threading
import templates

app = Flask(__name__)

sense = SenseHat()

temp_data = []
humidity_data = []

def update_data():
    while True:
        temperature = sense.get_temperature()
        humidity = sense.get_humidity()
        
        temp_data.append(temperature)
        humidity_data.append(humidity)
        
        if len(temp_data) > 20:
            temp_data.pop(0)
        if len(humidity_data) > 20:
            humidity_data.pop(0)
        
        time.sleep(2)

threading.Thread(target=update_data, daemon=True).start()

@app.route('/')
def index():
    temperature = temp_data[-1] if temp_data else 0
    humidity = humidity_data[-1] if humidity_data else 0
    return render_template('index.html', temperature=temperature, humidity=humidity)

if __name__ == '__main__':
    app.run(debug=True)
