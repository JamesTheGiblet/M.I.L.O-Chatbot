import requests

def extract_city_from_input(user_input):
    # Simple city extraction (you might need to improve this)
    if "in" in user_input:
        city = user_input.split("in")[-1].strip()
        return city
    return None

def get_weather(city):
    api_key = ""  # Replace with your actual API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city}"
    response = requests.get(complete_url)

    print(response.status_code) 

    if response.status_code == 200:
        data = response.json()
        main = data['main']
        temperature = round(main['temp'] - 273.15, 2)
        description = data['weather'][0]['description']
        return {
            "temperature": temperature,
            "description": description
        }
    else:
        return None
