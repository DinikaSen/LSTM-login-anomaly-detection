import pandas as pd
import numpy as np
import re

def remove_version(string_with_version):
    res = re.findall('([a-zA-Z ]*)\d*.*', string_with_version)
    return str(res[0]).strip()

def get_time_of_day(x):
    if (x > 4) and (x <= 6):
        return 'early_morning'
    elif (x > 6) and (x <= 8):
        return 'morning'
    elif (x > 8) and (x <= 11):
        return'late_morning'
    elif (x > 11) and (x <= 13):
        return'noon'
    elif (x > 13) and (x <= 15):
        return'afternoon'
    elif (x > 15) and (x <= 18) :
        return 'evening'
    elif (x > 18) and (x <= 20) :
        return 'late_evening'
    elif (x > 20) and (x <= 24):
        return 'night'
    elif (x <= 4):
        return 'late_night'

df = pd.read_csv("/Users/dinika/Desktop/Dinika/MSc/Dissertation_Source_code/Authentication_Anomaly_Detection_Module/preprocessing/preprocessed_data_150_per_user_unsupervised.csv")

df.rename(columns={'User ID':'user_id'}, inplace=True)
df.rename(columns={'Login Timestamp':'datetime'}, inplace=True)
df.rename(columns={'Country':'country'}, inplace=True)
df.rename(columns={'Device Type':'device'}, inplace=True)
df.rename(columns={'Login Successful':'is_login_success'}, inplace=True)

df['user_id'] =  pd.to_numeric(df['user_id'])
df['datetimef'] =  pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M:%S.%f')
df['hour'] = df['datetimef'].dt.hour
df['login_time'] = df['hour'].apply(get_time_of_day)
df['timestamp'] = df.datetimef.values.astype(np.int64)
df['login_status'] = np.where(df['is_login_success'].astype(str)== 'True', 1, 0)

df['os_version'] = df['OS Name and Version'].apply(remove_version)
df['browser'] = df['Browser Name and Version'].apply(remove_version)

df_new = df[['user_id','timestamp','login_time','country','browser','os_version','device','login_status','is_malicious']]

unique_item_count = df_new.nunique()
print (unique_item_count)

header = ['user_id','timestamp','login_time','country','browser','os_version','device','login_status','is_malicious']
df_new.to_csv('final_processed_user_data_un.csv', columns = header, index=False)
