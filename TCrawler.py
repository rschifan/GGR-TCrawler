from configparser import RawConfigParser
from pprint import pprint
import requests 
import time 

class TCrawler:
    
    def __init__(self, config_file = "config.ini"):    
        print('TCrawler: __init__')
        self.config_file = config_file
        self.load_config(config_file)

    
    def load_config(self, config_file):
        #Read config.ini file
        config_object = RawConfigParser()
        config_object.read(config_file)

        api_credentials = config_object["API"]
        self.consumer_key = api_credentials['consumer_key']
        self.consumer_secret = api_credentials['consumer_secret']
        self.bearer_token = api_credentials['bearer_token']
        print('loaded account credentials')

        endpoint = config_object["ENDPOINT"]
        self.api_url = endpoint['api_url']
        print('loaded API url: %s' %self.api_url)

        endpoint = config_object["QUERY"]
        self.query = {'query': endpoint['query']}
        print('loaded query: %s' %self.query)

        api_parameters = config_object["PARAMS"]
        self.params = {}
        for current in api_parameters:
            self.params[current] = api_parameters[current]
        print('loaded %d query parameters' %len(api_parameters))
        pprint(self.params)

        crawler = config_object["CRAWLER"]
        self.sleep_time = int(crawler['sleep.time'])
        self.verbose = eval(crawler['verbose'])
        if 'max.requests' in crawler:
            self.max_requests = int(crawler['max.requests'])
        else:
            self.max_requests = None
        
    def set_params(self, params):
        self.params = params
    
    def set_query(self, query):
        self.query = query
        
    def set_api_url(self, api_url):
        self.api_url = api_url


    def create_headers(self):
        headers = {"Authorization": "Bearer {}".format(self.bearer_token)}
        return headers


    def connect_to_endpoint(self, url, headers, params):

        request = requests.Request("GET", url, headers=headers, params=params)
        prepped = request.prepare()

        if self.verbose: 
            print('retrieving: {}'.format(prepped.url))
        
        n_attempts = 0
        while True:
        
            response = requests.Session().send(prepped)

            if response.status_code != 200:
                if n_attempts>3 or response.status_code==400:
                    raise Exception(response.status_code, response.text)
                else:
                    print(f"Exception: {response.status_code} {response.text}\nn_attempts {n_attempts}")                    
                    n_attempts+=1
                    time.sleep(60*n_attempts)
            else:
                return response.json()

    def save(self, json_response):
        pprint(json_response)

    def run(self):
        
        print()
        headers = self.create_headers()
        counter = 0

        while True:

            if self.max_requests and self.max_requests > 0:
                if counter>=self.max_requests:
                    print('Reached max requests limit: {}'.format(self.max_requests))
                    break
            

            json_response = self.connect_to_endpoint(
                self.api_url, 
                headers, 
                {**self.params, **self.query} 
            )
            

            if json_response and 'meta' in json_response:

                print('retrieved %d posts' %json_response['meta']['result_count'] )
                
                self.save(json_response)
                
                print('slowing down')
                time.sleep(self.sleep_time)
                
                if 'next_token' in json_response['meta']:
                    print('retrieving next page (%s)' %json_response['meta']['next_token'] )
                    self.params['next_token'] = json_response['meta']['next_token']
                else:
                    break

                counter += 1
            
            else:
                print('Bad response format: stopping')
                break
        
        print('done.')


if __name__ == "__main__":
    crawler = TCrawler()
    crawler.run()


