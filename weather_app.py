from tkinter import *  # Import all classes/functions from the tkinter module
from tkinter import messagebox  # Import the messagebox module from tkinter
import requests  # Import the requests module for making HTTP requests
from configparser import ConfigParser  # Import ConfigParser from configparser for reading config files

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'  # Define the API URL for weather data

config_file = 'config.ini'  # Define the name of the config file
config = ConfigParser()  # Create an instance of ConfigParser
config.read(config_file)  # Read the configuration file
api_key = config['api_key']['key']  # Get the API key from the config file

# Function to retrieve weather data for a given city
def get_weather(city):
    result = requests.get(url.format(city, api_key))  # Make a GET request to the weather API
    if result:  # Check if the request was successful
        json = result.json()  # Parse the JSON response
        # Extract relevant weather information from the JSON data
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_fahrenheit = (temp_kelvin - 273.15) * 9/5 + 32
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        final = (city, country, temp_fahrenheit, icon, weather)  # Store the weather data in a tuple
        return final  # Return the weather data
    else:
        return None  # Return None if the request fails

# Function to perform a weather search based on user input
def search():
    city = city_text.get()  # Get the city entered in the Entry widget
    weather = get_weather(city)  # Get weather data for the entered city
    if weather:  # If weather data is available
        # Update the GUI elements with weather information
        location_lbl['text'] = '{},{}'.format(weather[0], weather[1])
        temp_lbl['text'] = '{:.2f}°F'.format(weather[2])
        image['bitmap'] = 'weather_icons/{}.png'.format(weather[3])
        weather_lbl['text'] = weather[4]
    else:
        messagebox.showerror('Error', 'Cannot find city ()'.format(city))  # Show an error message

app = Tk()  # Create the main application window
app.title('Weather App')  # Set the window title
app.geometry('700x350')  # Set the window size

city_text = StringVar()  # Create a StringVar to hold the text entered in the Entry widget
city_entry = Entry(app, textvariable=city_text)  # Create an Entry widget linked to city_text
city_entry.pack()  # Place the Entry widget in the window

search_btn = Button(app, text='Search',width=12, command=search)  # Create a Search button
search_btn.pack()  # Place the Search button in the window

location_lbl = Label(app, text='Location', font=('bold', 20))  # Create a Label for location
location_lbl.pack()  # Place the location Label in the window

image = Label(app, bitmap='')  # Create a Label for the weather image
image.pack()  # Place the image Label in the window

temp_lbl = Label(app, text='Temperature')  # Create a Label for temperature
temp_lbl.pack()  # Place the temperature Label in the window

weather_lbl = Label(app, text='Weather')  # Create a Label for weather
weather_lbl.pack()  # Place the weather Label in the window

app.mainloop()  # Start the main event loop for the application (GUI)

