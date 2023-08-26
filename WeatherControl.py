import json
import tkinter as tk
from tkinter import ttk

class WeatherControlPanel:
    def __init__(self, root, weather_data):
        self.root = root
        self.weather_data = weather_data

    def clear_labels(self):
        pass  # To be implemented in child classes

def read_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def main():
    from TemperatureControlPanel import TemperatureControlPanel  # Move the import here

    weather_data = read_json_file('sorted_weather_data.json')
    root = tk.Tk()
    root.title("Weather Finder")

    temp_panel = TemperatureControlPanel(root, weather_data)
    # ... (initialize other panels)

    root.mainloop()

if __name__ == "__main__":
    main()
