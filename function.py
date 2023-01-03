import datetime
import json
import traceback
import urllib3
import time
import pandas as pd
import numpy as np


def facebook():
    # prendere il file
    df_facebook = pd.read_csv(
        'https://docs.google.com/spreadsheets/d/11AbcGG4K2b5tdV53mkW2iHPf9CehtzBku88aHTU5pxg/edit?usp=sharing')

# pulire il file
    df_facebook = df_facebook.dropna(axis=1, how="any")

# crea le variabili
# CPM
    last_CPM_Facebook = df_facebook.iloc[-1, 2]
    last_CPM_Facebook = last_CPM_Facebook.replace('€', '')
    last_CPM_Facebook = last_CPM_Facebook.replace(',', '.')
    last_CPM_Facebook = float(last_CPM_Facebook)

    secondo_CPM_Facebook = df_facebook.iloc[-8, 2]
    secondo_CPM_Facebook = secondo_CPM_Facebook.replace('€', '')
    secondo_CPM_Facebook = secondo_CPM_Facebook.replace(',', '.')
    secondo_CPM_Facebook = float(secondo_CPM_Facebook)

    differenza_CPM = round(
        (last_CPM_Facebook/secondo_CPM_Facebook-1)*100, 2)
    differenza_CPM

    if differenza_CPM < 0:
        messaggio_cpm = f"🟢 {differenza_CPM}% CPM Facebook rispetto alla settimana prima"
        else:
        messaggio_cpm = f"🔴 +{differenza_CPM}% CPM Facebook rispetto alla settimana prima"


# Amount Spent
        last_spent_Facebook = df_facebook.iloc[-1, 1]
        last_spent_Facebook = last_spent_Facebook.replace('€', '')
        last_spent_Facebook = last_spent_Facebook.replace(',', '.')
        last_spent_Facebook = float(last_spent_Facebook)

        secondo_spent_Facebook = df_facebook.iloc[-8, 1]
        secondo_spent_Facebook = secondo_spent_Facebook.replace('€', '')
        secondo_spent_Facebook = secondo_spent_Facebook.replace(',', '.')
        secondo_spent_Facebook = float(secondo_spent_Facebook)

        differenza_spent = round(
            (last_spent_Facebook/secondo_spent_Facebook-1)*100, 2)
        differenza_spent

        if differenza_spent < 0:
        messaggio_spent_facebook = f"🟢 {differenza_spent}% Budget Speso su Facebook rispetto alla settimana prima"
        else:
        messaggio_spent_facebook = f"🔴 +{differenza_spent}% Budget Speso su Facebook rispetto alla settimana prima"

        # CPC
        last_CPC_Facebook = df_facebook.iloc[-1, 3]
        last_CPC_Facebook = last_CPC_Facebook.replace('€', '')
        last_CPC_Facebook = last_CPC_Facebook.replace(',', '.')
        last_CPC_Facebook = float(last_CPC_Facebook)

        secondo_CPC_Facebook = df_facebook.iloc[-8, 3]
        secondo_CPC_Facebook = secondo_CPC_Facebook.replace('€', '')
        secondo_CPC_Facebook = secondo_CPC_Facebook.replace(',', '.')
        secondo_CPC_Facebook = float(secondo_CPC_Facebook)

        differenza_CPC = round(
            (last_CPC_Facebook/secondo_CPC_Facebook-1)*100, 2)
        differenza_CPC

        if differenza_CPC < 0:
            messaggio_cpc_facebook = f"🟢 {differenza_CPC}% CPC Facebook rispetto alla settimana prima"
        else:
            messaggio_cpc_facebook = f"🔴 +{differenza_CPC}% CPC Facebook rispetto alla settimana prima"

        # CTR
        last_CTR_Facebook = df_facebook.iloc[-1, -1]
        last_CTR_Facebook = float(last_CTR_Facebook.replace(',', '.'))

        secondo_CTR_Facebook = df_facebook.iloc[-8, -1]
        secondo_CTR_Facebook = float(secondo_CTR_Facebook.replace(',', '.'))

        differenza_CTR = round(
            (last_CTR_Facebook/secondo_CTR_Facebook-1)*100, 2)
        differenza_CTR

        if differenza_CTR < 0:
            messaggio_CTR = f"🔴{differenza_CTR}% CTR Facebook rispetto alla settimana prima"
        else:
            messaggio_CTR = f"🟢 +{differenza_CTR}% CTR Facebook rispetto alla settimana prima"

        facebook = [differenza_spent, differenza_CTR,
                    differenza_CPC, differenza_CPM]
        facebook.sort()

        messaggio_facebook = []
        if len(messaggio_facebook) >= 0:
            if (facebook[0] == differenza_spent):
                messaggio_facebook.insert(0, messaggio_spent_facebook)
            elif (facebook[0] == differenza_CTR):
                messaggio_facebook.insert(0, messaggio_CTR)
            elif (facebook[0] == differenza_CPM):
                messaggio_facebook.insert(0, messaggio_cpm)
            else:
                messaggio_facebook.insert(0, messaggio_cpc_facebook)

            if (facebook[1] == differenza_spent):
                messaggio_facebook.insert(1, messaggio_spent_facebook)
            elif (facebook[1] == differenza_CTR):
                messaggio_facebook.insert(1, messaggio_CTR)
            elif (facebook[1] == differenza_CPM):
                messaggio_facebook.insert(1, messaggio_cpm)
            else:
                messaggio_facebook.insert(1, messaggio_cpc_facebook)

            if (facebook[2] == differenza_spent):
                messaggio_facebook.insert(2, messaggio_spent_facebook)
            elif (facebook[2] == differenza_CTR):
                messaggio_facebook.insert(2, messaggio_CTR)
            elif (facebook[2] == differenza_CPM):
                messaggio_facebook.insert(2, messaggio_cpm)
            else:
                messaggio_facebook.insert(2, messaggio_cpc_facebook)

            if (facebook[3] == differenza_spent):
                messaggio_facebook.insert(3, messaggio_spent_facebook)
            elif (facebook[3] == differenza_CTR):
                messaggio_facebook.insert(3, messaggio_CTR)
            elif (facebook[3] == differenza_CPM):
                messaggio_facebook.insert(3, messaggio_cpm)
            else:
                messaggio_facebook.insert(3, messaggio_cpc_facebook)


messaggio = (f"""Recap della settimana prima

Facebook Ads:
{messaggio_facebook[0]}
{messaggio_facebook[1]}
{messaggio_facebook[2]}
{messaggio_facebook[3]}
""")

# slack
WEBHOOK_URL = "https://hooks.slack.com/services/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"

# Send Slack notification based on the given message


def slack_notification(messaggio):
    try:
        # Create HTTP client and make request to Slack API
        http = urllib3.PoolManager()
        response = http.request('POST', WEBHOOK_URL, body=json.dumps(
            {'text': messaggio}), headers={'Content-Type': 'application/json'}, retries=False)
        # Check status code of response
        if response.status == 200:
            # Return True to indicate that the notification was successful
            return True
        else:
            # Return False to indicate that the notification failed
            return False
    except Exception as e:
        # Print the traceback of the exception
        traceback.print_exc()
        # Return False to indicate that the notification failed
        return False


slack_notification(messaggio)
time.sleep(86400)
