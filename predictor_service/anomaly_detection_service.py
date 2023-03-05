from flask import Flask, jsonify, request
from user_agents import parse
import json
import urllib.request as urllib2
import pandas as pd
import datetime
import joblib
from tensorflow import keras


timesteps = 10
training_mode = "supervised"
# creating a Flask app
app = Flask(__name__)

def getLoginTime(timestamp):
    #extract hour from timestamp
    dt_object = datetime.datetime.fromtimestamp(float(timestamp))
    x = dt_object.hour
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

def getCountryFromIP(ip):
    url = 'https://ipinfo.io/' + ip + '/json'
    response = urllib2.urlopen(url)
    data = json.load(response)
    country=data['country']
    return country
         
def deriveDevice(user_agent):
    if (user_agent.is_mobile):
        return 'mobile'
    elif (user_agent.is_tablet):
        return 'tablet'
    elif (user_agent.is_pc):
        return 'desktop'
    elif (user_agent.is_bot):
        return 'bot'
    else:
        return 'other'

def extractAgentData(userAgent):
    user_agent = parse(userAgent)
    browser = user_agent.browser.family
    os = user_agent.os.family
    device = deriveDevice(user_agent)
    return browser, os, device

def formDataframe(userAgent, timestamp, userID, location):
    browser, os_version, device = extractAgentData(userAgent)
    country = getCountryFromIP(location)
    login_time = getLoginTime(timestamp)
    data = {
        'user_id': [userID],
        'timestamp': [timestamp],
        'login_time': [login_time],
        'country': [country],
        'browser': [browser],
        'os_version': [os_version],
        'device': [device],
        'login_status': [1]
        }
    df = pd.DataFrame(data)

def getPastData(timesteps, userID):
    df = pd.read_csv('../data/LSTM_user_data/user_past_data.csv')
    #get last 9 columns with user_ID = a
    df = df[df['user_id'] == userID].tail(timesteps)
    return df

def encodeData(df):
    id_encoder = joblib.load("../LSTM/supervised/encoders/id_encoder.joblib")
    country_encoder = joblib.load("../LSTM/supervised/encoders/country_encoder.joblib")
    browser_encoder = joblib.load("../LSTM/supervised/encoders/browser_encoder.joblib")
    OS_encoder = joblib.load("../LSTM/supervised/encoders/OS_encoder.joblib")
    device_encoder = joblib.load("../LSTM/supervised/encoders/device_encoder.joblib")
    time_encoder = joblib.load("../LSTM/supervised/encoders/time_encoder.joblib")
    min_max_scaler = joblib.load("../LSTM/supervised/encoders/uid_min_max_scaler.joblib")

    transformed_country = country_encoder.transform(df['country'].to_numpy().reshape(-1, 1))
    ohe_df_contry = pd.DataFrame(transformed_country, columns=country_encoder.get_feature_names_out())
    df = pd.concat([df, ohe_df_contry], axis=1).drop(['country'], axis=1)

    transformed_browser = browser_encoder.transform(df['browser'].to_numpy().reshape(-1, 1))
    ohe_df_browser = pd.DataFrame(transformed_browser, columns=browser_encoder.get_feature_names_out())
    df = pd.concat([df, ohe_df_browser], axis=1).drop(['browser'], axis=1)

    transformed_os = OS_encoder.transform(df['os_version'].to_numpy().reshape(-1, 1))
    ohe_df_os_version = pd.DataFrame(transformed_os, columns=OS_encoder.get_feature_names_out())
    df = pd.concat([df, ohe_df_os_version], axis=1).drop(['os_version'], axis=1)

    transformed_device = device_encoder.transform(df['device'].to_numpy().reshape(-1, 1))
    ohe_df_device = pd.DataFrame(transformed_device, columns=device_encoder.get_feature_names_out())
    df = pd.concat([df, ohe_df_device], axis=1).drop(['device'], axis=1)

    transformed_time = time_encoder.transform(df['login_time'].to_numpy().reshape(-1, 1))
    ohe_df_time = pd.DataFrame(transformed_time, columns=time_encoder.get_feature_names_out())
    df = pd.concat([df, ohe_df_time], axis=1).drop(['login_time'], axis=1)

    transformed_uid = id_encoder.transform(df['user_id'].to_numpy().reshape(-1, 1))
    encoded_uid= pd.DataFrame(transformed_uid, columns=['uid_code'])
    df = pd.concat([df, encoded_uid], axis=1).drop(['user_id'], axis=1)

    uid_scaled = min_max_scaler.fit_transform(df['uid_code'].to_numpy().reshape(-1, 1))
    uid_scaled = pd.DataFrame(uid_scaled, columns=['uid_scaled'])
    df = pd.concat([df, uid_scaled], axis=1).drop(['uid_code'], axis=1)

    return df

def getRiskScoreSupervised(df):
    model = joblib.load("../LSTM/supervised/models/LSTM_model.joblib")
    X = df.drop(['timestamp'], axis=1)
    X = X.to_numpy()
    X = X.reshape(1, X.shape[0], X.shape[1])
    risk_score = model.predict(X)
    return risk_score

def getRiskScoreUnsupervised(df):
    model = joblib.load("../LSTM/unsupervised/models/LSTM_autoencoder_model.joblib")
    X = df.drop(['timestamp'], axis=1)
    X = X.to_numpy()
    X = X.reshape(1, X.shape[0], X.shape[1])
    risk_score = model.predict(X)
    return risk_score

@app.route('/getAnomalyScore', methods=['POST'])
def getAnomalyScore():
    if request.method == 'POST':
        incoming_data = request.get_json()
        userAgent = incoming_data['userAgent']
        timestamp = incoming_data['timestamp']
        userID = incoming_data['userID']
        location = incoming_data['location']
        df = formDataframe(userAgent, timestamp, userID, location)
        pastData = getPastData(timesteps, userID)
        if (pastData.empty):
            return jsonify(isError= True,
                        message= "No past data found for user",
                        statusCode= 400,
                        data= {}), 400
        df = df.append(pastData, ignore_index=True)
        df = encodeData(df)
        risk_score = 1
        if (training_mode == 'supervised'):
            risk_score = getRiskScoreSupervised(df)
        else:
            risk_score = getRiskScoreUnsupervised(df)
        return_data = {"riskScore": risk_score}
        return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200,
                    data= return_data), 200

if __name__ == '__main__':
    app.run(debug = True)


