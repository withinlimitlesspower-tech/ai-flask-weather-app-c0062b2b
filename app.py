import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city_name):
    """Fetch weather data from OpenWeatherMap API"""
    if not API_KEY:
        return {"error": "API key not configured"}
    
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric'  # For Celsius, use 'imperial' for Fahrenheit
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch weather data: {str(e)}"}

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def get_weather():
    """API endpoint to get weather data"""
    city = request.args.get('city')
    
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
    
    weather_data = get_weather_data(city)
    
    if 'error' in weather_data:
        return jsonify(weather_data), 500
    
    # Extract relevant data
    if weather_data.get('cod') != 200:
        return jsonify({"error": "City not found"}), 404
    
    processed_data = {
        'city': weather_data['name'],
        'country': weather_data['sys']['country'],
        'temperature': round(weather_data['main']['temp'], 1),
        'feels_like': round(weather_data['main']['feels_like'], 1),
        'humidity': weather_data['main']['humidity'],
        'pressure': weather_data['main']['pressure'],
        'wind_speed': round(weather_data['wind']['speed'] * 3.6, 1),  # Convert m/s to km/h
        'wind_direction': weather_data['wind'].get('deg', 0),
        'description': weather_data['weather'][0]['description'].title(),
        'icon': weather_data['weather'][0]['icon'],
        'visibility': weather_data.get('visibility', 0) / 1000  # Convert to km
    }
    
    return jsonify(processed_data)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather App</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
            width: 100%;
            max-width: 500px;
            padding: 40px;
            backdrop-filter: blur(10px);
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header h1 {
            color: #333;
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header p {
            color: #666;
            font-size: 1.1rem;
        }

        .search-box {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }

        .search-input {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s ease;
            outline: none;
        }

        .search-input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .search-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0 25px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 600;
            transition: transform 0.2s ease;
        }

        .search-btn:hover {
            transform: translateY(-2px);
        }

        .search-btn:active {
            transform: translateY(0);
        }

        .weather-card {
            background: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            display: none;
        }

        .weather-card.active {
            display: block;
            animation: fadeIn 0.5s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .location {
            text-align: center;
            margin-bottom: 20px;
        }

        .location h2 {
            color: #333;
            font-size: 2rem;
            margin-bottom: 5px;
        }

        .location .country {
            color: #666;
            font-size: 1.2rem;
        }

        .weather-main {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
        }

        .temperature {
            font-size: 4rem;
            font-weight: 300;
            color: #333;
            line-height: 1;
        }

        .temperature span {
            font-size: 2rem;
            vertical-align: top;
        }

        .weather-icon {
            width: 100px;
            height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .weather-icon img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }

        .description {
            text-align: center;
            color: #666;
            font-size: 1.3rem;
            margin-bottom: 30px;
            text-transform: capitalize;
        }

        .weather-details {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }

        .detail-item {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .detail-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.2rem;
        }

        .detail-info h3 {
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .detail-info p {
            color: #333;
            font-size: 1.4rem;
            font-weight: 600;
        }

        .error-message {
            background: #fee;
            border: 1px solid #fcc;
            color: #c33;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            margin-top: 20px;
            display: none;
        }

        .error-message.active {
            display: block;
            animation: shake 0.5s ease;
        }

        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }

        .loading {
            text-align: center;
            padding: 20px;
            display: none;
        }

        .loading.active {
            display: block;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .footer {
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 0.9rem;
        }

        @media (max-width: 600px) {
            .container {
                padding: 20px;
            }
            
            .weather-details {
                grid-template-columns: 1fr;
            }
            
            .temperature {
                font-size: 3rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-cloud-sun"></i> Weather App</h1>
            <p>Get real-time weather information for any city</p>
        </div>

        <div class="search-box">
            <input type="text" class="search-input" id="cityInput" placeholder="Enter city name..." autocomplete="off">
            <button class="search-btn" id="searchBtn">
                <i class="fas fa-search"></i> Search
            </button>
        </div>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Fetching weather data...</p>
        </div>

        <div class="error-message" id="errorMessage"></div>

        <div class="weather-card" id="weatherCard">
            <div class="location">
                <h2 id="cityName">-</h2>
                <div class="country" id="country">-</div>
            </div>

            <div class="weather-main">
                <div class="temperature">
                    <span id="temperature">-</span><span>°C</span>
                </div>
                <div class="weather-icon">
                    <img id="weatherIcon" src="" alt="Weather Icon">
                </div>
            </div>

            <div class="description" id="weatherDescription">-</div>

            <div class="weather-details">
                <div class="detail-item">
                    <div class="detail-icon">
                        <i class="fas fa-temperature-low"></i>
                    </div>
                    <div class="detail-info">
                        <h3>Feels Like</h3>
                        <p id="feelsLike">-°C</p>
                    </div>
                </div>

                <div class="detail-item">
                    <div class="detail-icon">
                        <i class="fas fa-tint"></i>
                    </div>
                    <div class="detail-info">
                        <h3>Humidity</h3>
                        <p id="humidity">-%</p>
                    </div>
                </div>

                <div class="detail-item">
                    <div class="detail-icon">
                        <i class="fas fa-wind"></i>
                    </div>
                    <div class="detail-info">
                        <h3>Wind Speed</h3>
                        <p id="windSpeed">- km/h</p>
                    </div>
                </div>

                <div class="detail-item">
                    <div class="detail-icon">
                        <i class="fas fa-compress-alt"></i>
                    </div>
                    <div class="detail-info">
                        <h3>Pressure</h3>
                        <p id="pressure">- hPa</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="footer">
            <p>Powered by OpenWeatherMap API</p>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function()