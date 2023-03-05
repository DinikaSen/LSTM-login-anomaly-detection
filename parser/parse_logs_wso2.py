import re

#Define your log file path here
log_file_path = "sample_data/wso2_IS_events.log"

def log_parser(file_path):
    logs = []
    with open(file_path, 'r') as file:
        for line in file:
            # if line starts from word 'Event' then it is a new log
            if line.startswith('Event'):
                print(line)
                log = {}

                #find the remoteIp frrom the line
                remoteIp = re.search(r'(?<=remoteIp=)(.*?)(?=,)', line).group(0)
                print(remoteIp)


                # Parse the IP address
                ip_address = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line).group(0)
                log['ip_address'] = ip_address
                
                # Parse the timestamp
                timestamp = re.search(r'\[(.*)\]', line).group(0)
                log['timestamp'] = timestamp
                
                # Parse the HTTP method and URL
                request = re.search(r'\"(.*)\"', line).group(0)
                log['request'] = request
                
                # Parse the status code
                status_code = re.search(r'(\d{3})', line).group(0)
                log['status_code'] = status_code
                
                # Add the log to the logs list
                logs.append(log)

            # log = {}
            # # Parse the IP address
            # ip_address = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line).group(0)
            # log['ip_address'] = ip_address
            
            # # Parse the timestamp
            # timestamp = re.search(r'\[(.*)\]', line).group(0)
            # log['timestamp'] = timestamp
            
            # # Parse the HTTP method and URL
            # request = re.search(r'\"(.*)\"', line).group(0)
            # log['request'] = request
            
            # # Parse the status code
            # status_code = re.search(r'(\d{3})', line).group(0)
            # log['status_code'] = status_code
            
            # # Add the log to the logs list
            # logs.append(log)
    return logs

logs = log_parser(log_file_path)

print(logs[:5])


# import re

# log = 'TID: [-1234] [] [2023-01-19 20:53:33,901] [34751e5b-344b-4af3-8edf-baf532380d7c] INFO {org.wso2.carbon.event.output.adapter.logger.LoggerEventAdapter} — Unique ID: auth, Event: {"event":{"metaData":{"tenantId":-1234},"payloadData":{"contextId":"3ef244c6-2e35-4482-a883-7d80daf25003","eventId":"6627293f-b197-4fad-8947-6bccbd7d38d8","eventType":"step","authenticationSuccess":false,"username":"admin@guardio.com","localUserName":"admin@guardio.com","userStoreDomain":"PRIMARY","tenantDomain":"carbon.super","remoteIp":"127.0.0.1","region":"NOT_AVAILABLE","inboundAuthType":"oidc","serviceProvider":"Console","rememberMeEnabled":false,"forceAuthEnabled":false,"passiveAuthEnabled":false,"rolesCommaSeparated":"admin,SelfRegisterWorkflow","authenticationStep":"1","identityProvider":"LOCAL","authStepSuccess":true,"stepAuthenticator":"BasicAuthenticator","isFirstLogin":false,"identityProviderType":"LOCAL","_timestamp":1674161613883}}}'

# # Define regular expression pattern
# pattern = r'\[([\d-]+)\] \[\] \[(.+)\] \[(.+)\] (\S+) {(.+)} — .*"remoteIp":"(\d+\.\d+\.\d+\.\d+)".*"User-Agent":"([^"]*)".*"username":"([^"]*)"'

# # Match the pattern to the log message
# match = re.match(pattern, log)

# # Extract the matched groups
# if match:
#     tenant_id = match.group(1)
#     timestamp = match.group(2)
#     unique_id = match.group(3)
#     log_level = match.group(4)
#     event_data = match.group(5)
#     ip_address = match.group(6)
#     user_agent = match.group(7)
#     user_id = match.group(8)
    
#     # Output the extracted values
#     print("Tenant ID:", tenant_id)
#     print("Timestamp:", timestamp)
#     print("Unique ID:", unique_id)
#     print("Log level:", log_level)
#     print("Event data:", event_data)
#     print("IP address:", ip_address)
#     print("User agent:", user_agent)
#     print("User ID:", user_id)
# else:
#     print("No match found")