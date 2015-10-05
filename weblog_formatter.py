import pandas as pd
import re
import sys
import os

files = os.listdir('.')
logs = []
for each_file in files:
  if '.log' in each_file:
    logs.append(each_file)

df = pd.DataFrame(columns = ['IP','Date','Request','Response HTTP','Response in bytes','Referer','User Agent'])

counter = 0
for each_log in logs:
  log = open(each_log, 'r')
  for line in log:
    #if counter < 15000:
    try:
      ip = re.search(r'\d{1,255}\.\d{1,255}\.\d{1,255}\.\d{1,255}', line).group()
      # date = line.split('[', 1)[1].split(']')[0]
      date = re.match(r"[^[]*\[([^]]*)\]", line).groups()[0]
      request = line.split('"', 1)[1].split('"')[0]
      response_http = line.split('" ', 1)[1].split(' ')[0]
      response_bytes = line.split('" ')[1].split(' ')[1]
      referer = line.split(' "')[2].replace('"', ' ')
      # user_agent = line.split(' "')[3].replace('"', ' ').replace(',', ' ')
      user_agent = line.split('"')[-2]
      # print user_agent

      # df.append({'IP':str(ip),'Date':str(date), 'Request':str(request), 'Response HTTP':str(response_http), 'Response in bytes':str(response_bytes), 'Referer':str(referer), 'User Agent':user_agent}, ignore_index = True)

      df.loc[len(df)+1]=[ip, date, request, response_http, response_bytes, referer, user_agent]
    
      counter = counter + 1

    # print 'Inserting in df[' + str(len(df)) + ']'
    except KeyboardInterrupt:
      print 'KeyboardInterrupt exception raised. Generating weblogs.csv...'
      df.to_csv('weblogs.csv')
      sys.exit()

    except AttributeError:
      print 'Not possible to identify IP address...'
      pass

df.to_csv('weblogs.csv')
# print df

