# README.md content as a string variable
readme_content = '''# Weather Application

A modern, responsive weather application built with Flask backend and OpenWeatherMap API. Features real-time weather data with clean UI.

## Features
- Search weather by city name
- Display current temperature, humidity, and wind speed
- Clean, modern user interface
- Responsive design for mobile and desktop
- Error handling for invalid cities

## Prerequisites
- Python 3.7+
- OpenWeatherMap API key (free tier available)

## Installation

### 1. Clone the repository
git clone <repository-url>
cd weather-app

### 2. Create virtual environment
python -m venv venv

### 3. Activate virtual environment
- **Windows:**
    venv\\Scripts\\activate
  - **macOS/Linux:**
    source venv/bin/activate
  
### 4. Install dependencies
pip install -r requirements.txt

### 5. Get OpenWeatherMap API Key
1. Go to [OpenWeatherMap](https://openweathermap.org/)
2. Sign up for a free account
3. Navigate to [API Keys](https://home.openweathermap.org/api_keys)
4. Generate a new API key

### 6. Configure API Key
Create a `.env` file in the project root:
OPENWEATHER_API_KEY=your_api_key_here

## Project Structure
weather-app/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── static/
│   └── style.css      # CSS styles
└── templates/
    └── index.html     # Main HTML template

## Running the Application

### Development Mode
python app.py
The application will be available at `http://localhost:5000`

### Production Deployment
For production, use a WSGI server like Gunicorn:
pip install gunicorn
gunicorn app:app

## Usage
1. Open your browser and navigate to `http://localhost:5000`
2. Enter a city name in the search box
3. Click "Get Weather" or