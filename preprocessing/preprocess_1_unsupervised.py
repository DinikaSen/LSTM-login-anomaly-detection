#Extract login data between 3rd Feb 2020 and 3rd Aug 2020 from the original dataset.
#The original dataset is too large to be processed in one go. Hence, it is split into chunks of 100000.
#The chunks are then processed and saved into a new file.

import pandas as pd

#Required feature columns.
data_columns = ['Login Timestamp','User ID','Country','User Agent String','Browser Name and Version','OS Name and Version','Device Type','Login Successful','Is Attack IP','Is Account Takeover']

#Required date range
date_first = '2020-02-03'
date_last = '2020-10-03'

#All anonymus users are labelled under this user ID. Hence, will be skipped.
skip_userID = '-4324475583306591935'
skip_userID2 = '6998943612473066845'

write_header = True

def generate_malicious_column(row):
    if row['Is Attack IP'] or row['Is Account Takeover']:
        return 1
    return 0

df = pd.read_csv("/Users/dinika/Desktop/Dinika/MSc/Dissertation_Source_code/data_preprocess/rba-dataset.csv", chunksize=100000, usecols=data_columns)

result = None
for chunk in df:
    chunk = chunk[(chunk['User ID'].astype(str) != skip_userID) & (chunk['User ID'].astype(str) != skip_userID2)
                  & (chunk['Login Timestamp'].astype(str).str[:10] >= date_first)
                  & (chunk['Login Timestamp'].astype(str).str[:10] <= date_last)
                  ]

    chunk['is_malicious'] = chunk.apply(lambda row: generate_malicious_column(row), axis=1)

    chunk.to_csv('initial_preprocessed_data_unsupervised.csv', mode='a', index=False, header=write_header)
    write_header = False

print("Finished processing")

