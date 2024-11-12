
import pandas as pd

checkin_checkout_df = pd.read_csv('/Users/joannarasmussen/Documents/DTU/02807/Project/final_project_data_science/source/checkin_checkout_history_updated.csv')
gym_location_df = pd.read_csv('/Users/joannarasmussen/Documents/DTU/02807/Project/final_project_data_science/source/gym_locations_data.csv')
subscription_df = pd.read_csv('/Users/joannarasmussen/Documents/DTU/02807/Project/final_project_data_science/source/subscription_plans.csv')
user_df = pd.read_csv('/Users/joannarasmussen/Documents/DTU/02807/Project/final_project_data_science/source/users_data.csv')

checkin_checkout_df.drop(['calories_burned'], axis = 1, inplace = True) # Remove 'calories_burned' column - not interested to look at

# Calculate workout length (in minutes) for each session - add as column
checkin_checkout_df['workout_duration (min)'] = (pd.to_datetime(checkin_checkout_df['checkout_time']) - 
                                        pd.to_datetime(checkin_checkout_df['checkin_time'])).dt.total_seconds() / 60

# First "extracting" the hour of check-in, e.g. 15 o'clock.
# Group into either morning, afternoon or evening depending on the time checked in
checkin_checkout_df['time_window'] = pd.to_datetime(checkin_checkout_df['checkin_time']).dt.hour 
checkin_checkout_df['time_of_day'] = pd.cut(
    checkin_checkout_df['time_window'],
    bins = [0, 5, 8, 11, 14, 17, 20, 23, 24],
    labels = ['odd hours', 'early morning', 'morning', 'noon', 'afternoon', 'evening', 'late evening', 'odd hours'],
    include_lowest = True,
    ordered = False
)
checkin_checkout_df.drop(['time_window'], axis = 1, inplace = True) # Remove 'time_window' column - not interested to look at
checkin_checkout_df = checkin_checkout_df.merge(user_df[['user_id', 'age', 'gender']], on = 'user_id', how = 'left')
#print(checkin_checkout_df.head(25))

# Groupby gym and extract most frequent item 
gym_summary = checkin_checkout_df.groupby('gym_id').agg({
    'time_of_day': lambda x: x.mode()[0],  # Most common time window
    'workout_type': lambda x: x.mode()[0],  # Most common workout type
    'workout_duration (min)': 'mean',  # Average workout duration
    'gender': lambda x: x.mode()[0]
}).reset_index()

gym_summary.columns = ['gym_id', 'peak_time_of_day', 'popular_workout_type', 'avg_workout_duration', 'most_common_gender']
print(gym_summary.head(25))

gender_summary = checkin_checkout_df.groupby('gender').agg({
    'age': 'mean', 
    'workout_type': lambda x: x.mode()[0] 
}).reset_index()
print(gender_summary)