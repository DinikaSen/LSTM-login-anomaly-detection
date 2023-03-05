# Authentication Anomaly Detection using LSTM

This is an implementation of a framework that detects authentication anomalies in enterprise authentication systems using LSTM based techniques. The framework consists of 3 main components.
1. Log parser
2. LSTM based model
3. Anomaly detection service

## Log parser
Any standard authentication server today logs the user login events to log files. The information available in those log files can be used to extract useful information about the user login patterns which can then be used to identify malicious login events. The log parser component parses authentication logs and extracts the useful information required by the LSTM model to train. Since each authentication server uses its own formats for logging, it is not possible to build a paser that works for any authentication log. Hence, you can use the provided framework to build a parser to extract the required information as defined in the <HOME>/parser/parse_logs_generic.py sketch.

## LSTM based model
This component contains 2 pretrained LSTM models with its source code so that the models can be retrained for your own dataset. The two LSTM nodels are based on two different LSTM architectures. 

One model is an unsupervised model which uses LSTM based autoencoders to detect malicious logins. This model can be used when you do not have labelled malicious login data. The interactive jupyter notebook code for the model can be accessed from <HOME>/LSTM/unsupervised/<HOME>/parser/lstm_autoencoder.ipynb

The other model is a supervised model which uses an LSTM architecture to detect malicious logins. This model can be used when you have labelled malicious login data. The interactive jupyter notebook code for the model can be accessed from <HOME>/LSTM/supervised/<HOME>/parser/lstm_supervised.ipynb

For each model, the categorical encoders, scalars, sampled login sequences, trained model are saved in order to make it possible to use them for real world anomaly detection on live authentication data.

## Anomaly detection service
The anomaly detection service is a REST endpoint which can be called from an authentication server via POST requests with the required information about a real time authentication event. The anomaly detection service then predicts the anomaly score (risk score) for that login event, and responds it back to the authentication server. The service can be run by following the below commands.

```sh
cd predictor_service
python3 anomaly_detection_service.py
```

This will initiate a service running on http://127.0.0.1:5000. You can send post requests to the /getAnomalyScore with required information. Below curl command contains a sample request for your reference.

```sh
curl --location --request POST 'http://127.0.0.1:5000/getAnomalyScore' \
--header 'Content-Type: text/plain' \
--data-raw '{
    "userAgent":"Mozilla/5.0  (iPad; CPU OS 7_1 like Mac OS X) AppleWebKit/533.1 (KHTML, like Gecko Version/4.0 Mobile Safari/533.1 variation/277457",
    "timestamp":"1589912560607000000",
    "userID":"1023937207516135485",
    "location":"212.78.83.12"
}'
```
The service will then response with the risk score associated with the login event in the below format.

```sh
{"riskScore": 0.5}
``` 
