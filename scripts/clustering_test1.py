
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

checkin_checkout_df = pd.read_csv('checkin_checkout_history_updated.csv')
gym_location_df = pd.read_csv('gym_locations_data.csv')
subscription_df = pd.read_csv('subscription_plans.csv')
user_df = pd.read_csv('users_data.csv')

# JOIN dataframes

# Calculate workout duration
checkin_checkout_df['workout_duration (min)'] = (pd.to_datetime(checkin_checkout_df['checkout_time']) - 
                                        pd.to_datetime(checkin_checkout_df['checkin_time'])).dt.total_seconds() / 60  # in minutes

checkin_checkout_df['time_window'] = pd.to_datetime(checkin_checkout_df['checkin_time']).dt.hour
checkin_checkout_df['time_of_day'] = pd.cut(
    checkin_checkout_df['time_window'],
    bins = [0, 12, 18, 24],
    labels = ['morning', 'afternoon', 'evening'],
    include_lowest = True
)

# Data by gym
gym_summary = checkin_checkout_df.groupby('gym_id').agg({
    'time_of_day': lambda x: x.mode()[0],  # Most common time window
    'workout_type': lambda x: x.mode()[0],  # Most common workout type
    'workout_duration (min)': 'mean',  # Average workout duration
    'user_id': 'count',  # Total check-ins (proxy for activity level)
}).reset_index()

gym_summary.columns = ['gym_id', 'peak_time_of_day', 'popular_workout_type', 'avg_workout_duration', 'total_checkins']
print(gym_summary)
