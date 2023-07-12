import openai
import sys
    
class WinGTP:
    
    def __init__(self, api_key_path):
        self.response_token_limit = 200#/minute (default)
        self.response_count = 1 #(default)
        self.engine = 'text-davinci-003'
        self.api_key_path = api_key_path
        self.api_key = self.getAPIKey(self.api_key_path)
        self.api_base = openai.api_base
        self.api_type = openai.api_type
        self.api_version = openai.api_version
        self.data_file = None
        self.request = 'What\'s todays date?'
        self.response = None
        self.organization = openai.organization
        self.user_defined_filename = None
        openai.api_key_path = self.api_key_path
        openai.api_key = self.api_key
    
    def setAPIBase(self, api_base):
        self.api_base = api_base
        openai.api_base = self.api_base
        
    def getAPIBase(self):
        return openai.api_base
    
    def setAPIType(self, api_type):
        self.api_type = api_type
        openai.api_type = self.api_type
        
    def getAPIType(self):
        return openai.api_type
    
    def setAPIVersion(self, api_version):
        self.api_version = api_version
        openai.api_version = self.api_version
        
    def getAPIVersion(self):
        return openai.api_version
    
    def setOrganization(self, organization):
        self.organization = organization
        openai.organization = self.organization
        
    def getOrganization(self):
        return openai.organization
    
    def setUserDefinedFileName(self, file_name):
        self.user_defined_filename = file_name
        
    def getUserDefinedFileName(self):
        return self.user_defined_filename
        
    def setAPIKeyPath(self, api_key_path):
        self.api_key_path = api_key_path
        openai.api_key_path = self.api_key_path
        
    def getAPIKeyPath(self):
        return openai.api_key_path
        
    def setAPIKey(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key
        
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
    
    def setDataFile(self, jsonl_file_path):
        self.data_file = file_obj = openai.File.create(
            file=open(f"{jsonl_file_path}", 'rb'),
            purpose='fine-tune',
            model=self.engine,
            api_key = self.api_key,
            api_base = self.api_base,
            api_type = self.api_type,
            api_version = self.api_version,
            organization = self.organization,
            user_provided_filename = self.user_defined_filename,     
        )
        
    def getDataFile(self):
        return self.data_file 
    
    def readDataFile(self):
        return None
    
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
        if(self.data_file == None):
            self.response = openai.Completion.create(
                engine=f"{self.engine}",                # The model being used.
                prompt=f"{self.request}",               # The input.
                max_tokens=self.response_token_limit,   # Max tokens allowed in each response.
                n=self.response_count,                  # Number of responses 
            )
        else:
            self.response = openai.Completion.create(
                engine=f"{self.engine}",                # The model being used.
                prompt=f"{self.request}",               # The input.
                max_tokens=self.response_token_limit,   # Max tokens allowed in each response.
                n=self.response_count,                  # Number of responses 
                files=[self.data_file.id]
            )
        
    def getResponse(self):
        return self.response.choices[0].text.strip()

    def converse(self):
        while True:
            user_prompt = input(':>>> ')
            if user_prompt == 'exit':
                print(f'Goodbye! ...')
                sys.exit()
            else:
                REQUEST = str(user_prompt)
                RESPONSE_TOKEN_LIMIT = 200
                RESPONSE_COUNT = 1
                ENGINE = 'text-davinci-003'
                self.setResponseTokenLimit(RESPONSE_TOKEN_LIMIT)
                self.setEngine(ENGINE)
                self.setResponseCount(RESPONSE_COUNT)
                self.setRequest(REQUEST)
                self.requestData()
                print(self.getResponse())
                
API_KEY_PATH = './.api_key.conf'
newRequest = WinGTP(API_KEY_PATH)
newRequest.converse()
