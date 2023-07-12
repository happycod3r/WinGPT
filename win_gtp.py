import openai
import sys
    
class WinGTP:
    
    def __init__(self, api_key_path):
        self.response_token_limit = 200#/minute (default)
        self.response_count = 1 #(default)
        self.engine = 'text-davinci-003'
        self.api_key_path = api_key_path
        self.api_key = self.getAPIKey(self.api_key_path)
        self.request = 'What\'s todays date?'
        self.response = None
        openai.api_key_path = self.api_key_path
        # openai.api_key = self.api_key
        
    def getAPIKeyPath(self):
        return self.api_key_path
    
    def setAPIKeyPath(self, api_key_path):
        self.api_key_path = api_key_path
        
    def setAPIKey(self, api_key):
        self.api_key = api_key
        
    def getAPIKey(self, api_key_path):
        try:
            with open(api_key_path, 'r') as file:
                key = file.read()
                file.close()
        except FileNotFoundError:
            print("API key not found")
        except IOError:
            print("An error occurred while reading the api key configuration file.")
        except Exception as e:
            print("An unexpected error occurred while trying to read the api key configuration file", str(e))
        
        return key
        
    def setEngine(self, engine):
        self.engine = engine
        
    def getEngine(self):
        return self.engine
    
    def setRequest(self, request):
        self.request = request
        
    def getRequest(self):
        return self.request
   
    def setResponseTokenLimit(self, response_token_limit):
        self.response_token_limit = response_token_limit
        
    def getResponseTokenLimit(self):
        return self.response_token_limit
     
    def getResponseCount(self):
         return self.response_count
    
    def setResponseCount(self, response_count):
        self.response_count = response_count
        
    def requestData(self):
        response = openai.Completion.create(
            engine=f"{self.engine}",                # The model being used.
            prompt=f"{self.request}",               # The input.
            max_tokens=self.response_token_limit,   # Max tokens allowed in each response.
            n=self.response_count,                  # Number of responses 
        )
        self.response = response
        
    def getResponse(self):
        return self.response.choices[0].text.strip()
    
REQUEST = "How do you write a function in javascript?"
API_KEY_PATH = './.api_key.conf'
RESPONSE_TOKEN_LIMIT = 200
RESPONSE_COUNT = 1
ENGINE = 'text-davinci-003'

newRequest = WinGTP(API_KEY_PATH)
newRequest.setEngine(ENGINE)
print("//////////////// WinGTP ////////////////")
print("----------------------------------------")
print("Engine:")
print(newRequest.getEngine())
newRequest.setResponseTokenLimit(RESPONSE_TOKEN_LIMIT)
print("----------------------------------------")
print("Response token limit:")
print(newRequest.getResponseTokenLimit())
newRequest.setResponseCount(RESPONSE_COUNT)
print("----------------------------------------")
print("Engine:")
print(newRequest.getResponseCount())
newRequest.setRequest(REQUEST)
print("----------------------------------------")
print("Request:")
print(newRequest.getRequest())
newRequest.requestData()
print("----------------------------------------")
print("Response:")
print(newRequest.getResponse())
print("\n")
