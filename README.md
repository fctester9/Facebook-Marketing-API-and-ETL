# Facebook-Marketing-API-and-ETL
An example of pulling data from the Facebook Marketing API and storing it in a database

In facebook.py

1. Enter your database credentials

```python
params = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=XXXXXX;DATABASE=XXXXXX;UID=XXXXXX;PWD=XXXXXX")
```

2. Enter a long-lived Facebook access token with ad_reads permissions

```python
access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
```

3. Tweak the parameters and fields based on [Facebook Documentation](https://developers.facebook.com/docs/marketing-api/insights/parameters) 

```python
params = {'level': 'campaign', 'time_range': {'since': '2018-01-05','until':'2018-09-19'}, 'action_breakdowns':['action_type'], 'breakdowns' : ['publisher_platform']}
fields = ['impressions', 'clicks', 'actions', 'campaign_name', 'spend', 'video_10_sec_watched_actions']
```

4. Enter your desired database name and schema destination

```python
df.to_sql('Enter you table name' , schema='Enter your schema name', con = engine, if_exists='replace', index=False)
```
In multi.py

5. Enter a list of Facebook Ad Account IDs

```python
accounts = ['XXXXXXXX', 'XXXXXXXX']
```

6. Run the multi.py file
