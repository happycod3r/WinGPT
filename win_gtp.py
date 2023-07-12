import openai
import sys
import os
    
class WinGTP:
    
    def __init__(self, api_key_path):
        self.response_token_limit = 200#/minute (default)
        self.response_count = 1 #(default)
        self.engines = [
            ['gtp-4', 8192, '9-2021'],
            ['gtp-4-0613', 8912, '9-2021'],
            ['gtp-4-32k', 32768, '9-2021'],
            ['gtp-4-32k-0613', 32768, '9-2021'],
            ['gpt-3.5-turbo', 4096, '9-2021'],
            ['gpt-3.5-turbo-16k', 16384, '9-2021'],
            ['gpt-3.5-turbo-0613', 4096, '9-2021'],
            ['gpt-3.5-turbo-16k-0613', 16384, '9-2021'],
            ['text-davinci-003', 4097, '06-2021'],
            ['text-davinci-002', 4097, '06-2021'],
            ['code-davinci-002', 8001, '06-2021'],
            ['text-curie-001', 2049, '10-2019'], 
            ['text-babbage-001', 2049, '10-2019'], 
            ['text-ada-001', 2049, '10-2019'],
            ['davinci', 2049, '10-2019'],
            ['curie', 2049, '10-2019'],
            ['babbage', 2049, '10-2019'],
            ['ada', 2049, '10-2019']
        ]
        self.engine = f"{self.engines[8][0]}"
        self.api_key_path = api_key_path
        self.api_key = self.getAPIKey(self.api_key_path)
        self.api_base = openai.api_base
        self.api_type = openai.api_type
        self.api_version = openai.api_version
        self.jsonl_data_file = None
        self.request = 'What\'s todays date?'
        self.response = None
        self.organization = openai.organization
        self.user_defined_filename = None
        openai.api_key_path = self.api_key_path
        openai.api_key = self.api_key

    def writeResonseToFile(msg, f_path):
        if os.path.exists(f_path):
            mode = 'a'
        else:
            mode = 'w'
        try:
            with open(f_path, mode) as file:
                file.write(msg + '\n')
            print("Message appended to the file successfully!")
        except IOError:
            print("An error occurred while appending to the file.")
        
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
    
    def setJSONLDataFile(self, jsonl_file_path):
        self.jsonl_data_file = file_obj = openai.File.create(
            file=open(f'{jsonl_file_path}', 'rb'),
            purpose='fine-tune'
            # model=self.engine,
            # api_key = self.api_key,
            # api_base = self.api_base,
            # api_type = self.api_type,
            # api_version = self.api_version,
            # organization = self.organization,
            # user_provided_filename = self.user_defined_filename,     
        )
        
    def getJSONLDataFile(self):
        return self.jsonl_data_file 
    
    def readJSONLDataFile(self):
        pass
    
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
        if(self.jsonl_data_file == None):
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
                files=[self.jsonl_data_file.id]
            )
        
    def getResponse(self):
        return self.response.choices[0].text.strip()

    def converse(self):
        PRINT_RESPONSES = False
        PRINT_FULL = False
        
        cli_options = [
            'exit', # exit the chat session. 
            '-l',   # Set the response token limit.
            '-e',   # Set the engine. 
            '-r',   # Set the number of reponses
            '-b',   # Set the API base.
            '-t',   # Set the API type.
            '-v',   # Set the api version.
            '-o',   # Set the organization name.
            '-f',   # Set the user defined file name.
            '-j',   # Set the JSONL data file path. 
        ]   
        
        while True:
            user_prompt = input(':>>> ')
            if user_prompt == cli_options[0]:
                print(f'Goodbye! ...')
                sys.exit()
            elif user_prompt == cli_options[1]:
                token_limit = input('Set the max amount of reponse tokens: ')
                self.setResponseTokenLimit(int(token_limit))
                print(f'Token limit set to {self.getResponseTokenLimit()} tokens per response.')
                continue
            elif user_prompt == cli_options[2]:
                engine = input("Set the engine: ")
                self.setEngine(engine)
                print(f'Engine set to {self.getEngine()}')
                continue
            elif user_prompt == cli_options[3]:
                response_count = input("Set the number of reponses: ")
                self.setResponseCount(int(response_count))
                print(f'The number of reponses is set to {self.getResponseCount()}')
                continue
            elif user_prompt == cli_options[4]:
                api_base = input("Set the API base: ")
                self.setAPIBase(str(api_base))
                print(f'The API base is set to {self.getAPIBase()}')
                continue
            elif user_prompt == cli_options[5]:
                api_type = input("Set the API type: ")
                self.setAPIType(str(api_type))
                print(f'The API type is set to {self.getAPIType()}')
                continue
            elif user_prompt == cli_options[6]:
                api_version = input("Set the API version: ")
                self.setAPIVersion(str(api_version))
                print(f'The API version is set to {self.getAPIVersion()}')
                continue
            elif user_prompt == cli_options[7]:
                organization = input("Set the organization name: ")
                self.setOrganization(str(organization))
                print(f'The API base is set to {self.getOrganization()}')
                continue
            elif user_prompt == cli_options[8]:
                user_defined_filename = input("Set a user defined file name: ")
                self.setUserDefinedFileName(str(user_defined_filename))
                print(f'The user defined file name is set to {self.getUserDefinedFileName()}')
                continue
            elif user_prompt == cli_options[9]:
                jsonl_file_path = input("Set a JSONL file: ")
                self.setJSONLDataFile(str(jsonl_file_path))
                print(f'The JSONL file is set to {self.getJSONLDataFile()}')
                continue
            else:
                self.setResponseTokenLimit(self.response_token_limit)
                self.setEngine(self.engine)
                self.setResponseCount(self.response_count)
                self.setRequest(str(user_prompt))
                self.requestData()
                print(self.getResponse())
                
API_KEY_PATH = './.api_key.conf'
newRequest = WinGTP(API_KEY_PATH)
newRequest.converse()
