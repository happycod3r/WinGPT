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
        
        self.USE_STOPLIST = self.config.getOption("chat", "use_stop_list")
        
        self.setAPIKeyPath(self.KEY_CONFIG_FILE)
        
        self.api_key_path = openai.api_key_path
        self.api_key = openai.api_key
        self.api_base = openai.api_base
        self.api_type = openai.api_type
        self.api_version = openai.api_version
        self.organization = openai.organization
        self.engines = self.getEngines()
        self.engine = self.config.getOption("chat", "chat_engine")
        self.user_defined_filename = None
        self.jsonl_data_file = None
        self.stop_list = None
        
        _echo = self.config.getOption("chat", "echo_chat") 
        if _echo == "False": self.echo = False
        else: self.echo = True
        
        _stream = self.config.getOption("chat", "stream_chat") 
        if _stream == "False": self.stream = False
        else: self.stream = True
        
        _save = self.config.getOption("chat", "chat_to_file") 
        if _save == "False": self.save_chat = False
        else: self.save_chat = True
        
        self.temps = {"low":0, "medium":1, "high":2}
        self.temperature = int(self.config.getOption("chat", "chat_temperature"))
        self.response = None
        self.response_token_limit = int(self.config.getOption("chat", "response_token_limit"))
        self.response_count = int(self.config.getOption("chat", "response_count"))
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
        self.request_type = int(self.config.getOption("chat", "request_type"))
        self.request = "What's todays date?"
        
        self.config.saveConfig()
   
    #//////////// API KEY ////////////
    def getAPIKeyPath(self) -> str:
        self.config.openConfig()
        _path = self.config.getOption("user", "api_key_path")
        self.config.saveConfig()
        return _path

    def setAPIKeyPath(self, _api_key_path: str) -> bool:
        if os.path.exists(_api_key_path):
            openai.api_key_path = _api_key_path
            self.config.openConfig()
            self.config.setOption("user", "api_key_path", f"{_api_key_path}")
            self.api_key_path = openai.api_key_path
            return True
        return False
        
    def getAPIKeyFromFile(self, api_key_path: str) -> str:
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

    def getAPIKeyfromConfig(self) -> str:
        self.config.openConfig()
        _api_key = self.config.getOption("user", "api_key")
        self.config.saveConfig()
        return _api_key
    
    def getAPIKey(self) -> str:
        return openai.api_key
    
    def setAPIKey(self, _api_key: str) -> bool:
        if os.path.exists(self.api_key_path):
            try:
                with open(self.api_key_path, 'w') as file:
                    file.write(_api_key)
                    file.close()
                    self.api_key = _api_key
                    openai.api_key = self.api_key
                    self.config.openConfig()
                    self.config.setOption("user", "api_key", _api_key)
                    self.config.saveConfig()
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
    
    def setAPIBase(self, _api_base: str) -> None:
        openai.api_base = self.api_base
        self.config.openConfig()
        self.config.setOption("chat", "api_base", f"{_api_base}")
        self.api_base = self.config.getOption("chat", "api_base")
        self.config.saveConfig()
        
    #//////////// API TYPE ////////////
    def getAPIType(self) -> str:
        return openai.api_type
    
    def setAPIType(self, _api_type: str) -> None:
        openai.api_type = self.api_type
        self.config.openConfig()
        self.config.setOption("chat", "api_type", f"{_api_type}")
        self.api_type = self.config.getOption("chat", "api_type")
        self.config.saveConfig()
        
    #//////////// API VERSION ////////////
    def getAPIVersion(self) -> str:
        return openai.api_version
    
    def setAPIVersion(self, _api_version: str) -> None:
        openai.api_version = _api_version
        self.config.openConfig()
        self.config.setOption("chat", "api_verion", f"{_api_version}")
        self.api_version = self.config.getOption("chat", "api_version")
        self.config.saveConfig()
    
    #//////////// ENGINE ////////////
    def getEngine(self) -> str:
        return self.engine

    def getEngines(self) -> list:
        model_lst = openai.Model.list()
        _engines = []
        for i in model_lst["data"]:
            _engines.append(i["id"])
        return _engines
    
    def setEngine(self, _engine: str) -> None:
        self.config.openConfig()
        self.config.setOption("chat", "chat_engine", f"{_engine}")
        self.engine = _engine
        self.config.saveConfig()
         
    #//////////// ORGANIZATION ////////////
    def getOrganization(self) -> str:
        return openai.organization
    
    def setOrganization(self, _organization_id: str) -> None:
        openai.organization = _organization_id
        self.config.openConfig()
        self.config.setOption("user", "organization", f"{_organization_id}")
        self.organization = _organization_id
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
        
    def requestData(self) -> None: 
        _respone = None
        try:
            if self.request_type == 0:
                _response = openai.Completion.create(
                    engine=self.engine,
                    prompt=self.request,
                    max_tokens=self.response_token_limit,
                    temperature=self.temperature,
                    n=self.response_count,
                    stream=self.stream,
                    echo=self.echo,
                    stop=self.stop_list,
                    frequency_penalty=0,
                    presence_penalty=0,
                    best_of=1,
                    timeout=None
                )
            elif self.request_type == 1:
                pass
            elif self.request_type == 2:
                pass
            elif self.request_type == 3:
                pass
            elif self.request_type == 4:
                pass
            elif self.request_type == 5:
                pass
            elif self.request_type == 6:
                pass
            elif self.request_type == 7:
                pass
            elif self.request_type == 8:
                pass
            elif self.request_type == 9:
                pass
            
            self.response = _response
        except openai.APIError:
            print("OpenAI API Error")
        except openai.OpenAIError:
            print("OpenAI Error")
        except Exception as e:
            print(repr(e))
        
    #//////////// RESPONSE ////////////
    def getResponse(self) -> str:
        response = self.response.choices[0].text.strip() 
        return response
    
    #//////////// RESPONSE TOKEN LIMIT ////////////
    def getResponseTokenLimit(self) -> int:
        return self.response_token_limit
    
    def setResponseTokenLimit(self, _response_token_limit: int) -> bool: 
        if isinstance(_response_token_limit, int):
            self.config.openConfig()
            self.config.setOption("chat", "response_token_limit", _response_token_limit)
            self.response_token_limit = _response_token_limit
            self.config.saveConfig()
            return True
        return False
     
    #//////////// RESPONSE COUNT ////////////
    def getResponseCount(self) -> int:
        return self.response_count
     
    def setResponseCount(self, _response_count: int) -> bool:
        if isinstance(_response_count, int):
            self.config.openConfig()
            self.config.setOption("chat", "response_count", _response_count) 
            self.response_count = _response_count
            self.config.saveConfig()
            return True
        return False
            
    #//////////// CHAT TEMPERATURE ////////////
    def getTemperature(self) -> int:
        return self.temperature
    
    def setTemperature(self, _temperature: int) -> bool:
        if isinstance(_temperature, (int, float)):
            self.config.openConfig()
            self.config.setOption("chat", "chat_temperature", _temperature)
            self.temperature = _temperature
            self.config.saveConfig()
            return True
        return False
                    
    #//////////// STOP LIST ////////////
    def getStopList(self) -> list:
        return self.stop_list

    def setStopList(self, _stoplist: str) -> None:
        self.stop_list = _stoplist.split()
    
    #//////////// CHAT ECHO ////////////    
    def getChatEcho(self) -> bool:
        return self.echo
    
    def setChatEcho(self, _echo: bool) -> None:
        self.config.openConfig()
        self.config.setOption("chat", "echo_chat", _echo)
        self.echo = _echo
        self.config.saveConfig()
        
    #//////////// CHAT STREAM ////////////
    def getChatStream(self) -> bool:
        return self.stream
    
    def setChatStream(self, _stream: bool) -> None:
        self.config.openConfig()
        self.config.setOption("chat", "stream_chat", _stream)
        self.stream = _stream
        self.config.saveConfig()
                
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
        
    def setSaveChat(self, _save):
        self.config.openConfig()
        self.config.setOption("chat", "chat_to_file", _save)
        self.stream = _save
        self.config.saveConfig()
        
    def getSaveChat(self) -> bool:
        self.config.openConfig()
        _save = self.config.getOption("chat", "chat_to_file")
        self.config.saveConfig()
        return _save
        
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
                
