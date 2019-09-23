# Copyright 2014 Facebook, Inc.

# You are hereby granted a non-exclusive, worldwide, royalty-free license to
# use, copy, modify, and distribute this software in source code or binary
# form for use in connection with the web services and APIs provided by
# Facebook.

# As with any software that integrates with the Facebook platform, your use
# of this software is subject to the Facebook Developer Principles and
# Policies [http://developers.facebook.com/policy/]. This copyright notice
# shall be included in all copies or substantial portions of the software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.


from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adreportrun import AdReportRun
from facebook_business.api import FacebookAdsApi
from io import StringIO
import time
import json
import requests
import sqlalchemy
import urllib
import pandas as pd
import sys

def main(arg1):
    #initiate SQL Engine
    params = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=XXXXXX;DATABASE=XXXXXX;UID=XXXXXX;PWD=XXXXXX")
    engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

    #Set long term FB access token and request parameters and fields. Refer to https://developers.facebook.com/docs/marketing-api/insights/parameters for custom requirements.
    access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    params = {'level': 'campaign', 'time_range': {'since': '2019-01-05','until':'2019-09-19'}, 'action_breakdowns':['action_type'], 'breakdowns' : ['publisher_platform']}
    fields = ['impressions', 'clicks', 'actions', 'campaign_name', 'spend', 'video_10_sec_watched_actions']

    #initiate Facebook session 
    FacebookAdsApi.init(access_token=access_token)

    #Takes Facebook Ad Account ID passed as an argument from multi.py. Runs the reporting job asynchronously.
    account = AdAccount('act_' + str(arg1))
    i_async_job = account.get_insights(fields=fields, params=params, is_async=True)



    #Waiting for the job to complete
    while True:
        job = i_async_job.api_get()
        print("Percent done: " + str(job[AdReportRun.Field.async_percent_completion]))
        time.sleep(1)
        if job[AdReportRun.Field.async_status] == 'Job Completed':
            print("Done!")
            break

    #Fetching resulting Job ID
    reportid = json.loads(str(i_async_job).replace('\n', '').replace('<AdReportRun> ', ''))
    report_id = reportid['report_run_id']

    #Fetching the response in csv format after the job has completed
    response = requests.get('https://www.facebook.com/ads/ads_insights/export_report/?report_run_id=' + report_id + '&name=myreport&format=csv&locale=en_GB&access_token=' + access_token)

    #Loading the result in a pandas data frame
    response = StringIO(response.text)
    df = pd.read_csv(response, encoding='utf8')

    #Uncomment to retrieve data as a flat file.
    ##print(df)
    ##f = open(report_id + '.csv','w', encoding="utf-8")
    ##f.write(response.text) 
    ##
    ##f.close()

    #Replacing NAs with 0s and importing the dataframe to a database table
    df = df.fillna(0)
    df.to_sql('Enter you table name' , schema='Enter your schema name', con = engine, if_exists='replace', index=False)


if __name__ == "__main__":
    main(sys.argv[1])

