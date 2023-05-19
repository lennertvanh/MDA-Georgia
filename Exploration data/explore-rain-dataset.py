import pandas as pd

weather_data = pd.read_csv("../Data/combined_weatherdata_2022.csv", header = 0, sep=',')
print(weather_data.head())

print(weather_data['LC_DAILYRAIN'])
#theoretically 0.2mm or more is a rainy day