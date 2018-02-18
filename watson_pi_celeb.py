import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights

def analyze(handle):

  twitter_consumer_key = 'rykNr9mmDA2ivJ0ER2gGi6cfk'
  twitter_consumer_secret = 't7ZHC9yp0faXr3rDONpWnHnT6eTQAIeDmDV7y2Dz7ilhBilZ89'
  twitter_access_token = '922168537086681088-oLF3OxVY5gFyNtWpwLTY2uPCbo8DwHi'
  twitter_access_secret = 'L3tF40kuO2195VTLfP4jAMukNNtQI6qEIz0fsBc9adzOw'
  twitter_api = twitter.Api(consumer_key=twitter_consumer_key,
                  consumer_secret=twitter_consumer_secret,
                  access_token_key=twitter_access_token,
                  access_token_secret=twitter_access_secret)
  statuses = twitter_api.GetUserTimeline(screen_name=handle, count=200, include_rts=False)
  text = "" 
  for s in statuses:
	    if (s.lang =='en'):
    			text += s.text.encode('utf-8')
          
  pi_username = 'ffa67b47-955e-4208-984b5e198712d137'
  pi_password='0wWb4HEg2YsG'
  personality_insights = PersonalityInsights(username=pi_username, password=pi_password)

  pi_result = personality_insights.profile(text)
  return pi_result

def flatten(orig):
    data = {}
    for c in orig['tree']['children']:
        if 'children' in c:
            for c2 in c['children']:
                if 'children' in c2:
                    for c3 in c2['children']:
                        if 'children' in c3:
                            for c4 in c3['children']:
                                if (c4['category'] == 'personality'):
                                    data[c4['id']] = c4['percentage']
                                    if 'children' not in c3:
                                        if (c3['category'] == 'personality'):
                                                data[c3['id']] = c3['percentage']
    return data
  
def compare(dict1, dict2):
	compared_data = {}
	for keys in dict1:
    		if dict1[keys] != dict2[keys]:
			compared_data[keys] = abs(dict1[keys] - dict2[keys])
	return compared_data

user_handle = "@realDonaldTrump"
celebrity_handle = "@BarackObama"

user_result = analyze(user_handle)
celebrity_result = analyze(celebrity_handle)

#Flatten the results from the Watson PI API
user = flatten(user_result)
celebrity = flatten(celebrity_result)

#Compare the results of the Watson PI API by calculating the distance between traits
compared_results = compare(user,celebrity)

sorted_result = sorted(compared_results.items(), key=operator.itemgetter(1))

for keys, value in sorted_result[:5]:
    print keys,
    print(user[keys]),
    print ('->'),
    print (celebrity[keys]),
    print ('->'),
    print (compared_results[keys])
