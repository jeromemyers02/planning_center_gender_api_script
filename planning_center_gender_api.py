import requests
import arrow
import json


# https://api.planningcenteronline.com/oauth/applications to get your planning center application id and secret key
planning_center_activity_id='replace_application_id'               # example 'c743bf00cbhh13d55b9649948796574fbebcfab'
planning_center_secret='replace_with_secret'        # example  'baf8544a1c23423aa386585fs0d41eabbcef2b1e32cdc9ae89'

# https://gender-api.com/ to create a user and get a gender API
gender_api_key='replace with gender api key' # example 'qGKDok23Sasfwtghq75ZLe'

def gender_api(name):
    # call gender api
    gender_url='https://gender-api.com/get?name={}&key={}'.format(name,gender_api_key)
    response=requests.get(gender_url)
    return json.loads(response.text)

def getPlanningCenter(url):
    # get from planning center
    stuff2= requests.get(url, auth=(planning_center_activity_id, planning_center_secret))
    data=json.loads(stuff2.text)
    return data

def updatePlanningCenter(url,jsonData):
    # update planning center
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    data=requests.patch(url,auth=(planning_center_activity_id, planning_center_secret), data=json.dumps(jsonData),headers=headers )
    return data


def gender():
    gender_url='https://api.planningcenteronline.com/people/v2/people?order=gender&per_page=100'
    data=getPlanningCenter(gender_url)
    for row in data['data']:
        if row['type']=='Person'and row['attributes']['gender']==None:
            if len(row['attributes']['first_name'])>=3:
                genderResponse=gender_api(row['attributes']['first_name'])
                if int(genderResponse["accuracy"]) > 70:
                    if genderResponse["gender"]=="male":
                        genderType='M'
                    elif genderResponse['gender']=="female":
                        genderType='F'
                    jsonData={"data":{"type":"Person","id":row['id'],"attributes":{"gender":genderType}}}
                    post_url='https://api.planningcenteronline.com/people/v2/people/{}'.format(row['id'])
                    response=updatePlanningCenter(post_url,jsonData)
                    print(response.status_code,genderType,'https://people.planningcenteronline.com/people/{}'.format(row['id']))
                else:
                    print ('{}% For {}'.format(genderResponse['accuracy'],row['attributes']['first_name']),'https://people.planningcenteronline.com/people/{}'.format(row['id']))
            else:
                print('{} does not have three characters in its first name and will not be evaluated using the gender API. Manual evaluation is expected.'.format(row['attributes']['first_name']),'https://people.planningcenteronline.com/people/{}'.format(row['id']))

        else:
            print(row['attributes']['first_name'],row['attributes']['gender'],'https://people.planningcenteronline.com/people/{}'.format(row['id']))

gender()
