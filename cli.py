import persistence
import openai
import os

class OpenAIInterface:
     
    def __init__(self) -> None:
        self.config = persistence.Persistence()
        self.config.openConfig()
        self.CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
        self.CONFIG_DIR = self.config.getOption("system", "config_dir")
        self.LOGS_DIR = self.config.getOption("system", "logs_dir")
        self.USER_SETTINGS_FILE = self.config.getOption("system", "config_file")
        self.KEY_CONFIG_FILE = self.config.getOption("user", "api_key_path")
        self.USE_STOPLIST = False
        
        self.setAPIKeyPath(self.KEY_CONFIG_FILE)
        
        self.api_key_path = self.KEY_CONFIG_FILE
        openai.api_key_path = self.KEY_CONFIG_FILE
        openai.api_key = self.config.getOption("user", "api_key")
        self.api_key = openai.api_key
        
        self.api_base = openai.api_base
        self.api_type = openai.api_type
        self.api_version = openai.api_version
        
        self.engines = self.getEngines()
        self.engine = self.config.getOption("chat", "chat_engine")
        self.jsonl_data_file = None
        self.echo = False
        self.stream = False
        self.request_types = {
            "chat": 0, 
             "images": 1, 
            "audio" : 2, 
            "embeddings": 3, 
            "files": 4, 
            "fine_tuning": 5, 
            "moderations": 6, 
            "build_requests": 7
        }
        self.request_type = self.request_types["chat"]
        self.request = "What's todays date?"
        self.response = None
        self.response_token_limit = 16 #/minute (default)
        self.response_count = 1 #(default)
        self.organization = self.config.getOption("user", "organization")
        self.user_defined_filename = None
        self.temps = {"low":0, "medium":1, "high":2}
        self.temperature = self.temps["medium"]
        self.stop_list = None
        
        self.config.saveConfig()
    
    #//////////// API KEY PATH ////////////
    def getAPIKeyPath(self) -> str:
        return openai.api_key_path

    def setAPIKeyPath(self, api_key_path: str) -> bool:
        if os.path.exists(api_key_path):
            self.api_key_path = api_key_path
            openai.api_key_path = api_key_path
            return True
        return False
        
    #//////////// API KEY ////////////
    def getAPIKey(self, api_key_path: str) -> str:
        if os.path.exists(api_key_path):
            try:
                with open(api_key_path, 'r') as file:
                    key = file.read()
                    file.close()
                    return key
            except FileNotFoundError:
                print("API key not found")
            except IOError:
                print("An error occurred while reading the api key configuration file.")
            except Exception as e:
                print("An unexpected error occurred while trying to read the api key configuration file", repr(e))

    def setAPIKey(self, api_key: str) -> bool:
        if os.path.exists(self.api_key_path):
            try:
                with open(self.api_key_path, 'w') as file:
                    file.write(api_key)
                    file.close()
                    self.api_key = api_key
                    openai.api_key = self.api_key
                    return True
            except FileNotFoundError:
                print("API key file not found")
                return False
            except IOError:
                print("An error occurred while setting the api key configuration file.")
                return False
            except Exception as e:
                print("An unexpected error occurred while trying to set the api key configuration file", str(e))
                return False
    
    def validateAPIKey(self, api_key: str) -> bool:
        if not (api_key.startswith('sk-') and len(api_key) == 51):
            return False
        else:    
            return True
        
    #//////////// API BASE ////////////
    def getAPIBase(self) -> str:
        return openai.api_base
    
    def setAPIBase(self, api_base: str) -> None:
        self.api_base = api_base
        openai.api_base = self.api_base
        
    #//////////// API TYPE ////////////
    def getAPIType(self) -> str:
        return openai.api_type
    
    def setAPIType(self, api_type: str) -> None:
        self.config.openConfig()
        self.config.setOption("chat", "api_type", f"{api_type}")
        self.api_type = api_type = self.config.getOption("chat", "api_type")
        openai.api_type = self.api_type
        
    #//////////// API VERSION ////////////
    def getAPIVersion(self) -> str:
        return openai.api_version
    
    def setAPIVersion(self, api_version: str) -> None:
        self.api_version = api_version
        openai.api_version = self.api_version
        
      #//////////// ENGINE ////////////
    
    #//////////// ENGINE ////////////
    def getEngine(self) -> str:
        return self.engine

    def getEngines(self) -> list:
        model_lst = openai.Model.list()
        _engines = []
        for i in model_lst["data"]:
            _engines.append(i["id"])
        return _engines
    
    def setEngine(self, engine: str) -> None:
        self.config.openConfig()
        self.config.setOption("chat", "chat_engine", f"{engine}")
        self.engine = self.config.getOption("chat", "chat_engine")
        self.config.saveConfig()
         
    #//////////// ORGANIZATION ////////////
    def getOrganization(self) -> str:
        return self.organization
    
    def setOrganization(self, organization_id: str) -> None:
        self.config.openConfig()
        self.config.setOption("user", "organization", f"{organization_id}")
        self.organization = self.config.getOption("user", "organization")
        self.config.saveConfig()
        
    #//////////// USER DEFINED FILE NAME ////////////
    def getUserDefinedFileName(self) -> str:
        return self.user_defined_filename
    
    def setUserDefinedFileName(self, file_name: str) -> None:
        self.user_defined_filename = file_name

    #//////////// JSONL DATA FILE ////////////
    def getJSONLDataFile(self):
        return self.jsonl_data_file 

    def setJSONLDataFile(self, jsonl_file_path: str) -> bool:
        """ Sets a jsonl data file. Need to look into this more before fully implementing anything.            
        Args:
            jsonl_file_path (str): _description_

        Returns:
            bool: Returns True if operation was successful otherwise False
        """
        if os.path.exists(jsonl_file_path):
            
            self.jsonl_data_file = file_obj = openai.File.create(
                file=open(f'{jsonl_file_path}', 'rb'),
                purpose='fine-tune'
                # model=self.engine,
                # api_key=self.api_key,
                # api_base=self.api_base,
                # api_type=self.api_type,
                # api_version=self.api_version,
                # organization=self.organization,
                # user_provided_filename=self.user_defined_filename,     
            )
            return True
        return False
    
    def readJSONLDataFile(self) -> None:
        pass

    #//////////// REQUEST ////////////
    def getRequest(self) -> str:
        return self.request

    def setRequest(self, request: str) -> None:
        self.request = request
    
    def setRequestType(self, request_type: int) -> None:
        self.request_type = request_type
        if request_type == 0:
            pass
        elif request_type == 1:
            pass
        elif request_type == 2:
            pass
        elif request_type == 3:
            pass
        elif request_type == 4:
            pass
        elif request_type == 5:
            pass
        elif request_type == 6:
            pass
        elif request_type == 7:
            pass
        elif request_type == 8:
            pass
        elif request_type == 9:
            pass
        else:
            # default
            pass
        
    def requestData(self) -> None: 
        _respone = None
        try:
            if self.request_type == 0:
                _response = openai.Completion.create(
                    engine=str(self.engine),
                    prompt=str(self.request),
                    max_tokens=int(self.response_token_limit),
                    temperature=int(self.temperature),
                    n=int(self.response_count),
                    stream=bool(self.stream),
                    echo=bool(self.echo),
                    stop=self.stop_list,
                    frequency_penalty=0,
                    presence_penalty=0,
                    best_of=1,
                    timeout=None
                )
            
            self.response = _response
        except openai.APIError:
            print("OpenAI API Error")
        except openai.OpenAIError:
            print("OpenAI Error")
        
    #//////////// RESPONSE ////////////
    def getResponse(self) -> str:
        response = self.response.choices[0].text.strip() 
        return response
    
    #//////////// RESPONSE TOKEN LIMIT ////////////
    def getResponseTokenLimit(self) -> int:
        return self.response_token_limit
    
    def setResponseTokenLimit(self, response_token_limit: int) -> None: 
        self.response_token_limit = response_token_limit
     
    #//////////// RESPONSE COUNT ////////////
    def getResponseCount(self) -> int:
        return self.response_count
     
    def setResponseCount(self, response_count: int) -> None: 
        self.response_count = response_count
        
    #//////////// CHAT TEMPERATURE ////////////
    def setTemperature(self, _temperature: int) -> None:
        if isinstance(_temperature, (int, float)):
            self.temperature = _temperature
        
    def getTemperature(self) -> int:
        return self.temperature
        
    #//////////// STOP LIST ////////////
    def setStopList(self, _stoplist: str) -> None:
        self.stop_list = _stoplist.split()
    
    def getStopList(self) -> list:
        return self.stop_list
    
    #//////////// CHAT ECHO ////////////    
    def setChatEcho(self, echo: bool) -> None:
        self.echo = echo
        
    def getChatEcho(self) -> bool:
        return self.echo
        
    #//////////// CHAT STREAM ////////////
    def setChatStream(self, stream: bool) -> None:
        self.stream = stream
        
    def getChatStream(self) -> bool:
        return self.stream
        
    #//////////// SAVE CHAT TO FILE ////////////
    def saveChat(self, file_path: str = None, content: str = None) -> bool:
        try:
            if os.path.exists(file_path):
                with open(f"{file_path}", "a") as file:
                    file.write(content)
                    file.close()
                return True
            else:
                with open(f"{file_path}", "x") as file:
                    file.write(content)
                    file.close()
                    return True
        except IOError:
            return False
        except Exception as e:
            return False
        
    #//////////// UTILITY METHODS ////////////
    def _help(self) -> None:
        """
            All available WinGTP Interface options:
            
            exit                      - exit the chat session.
            -l                        - Set the response token limit.
            -e                        - Set the engine. 
            -r                        - Set the number of reponses
            -b                        - Set the API base.
            -t                        - Set the API type.
            -v                        - Set the api version.
            -o                        - Set the organization name.
            -f                        - Set the user defined file name.
            -j                        - Set the JSONL data file path.
            help                      - Prints this message. 
            clear                     - Clear the output box and command entry.
            theme <Light|Dark|System> - Switch between themes.
            temp                      - Set the output temperature.
        """
    
    def greetUser(self, user: str, key_path: str) -> str:
        if os.path.exists(key_path):
            try:
                self.setAPIKeyPath(key_path)
                self.setResponseTokenLimit(self.response_token_limit)
                self.setEngine(self.engine)
                self.setResponseCount(self.response_count)
                self.setRequest(f'Hi I\'m {user}.')
                self.requestData()
                greeting = self.getResponse()
            except openai.APIError:
                print("OpenAI API Error!")
            except openai.OpenAIError:
                print("OpenAI Error!")
            return greeting
                

