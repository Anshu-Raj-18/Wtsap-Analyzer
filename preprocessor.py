import pandas as pd
import re
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}[\s\u202f]?[ap]m\s-\s'
    messages = re.split(pattern, data)[1:]
    date_pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}[\s\u202f]?[ap]m'

    dates = re.findall(date_pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = df['message_date'].str.replace('\u202f', ' ', regex=False)

    df['message_date'] = pd.to_datetime(
        df['message_date'],
        format='%d/%m/%y, %I:%M %p'
    )
    df.rename(columns={'message_date': 'data'}, inplace=True)
    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)

        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['month_num'] = df['data'].dt.month
    # year date and time seperation
    df['year'] = df['data'].dt.year
    df['month'] = df['data'].dt.month_name()
    df['day'] = df['data'].dt.day
    df['hour'] = df['data'].dt.hour
    df['minute'] = df['data'].dt.minute
    return df