#Filter out users with more than 200 logins
#The filtered data is sorted by user ID and login timestamp.

import pandas as pd

df = pd.read_csv("initial_preprocessed_data.csv")

#Filter out users with more than 200 logins
df1 = df[df['User ID'].map(df['User ID'].value_counts()) >= 200]

unique_users = df1['User ID'].nunique()
print("Number of unique users with more than 200 logins: ", unique_users)

#Get only the last 200 logins of each user
df1 = df1.groupby('User ID').tail(200).reset_index(drop=True)
shape = df1.shape
print('Number of login entries :', shape[1])

df1['User ID'] = df1['User ID'].astype(str)
df1['Login Timestamp'] = pd.to_datetime(df1['Login Timestamp'])
df1 = df1.sort_values(['User ID','Login Timestamp'])

df1.to_csv('preprocessed_data_200_per_user.csv', mode='a', index=False)

