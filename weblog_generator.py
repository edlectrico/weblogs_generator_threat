from datetime import datetime
import os
import time
from time import gmtime, strftime
from random import randint, choice
import requests
import glob
import sys
# import pandas as pd

import utils as u

home_page = 'http://www.bbva.es/particulares/index.jsp'

http_responses = [200, 400, 403, 404, 500]

referers = ['http://www.elpais.com/', 
	    'http://www.elmundo.es/', 
	    'http://www.larazon.es/',
	    'http://www.abc.es/',
	    'http://www.cadenaser.com',
	    'http://www.cope.es/',
	    'http://www.expansion.com/',
	    'http://www.eleconomista.es/',
	    'https://www.facebook.com/',
	    'https://www.twitter.com/',
	    'https://www.linkedin.com/'
	   ]
  
suspicious_ips = ['.10.', '.11.', '.12.', '.13.', '.18.', '.19.']

#suspicious_df = pd.DataFrame(columns='IP')

initial_date = datetime.strptime('09/24/2015 12:00 AM', '%m/%d/%Y %I:%M %p')
final_date = datetime.strptime('10/20/2015 11:59 PM', '%m/%d/%Y %I:%M %p')

def main():
  # Get all resources from specified website
  page = requests.get(home_page)
  # tree = html.fromstring(page.text)
  source = page.text
  resources = []
  a = source.split('href="')

  for href in a:
    if ('.html' in href) or ('.jsp' in href):
      resources.append(href.split('"')[0])
  resources = resources[1:]

  user_agents_dir = "user_agents/"
  useragents_list = glob.glob(user_agents_dir + '*.txt')
  all_user_agents = []

  for file in useragents_list:
    all_user_agents.append(open(file, 'r').readlines())

  f = open('out.log', 'w')
  s = open('suspicious.log', 'w')
  
  while True:
    try:
      ip = str(randint(10,255)) + '.' + str(randint(0,255)) + '.' + str(randint(0,255)) + '.' + str(randint(0,255))
      date = str(u.random_date(initial_date, final_date))
      date = date.replace(" ", ":").replace("-", "/").split(' ')[0]
      resource = str(choice(resources))
      request = "GET " + resource
      response = str(u.weighted_choice([	
				(http_responses[0], 90), 
				(http_responses[1], 10), 
				(http_responses[2], 40), 
				(http_responses[3], 30), 
				(http_responses[4], 50)
			     ]))

      response_bytes = str(randint(2000,5000))
      referer = str(u.weighted_choice([
			(referers[0], 20),
                        (referers[1], 40),
                        (referers[2], 50),
                        (referers[3], 30),
                        (referers[4], 30),
                        (referers[5], 20),
                        (referers[6], 50),
                        (referers[7], 40),
                        (referers[8], 40),
                        (referers[9], 15),
                        (referers[10],15),
			]))
      user_agent = str(choice(choice(all_user_agents))).split("\n")[0]

      if process_ip(ip):
        # write in suspicious file
        s.write(ip + ' -' + ' - '  +'[' + date + ']' + ' ' + '"' + request + '"' + ' ' + response + ' ' + response_bytes + ' ' + '"' + referer + '"' + ' ' + '"' + user_agent + '"' + '\n')
      else:
        f.write(ip + ' -' + ' - '  +'[' + date + ']' + ' ' + '"' + request + '"' + ' ' + response + ' ' + response_bytes + ' ' + '"' + referer + '"' + ' ' + '"' + user_agent + '"' + '\n')

    except KeyboardInterrupt:
      print 'KeyboradInterrupt exception raised: Generating out_log...'
      f.write(ip + ' -' + ' - '  +'[' + date + ']' + ' ' + '"' + request + '"' + ' ' + response + ' ' + response_bytes + ' ' + '"' + referer + '"' + ' ' + '"' + user_agent + '"' + '\n')
      sys.exit()
    

def process_ip(ip_add):
  for ip in suspicious_ips:
    if ip in ip_add:
      # print 'Suspicious IP address detected...'
      return True
  return False

if __name__ == "__main__":
  main()

