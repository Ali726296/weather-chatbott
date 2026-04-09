from flask import Flask, render_template, request, jsonify
import requests
import re

app = Flask(__name__)

# 🔑 Your API Key
API_KEY = "222fde65635607c4877715a0c6cc625c"

# 🤖 Smart reply generator
def generate_reply(city, temp, desc):
    if temp > 35:
        advice = "🔥 It's very hot! Stay hydrated."
    elif temp < 15:
        advice = "🧥 It's cold, wear warm clothes."
    elif "rain" in desc.lower():
        advice = "☔ Carry an umbrella!"
    elif "cloud" in desc.lower():
        advice = "☁️ It’s cloudy, weather is calm."
    else:
        advice = "🌤️ Weather looks pleasant!"

    return f"""
    🌍 City: {city}<br>
    🌡️ Temperature: {temp}°C<br>
    🌥️ Condition: {desc}<br><br>
    👉 {advice}
    """

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_weather", methods=["POST"])
def get_weather():
    data = request.get_json()
    user_input = data.get("message", "")

    # ✅ FIXED CITY EXTRACTION
    user_input = user_input.lower()
    city = re.sub(r"weather in", "", user_input).strip()

    print("City sent to API:", city)  # debug

    # 🌐 API Call
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()

    # ❌ Error handling
    if response.get("cod") != 200:
        return jsonify({"reply": "❌ City not found. Try again!"})

    temp = response["main"]["temp"]
    desc = response["weather"][0]["description"]

    reply = generate_reply(city, temp, desc)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)