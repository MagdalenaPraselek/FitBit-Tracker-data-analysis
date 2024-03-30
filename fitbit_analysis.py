
#distinct - participants
#records per day

"""
Questions:
    1. How do users use fitbit? // daily activity // trends
    2. What are the benefts for users and how can we emphasize them?
"""

#importing neccesary modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



#importing selected data
df_daily_activity = pd.read_csv('Datasets\dailyActivity_merged.csv')
df_daily_sleep = pd.read_csv('Datasets\sleepDay_merged.csv')
df_daily_calories = pd.read_csv('Datasets\dailyCalories_merged.csv')
df_hourly_intensities = pd.read_csv('Datasets\hourlyIntensities_merged.csv')
df_hourly_steps = pd.read_csv('Datasets\hourlySteps_merged.csv')
df_hourly_calories = pd.read_csv('Datasets\hourlyCalories_merged.csv')


#data cleaning
df_daily_activity.drop(columns = ['TotalDistance', 'TrackerDistance', 'LoggedActivitiesDistance', 'VeryActiveDistance', 'ModeratelyActiveDistance', 'LightActiveDistance', 'SedentaryActiveDistance'], inplace = True)
df_daily_sleep.drop(columns = ['TotalTimeInBed'], inplace = True)


#printing df info
print(df_daily_activity.info())
print(df_daily_sleep.info())
print(df_daily_calories.info())
print(df_hourly_intensities.info())
print(df_hourly_steps.info())
print(df_hourly_calories.info())


#managing duplicates
print('Checking duplicates: ')
print('Daily activity: ' + str(df_daily_activity[df_daily_activity.duplicated()]))
print('Daily sleep: ' + str(df_daily_sleep[df_daily_sleep.duplicated()]))
print('Daily calories: ' + str(df_daily_calories[df_daily_calories.duplicated()]))
print('Hourly intensities: ' + str(df_hourly_intensities[df_hourly_intensities.duplicated()]))
print('Hourly steps: ' + str(df_hourly_steps[df_hourly_steps.duplicated()]))
print('Hourly calories: ' + str(df_hourly_calories[df_hourly_calories.duplicated()]))

df_daily_sleep.drop_duplicates(inplace = True)

#managing NaN
print('Checking if there are NaN values:')
print(df_daily_activity.isnull().any())
print(df_daily_sleep.isnull().any())
print(df_daily_calories.isnull().any())
print(df_hourly_intensities.isnull().any())
print(df_hourly_steps.isnull().any())
print(df_hourly_calories.isnull().any())

#changing Date columns type into DateTimeIndex
df_daily_activity['ActivityDate'] = pd.to_datetime(df_daily_activity['ActivityDate'])
df_daily_sleep['SleepDay'] = pd.to_datetime(df_daily_sleep['SleepDay'], format = '%m/%d/%Y %I:%M:%S %p')
df_daily_calories['ActivityDay'] = pd.to_datetime(df_daily_calories['ActivityDay'])
df_hourly_intensities['ActivityHour'] = pd.to_datetime(df_hourly_intensities['ActivityHour'], format = '%m/%d/%Y %I:%M:%S %p')
df_hourly_steps['ActivityHour'] =  pd.to_datetime(df_hourly_steps['ActivityHour'], format = '%m/%d/%Y %I:%M:%S %p')
df_hourly_calories['ActivityHour'] =  pd.to_datetime(df_hourly_calories['ActivityHour'], format = '%m/%d/%Y %I:%M:%S %p')

#changing columns name
df_daily_activity.rename(columns = {'ActivityDate': 'Date'}, inplace = True)
df_daily_sleep.rename(columns = {'SleepDay': 'Date'}, inplace = True)
df_daily_calories.rename(columns = {'ActivityDay': 'Date'}, inplace = True)
df_hourly_intensities.rename(columns = {'ActivityHour': 'DateTime'}, inplace = True)
df_hourly_steps.rename(columns = {'ActivityHour': 'DateTime'}, inplace = True)
df_hourly_calories.rename(columns = {'ActivityHour': 'DateTime'}, inplace = True)




#counting participants
print('Participants:')
print('All: ' + str(df_daily_activity['Id'].nunique()))
print('Sleep: ' + str(df_daily_sleep['Id'].nunique()))

#computations   
df_daily_activity['TotalActiveMinutes'] = df_daily_activity['VeryActiveMinutes'] + df_daily_activity['FairlyActiveMinutes'] + df_daily_activity['LightlyActiveMinutes']
df_daily_activity['DayOfWeek'] = df_daily_activity['Date'].dt.dayofweek.map({0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'})
df_hourly_intensities['Hour'] = df_hourly_intensities['DateTime'].dt.hour
df_hourly_steps['Hour'] = df_hourly_steps['DateTime'].dt.hour
df_hourly_steps['DayOfWeek'] = df_hourly_steps['DateTime'].dt.dayofweek.map({0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'})
df_daily_sleep['DayOfWeek'] = df_daily_sleep['Date'].dt.dayofweek.map({0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'})
df_hourly_calories['Hour'] = df_hourly_calories['DateTime'].dt.hour

pie_data = [df_daily_activity.iloc[::, i].sum() for i in range(3, 7)]
pie_labels = df_daily_activity.columns[3:7]

#printing descriptive stats

daily_activity_stats = df_daily_activity.describe()
daily_sleep_stats = df_daily_sleep.describe()
daily_calories_stats = df_daily_calories.describe()
hourly_intensities_stats = df_hourly_intensities.describe()
hourly_steps_stats = df_hourly_steps.describe()
hourly_calories_stats = df_hourly_calories.describe()


#data frames merging
df_daily_sleep_calories = pd.merge(df_daily_sleep, df_daily_calories, on = ['Id', 'Date'], how = 'inner')


#creating plots
sns.set()
sns.set_palette('viridis')

plt.pie(pie_data, autopct='%1.1f%%', pctdistance=1.2, labeldistance=1.4, radius = 1.3)
plt.title('Activty distribution', x = 0, y = 1.1)
plt.legend(pie_labels, bbox_to_anchor=(0, 1.1))
plt.show()

sns.histplot(data = df_daily_activity, x = 'TotalActiveMinutes')
plt.title('Daily active minutes distribution')
plt.xlabel('Active minutes')
plt.ylabel('Count')
plt.show()

sns.histplot(data = df_daily_activity, x = 'TotalSteps')
plt.title('Daily steps distribution')
plt.xlabel('Steps')
plt.ylabel('Count')
plt.xlim([0, 25000])
plt.show()

sns.lmplot(data = df_daily_activity, x = 'TotalActiveMinutes', y = 'Calories')
plt.title('Daily active minutes vs calories')
plt.xlabel('Active minutes')
plt.ylabel('Calories')
plt.show()

sns.lmplot(data = df_daily_activity, x = 'TotalSteps', y = 'Calories')
plt.title('Daily steps vs calories')
plt.xlabel('Steps')
plt.ylabel('Calories')
plt.show()




sns.barplot(data = df_daily_activity, x = 'DayOfWeek', y = 'TotalActiveMinutes')
plt.title('Daily active minutes vs. day of week')
plt.xlabel('Day of week')
plt.ylabel('Active minutes')
plt.show()

sns.barplot(data = df_daily_activity, x = 'DayOfWeek', y = 'TotalSteps')
plt.title('Daily steps vs. day of week')
plt.xlabel('Day of week')
plt.ylabel('Steps')
plt.show()

sns.barplot(data = df_daily_activity, x = 'DayOfWeek', y = 'Calories')
plt.title('Calories vs. day of week')
plt.xlabel('Day of week')
plt.ylabel('Daily calories')
plt.show()

sns.barplot(data = df_daily_sleep, x = 'DayOfWeek', y = 'TotalMinutesAsleep')
plt.title('Sleep vs. day of week')
plt.xlabel('Day of week')
plt.ylabel('Daily minutes asleep')
plt.show()

sns.barplot(data = df_hourly_intensities, x = 'Hour', y = 'TotalIntensity')
plt.title('Intensity vs. time')
plt.xlabel('Time')
plt.ylabel('Intensity')
plt.show()

sns.barplot(data = df_hourly_steps, x = 'Hour', y = 'StepTotal')
plt.title('Steps vs. time')
plt.xlabel('Time')
plt.ylabel('Steps')
plt.show()

sns.barplot(data = df_hourly_calories, x = 'Hour', y = 'Calories')
plt.title('Calories vs. time')
plt.xlabel('Time')
plt.ylabel('Calories')
plt.show()



