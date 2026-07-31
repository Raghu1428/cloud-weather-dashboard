const API_KEY = "YOUR_OPENWEATHER_API_KEY"; // Replace with your OpenWeatherMap API key

async function getWeather() {
    const city = document.getElementById('cityInput').value.trim();
    const resultDiv = document.getElementById('weatherResult');
    
    if (!city) {
        alert("Please enter a city name.");
        return;
    }

    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${API_KEY}`;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error("City not found or invalid API key.");
        }
        const data = await response.json();

        document.getElementById('cityName').innerText = `${data.name}, ${data.sys.country}`;
        document.getElementById('temp').innerText = `Temperature: ${data.main.temp}°C`;
        document.getElementById('condition').innerText = `Condition: ${data.weather[0].description}`;
        document.getElementById('humidity').innerText = `Humidity: ${data.main.humidity}%`;

        resultDiv.classList.remove('hidden');
    } catch (error) {
        alert(error.message);
        resultDiv.classList.add('hidden');
    }
}