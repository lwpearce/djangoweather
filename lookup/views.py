# This is my views.py file
from django.shortcuts import render
import logging

def getDescription():
    dummy = ''

# Create your views here.
def home(request):
    import json
    import requests

    colors_dict = {
        "Good":"good",
        "Moderate":"moderate",
        "Unhealthy for Sensitive Groups":"usg",
        "Unhealthy":"unhealthy",
        "Very Unhealthy":"veryUnhealthy",
        "Hazardous":"hazardous"
    }

    descriptions_dict = {
        "Good":"(0-50) Air quality is considered satisfactory, and air pollution poses little or no risk.",
        "Moderate":"(51-100) Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution.",
        "Unhealthy for Sensitive Groups":"(101-150) Although general public is not likely to be affected at thiis AQI range, people with lung disearse, older adults and children are at a greater risk.",
        "Unhealthy":"(151-200) Everyone may begin to experience health effects; members of sensitive groups may experiece more serious health effects.",
        "Very Unhealthy":"(201-300) Health alert: everyone may experience more serious health effects.",
        "Hazardous":"(301-500) Health warnings of emergency conditions. Teh entire population is more likely to be affected."
    }

    descriptions_params = {}
    colors_params = {}
    visibility_params = {}

    if request.method == "POST":        
        zipcode = request.POST['zipcode']
        api_request = requests.get("https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=" + zipcode + "&distance=0&API_KEY=BBA3C4F2-4A89-4443-889C-3C51EF3B3D29")
        try:
            api = json.loads(api_request.content)  # this loads and parses the content from the api_request variable and puts it in api variable
        except Exception as e:
            api = "Error..."
    else:
        api_request = requests.get("https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=23059&distance=0&API_KEY=BBA3C4F2-4A89-4443-889C-3C51EF3B3D29")
        
    try:
        api = json.loads(api_request.content)  # this loads and parses the content from the api_request variable and puts it in api variable
    except Exception as e:
        api = "Error..."
        
    descriptions_params["air_quality_description"] = descriptions_dict.get(api[0]['Category']['Name'])
    colors_params["air_quality_color"] = colors_dict.get(api[0]['Category']['Name'])

    if len(api) > 1:
        visibility_params["pm25_visibility"] = 'visible'
        descriptions_params["pm25_quality_description"] = descriptions_dict.get(api[1]['Category']['Name'])
        colors_params["pm25_quality_color"] = colors_dict.get(api[1]['Category']['Name'])

    if len(api) > 2:
        visibility_params["pm10_visibility"] = 'visible'
        descriptions_params["pm10_quality_description"] = descriptions_dict.get(api[2]['Category']['Name'])
        colors_params["pm10_quality_color"] = colors_dict.get(api[2]['Category']['Name'])

    return render(request, 'home.html', {
        'api': api, 
        'descriptions':descriptions_params,
        'visibilities':visibility_params,
            'colors':colors_params
    })

def about(request):
    return render(request, 'about.html', {})