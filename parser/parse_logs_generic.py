import re

log = ''

# Define regular expression pattern
pattern = r'\[([\d-]+)\] \[\] \[(.+)\] \[(.+)\] (\S+) {(.+)} — .*"remoteIp":"(\d+\.\d+\.\d+\.\d+)".*"User-Agent":"([^"]*)".*"username":"([^"]*)"'

# Match the pattern to the log message
match = re.match(pattern, log)

# Extract the matched groups
if match:
    tenant_id = match.group(1)
    timestamp = match.group(2)
    unique_id = match.group(3)
    log_level = match.group(4)
    event_data = match.group(5)
    ip_address = match.group(6)
    user_agent = match.group(7)
    user_id = match.group(8)
    
    # Output the extracted values
    print("Tenant ID:", tenant_id)
    print("Timestamp:", timestamp)
    print("Unique ID:", unique_id)
    print("Log level:", log_level)
    print("Event data:", event_data)
    print("IP address:", ip_address)
    print("User agent:", user_agent)
    print("User ID:", user_id)
else:
    print("No match found")