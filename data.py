# Imports
import os
import csv
import random

import datetime
import numpy as np
import torch
import matplotlib.pyplot as plt

# Traffic count limit for traffic density
count_limit = 150
# Traffic speed limit for traffic density
speed_limit = 50

# Traffic data of a location
class TrafficData:
    """
    A class to represent the traffic data of a location.

        Attributes:
            time (list[datetime]): Timestamps of the traffic data
            hour (list[int]): Hours for each timestamp
            weekday (list[int]): Weekdays for each timestamp (0..6)
            week_number (list[int]): Week numbers for each timestamp
            count (list[int]): Number of vehicles for each timestamp
            speed (list[float]): Average traffic speed for each timestamp
            speed_sum (list[int]): Traffic speed sum for each timestamp
            density (list[float]): Traffic density for each timestamp
        
        Methods:
            add_data(self, time, speed): Adds data to the traffic data
    """

    # Last added timestamp
    last_time = 0

    # Traffic data
    time = []
    hour = []
    weekday = []
    week_number = []

    count = []
    speed = []
    speed_sum = []
    density = []

    # Adds data to the traffic data
    def add_data(self, time, speed):
        """
        Adds data to the traffic data.

            Parameters:
                time (datetime): Timestamp to add to the traffic data
                speed (int): Traffic speed to add for the timestamp
        """

        # Add data to existing timestamp
        if(time in self.time):
            index = self.time.index(time)
            self.count[index] = self.count[index] + 1
            self.speed_sum[index] = self.speed_sum[index] + speed
        # Add data to new timestamp
        else:
            self.time.append(time)
            self.hour.append(time.hour)
            self.weekday.append(time.weekday())
            self.week_number.append(time.isocalendar()[1])
            self.count.append(1)
            self.speed_sum.append(speed)

            index = 0
            if self.last_time in self.time:
                index = self.time.index(self.last_time)

            count = self.count[index]
            speed = self.speed_sum[index] / count
            speed_param = limit(speed_limit - speed, 0, speed_limit)
            density = (map(count, 0, count_limit, 0, 9) + map(speed_param, 0, speed_limit, 0, 9)) / 2

            self.speed.append(speed)
            self.density.append(density)
            self.last_time = time

# Limits a value in an interval
def limit(value, min, max):
    """
    limit(value, min, max) -> limited_value

    Limits a value in an interval.

        Parameters:
            value: Value to limit in the interval
            min: Minimum value the given value should have
            max: Maximum value the given value should have

        Returns:
            The given value limited in the interval
    """

    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value

# Maps a value from one range to another
def map(value, min_in, max_in, min_out, max_out):
    """
    map(value, min_in, max_in, min_out, max_out) -> mapped_value

    Maps a value from one range to another.

        Parameters:
            value: Value to map to the new range
            min_in: Minimum value of the input range
            max_in: Maximum value of the input range
            min_out: Minimum value of the output range
            max_out: Maximum value of the output range

        Returns:
            The given value mapped to the new range
    """

    scale = float(value - min_in) / float(max_in - min_in)
    scale = limit(scale, 0, 1)

    return (scale * float(max_out - min_out)) + min_out

# CSV folder of traffic data
folder = "210226_Daten_Hackathon/210226_Daten_Verkehr_Hackathon/"

# CSV files with traffic data
files = os.listdir(folder)

# Traffic data for each street direction
traffic_data = {}

# Read all CSV files
for file in files:

    # Open the CSV file
    with open(folder + file) as csv_file:
        # Read the CSV file with delimiter ";"
        csv_reader = csv.reader(csv_file, delimiter = ";")
        i = 0

        # Iterate through CSV rows
        for row in csv_reader:
            # Skip first line
            if i < 1:
                i = i + 1
                continue

            # Get parameters
            direction = row[2]
            speed = int(row[3])
            time = datetime.datetime.strptime(row[4][:-3], "%d.%m.%Y %H")

            # Get current traffic instance
            if (direction in traffic_data) == False:
                traffic_data[direction] = TrafficData()

            current = traffic_data[direction]

            # Add traffic data
            current.add_data(time, speed)

data_traffic = traffic_data["Richtung A nach B"]


# Traffic data of a location
class WeatherData:
    """
    A class to represent the weather data of a location.

        Attributes:
            time (list[datetime]): Timestamps of the weather data
            hour (list[int]): Hours for each timestamp
            weekday (list[int]): Weekdays for each timestamp (0..6)
            week_number (list[int]): Week numbers for each timestamp
            temperature (list[float]): Temperature at 2 meters above ground in Celsius for each timestamp
            wind_speed (list[float]): Wind speed at 100 meters above ground in meters per second for each timestamp
            precipitation (list[float]): Total precipitation in kilogram per square meter for each timestamp
            radiation (list[float]): Global radiation flux at the surface in Watt per square meter for each timestamp
        
        Methods:
            add_data(self, time, temperature, wind_speed, precipitation, radiation): Adds data to the weather data
    """

    # Weather data
    time = []
    hour = []
    weekday = []
    week_number = []

    temperature = []
    wind_speed = []
    precipitation = []
    radiation = []

    # Adds data to the weather data
    def add_data(self, time, temperature, wind_speed, precipitation, radiation):
        """
        Adds data to the weather data.

            Parameters:
                time (datetime): Timestamp to add to the weather data
                temperature (float): Temperature in Celsius to add for the timestamp
                wind_speed (float): Wind speed in meters per second to add for the timestamp
                precipitation (float): Total precipitation in kilogram per square meter to add for the timestamp
                radiation (float): Global radiation flux in Watt per square meter to add for the timestamp
        """

        self.time.append(time)
        self.hour.append(time.hour)
        self.weekday.append(time.weekday())
        self.week_number.append(time.isocalendar()[1])

        self.temperature.append(temperature)
        self.wind_speed.append(wind_speed)
        self.precipitation.append(precipitation)
        self.radiation.append(radiation)

# CSV file with weather data
file = "210226_Daten_Hackathon/210226_Daten_Wetter_Hackathon.csv"

# Weather data for each postcode
weather_data = {}

# Open the CSV file
with open(file) as csv_file:
    # Read the CSV file with delimiter ";"
    csv_reader = csv.reader(csv_file, delimiter = ";")
    i = 0

    # Iterate through CSV rows
    for row in csv_reader:
        # Skip first 2 lines
        if i < 2:
            i = i + 1
            continue

        # Get parameters
        time = datetime.datetime.strptime(row[0][:-3], "%d.%m.%Y %H")
        postcode = int(row[1])
        temperature = float(row[2].replace(",", "."))

        if row[3] == "":
            wind_speed = 0
        else:
            wind_speed = float(row[3].replace(",", "."))

        precipitation = float(row[4].replace(",", "."))
        radiation = float(row[5].replace(",", "."))

        # Get current weather instance
        if (postcode in weather_data) == False:
            weather_data[postcode] = WeatherData()

        current = weather_data[postcode]

        # Add wheather data
        current.add_data(time, temperature, wind_speed, precipitation, radiation)

data_weather = weather_data[76131]

# Returns a tensor which represents traffic density in retrospect of specific date
def traffic_to_tensor(data_traffic, time):
    """
    traffic_to_tensor(data_traffic, time) -> Tensor

    Returns a tensor which represents traffic density in retrospect of specific date.

        Parameters:
            data_traffic: Traffic data to get the traffic tensor for
            time: Timestamp to get the traffic tensor for

        Returns:
            A tensor of shape (density)
    """

    # Create the traffic density tensor
    if (time in data_traffic.time) == True:
        index = data_traffic.time.index(time)
        density = int(data_traffic.density[index])

        traffic_tensor = torch.tensor([density], dtype = torch.long)
    else:
        traffic_tensor = torch.tensor([0])

    return traffic_tensor

# Gets a random index for a list
def random_choice(size):
    """
    random_choice(size) -> int

    Gets a random index for a list.

        Parameters:
            size: Size of the list to get the random index for

        Returns:
            A random index for e list with given size
    """

    random_index = random.randint(0, size - 1)
    return random_index

def weather_to_tensor(data_weather, batch = 1, input_size = 7):
    """
    weather_to_tensor() -> Tensor, datetime

    Returns a random tensor of shape (seq_len, batch, input_size)

        Parameters:
            data: Class whitch provides weather data
            batch: Total number of training examples present in a single batch
            input_size: The number of expected features in the input x

        Returns:
            Tensor: A random tensor of shape (seq_len, batch, input_size)
            datetime: Datetime of the random tensor
    """

    # Create empty tensor
    n_samples = len(data_weather.temperature)
    tensor = torch.zeros(1, batch, input_size)

    # Add wheather data for each batch
    for i in range(batch):
        sample_index = random_choice(n_samples)

        tensor[0][i][0] = data_weather.temperature[sample_index]
        tensor[0][i][1] = data_weather.wind_speed[sample_index]
        tensor[0][i][2] = data_weather.precipitation[sample_index]
        tensor[0][i][3] = data_weather.radiation[sample_index]
        tensor[0][i][4] = data_weather.hour[sample_index]
        tensor[0][i][5] = data_weather.weekday[sample_index]
        tensor[0][i][6] = data_weather.week_number[sample_index]

    return tensor, data_weather.time[sample_index]