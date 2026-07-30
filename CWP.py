import os

# Define the project directory
project_name = "Cloud-Weather-Dashboard"
templates_dir = os.path.join(project_name, "templates")

# Create directories
os.makedirs(templates_dir, exist_ok=True)

# Define file contents
app_py = """import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv('WEATHER_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    city = data.get('city')

    if not city:
        return jsonify({'error': 'City name is required'}), 400

    try:
        params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
        response = requests.get(BASE_URL, params=params)
        weather_data = response.json()

        if response.status_code == 200:
            result = {
                'city': weather_data['name'],
                'temperature': weather_data['main']['temp'],
                'description': weather_data['weather'][0]['description'].capitalize(),
                'humidity': weather_data['main']['humidity'],
                'wind_speed': weather_data['wind']['speed']
            }
            return jsonify(result), 200
        else:
            return jsonify({'error': weather_data.get('message', 'Failed to fetch weather data')}), response.status_code

    except Exception as e:
        return jsonify({'error': f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
"""

index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloud Weather Dashboard</title>
    <style>
        body { font-family: sans-serif; background: #f8fafc; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 350px; text-align: center; }
        input { padding: 0.5rem; width: 60%; border: 1px solid #ccc; border-radius: 4px; }
        button { padding: 0.5rem; background: #2563eb; color: white; border: none; border-radius: 4px; cursor: pointer; }
        #result { display: none; margin-top: 1rem; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Weather Dashboard</h2>
        <input type="text" id="city" placeholder="Enter city...">
        <button onclick="getWeather()">Search</button>
        <p id="error" style="color: red; display: none;"></p>
        <div id="result">
            <h3 id="name"></h3>
            <p id="desc"></p>
            <h1 id="temp"></h1>
            <p>Humidity: <span id="hum"></span>% | Wind: <span id="wind"></span>m/s</p>
        </div>
    </div>
    <script>
        async function getWeather() {
            const city = document.getElementById('city').value;
            const resDiv = document.getElementById('result');
            const errDiv = document.getElementById('error');
            resDiv.style.display = 'none'; errDiv.style.display = 'none';
            
            if(!city) return;
            
            const response = await fetch('/api/weather', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ city })
            });
            const data = await response.json();
            
            if(response.ok) {
                document.getElementById('name').textContent = data.city;
                document.getElementById('desc').textContent = data.description;
                document.getElementById('temp').textContent = Math.round(data.temperature) + '°C';
                document.getElementById('hum').textContent = data.humidity;
                document.getElementById('wind').textContent = data.wind_speed;
                resDiv.style.display = 'block';
            } else {
                errDiv.textContent = data.error;
                errDiv.style.display = 'block';
            }
        }
    </script>
</body>
</html>
"""

requirements_txt = "Flask==3.0.0\nrequests==2.31.0\npython-dotenv==1.0.0\n"
env_file = "WEATHER_API_KEY=insert_your_actual_openweathermap_api_key_here\n"

# Write files
files_to_create = {
    "app.py": app_py,
    "requirements.txt": requirements_txt,
    ".env": env_file,
    "templates/index.html": index_html
}

for filename, content in files_to_create.items():
    filepath = os.path.join(project_name, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print(f"✅ Success! Your project has been generated in the '{project_name}' folder.")
print("Next steps:")
print(f"1. cd {project_name}")
print("2. pip install -r requirements.txt")
print("3. python app.py")