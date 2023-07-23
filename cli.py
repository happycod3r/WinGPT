import persistence
import openai
import debug as dbg
import stdops
import os


class OpenAIInterface:
     
    def __init__(self) -> None:
        self.stdops = stdops.StdOps()
        self.config = persistence.Persistence()
        self.config.openConfig()
        self.CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
        self.CONFIG_DIR = self.config.getOption("system", "config_dir")
        self.LOGS_DIR = self.config.getOption("system", "logs_dir")
        self.USER_SETTINGS_FILE = self.config.getOption("system", "config_file")
        self.KEY_CONFIG_FILE = self.config.getOption("user", "api_key_path")
        
        self.setAPIKeyPath(self.KEY_CONFIG_FILE)
        
        self.api_key_path = openai.api_key_path # Set during setup.
        self.api_key = self.config.getOption("user", "api_key")
        self.api_base = self.config.getOption("chat", "api_base")
        self.api_type = self.config.getOption("chat", "api_type")
        self.api_version = self.config.getOption("chat", "api_version")
        self.organization = self.config.getOption("user", "organization")
        self.engines = self.getEngines()
        self.engine = self.config.getOption("chat", "chat_engine")
        self.user_defined_filename = None
        self.jsonl_data_file = None
        self.stop_list = None
        self.use_stop_list = self.config.getOption("chat", "use_stop_list")
        
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
        self.frequency_penalty = int(self.config.getOption("chat", "frequency_penalty"))
        self.presence_penalty = int(self.config.getOption("chat", "presence_penalty"))
        self.response = None
        self.response_token_limit = int(self.config.getOption("chat", "response_token_limit"))
        self.response_count = int(self.config.getOption("chat", "response_count"))
        self.best_of = int(self.config.getOption("chat", "best_of"))
        self.request_types = {
            "chat": 0, 
            "images": 1, 
            "audio" : 2, 
            "embeddings": 3, 
            "files": 4, 
            "fine_tuning": 5, 
            "moderations": 6, 
            "build_requests": 7,
            "translation": 8
        }
        self.request_type = int(self.config.getOption("chat", "request_type"))
        self.request = "What's todays date?"
        self.timeout = int(self.config.getOption("chat", "timeout"))
        self.config.saveConfig()
    
        # _data = [
        #     self.api_key_path, 
        #     self.api_key, 
        #     self.api_base, 
        #     self.api_type, 
        #     self.api_version,
        #     self.organization, 
        #     self.engine, 
        #     self.user_defined_filename,
        #     self.jsonl_data_file,
        #     self.stop_list,
        #     self.use_stop_list, 
        #     self.echo, 
        #     self.stream, 
        #     self.save_chat,
        #     self.temperature, 
        #     self.frequency_penalty, 
        #     self.presence_penalty, 
        #     self.response_count,
        #     self.response_token_limit, 
        #     self.best_of, 
        #     self.request_type,
        #     self.request,
        #     self.timeout
        # ] 
    #    dbg.out(_data)
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
        
    def getAPIKeyFromFile(self, api_key_path: str) -> (str | bool): #UNCALLED
        if os.path.exists(api_key_path):
            key = self.stdops.readFromFile(api_key_path)
            if not key:
                return False
            return key
        return False
        
    def getAPIKeyfromConfig(self) -> str:
        self.config.openConfig()
        _api_key = self.config.getOption("user", "api_key")
        self.config.saveConfig()
        return _api_key
    
    def getAPIKey(self) -> str: #UNCALLED
        return openai.api_key
    
    def setAPIKey(self, _api_key: str) -> bool:
        if os.path.exists(self.api_key_path):
            if self.stdops.writeTofile(self.api_key_path, _api_key):
                self.api_key = _api_key
                openai.api_key = self.api_key
                self.config.openConfig()
                self.config.setOption("user", "api_key", _api_key)
                self.config.saveConfig()
                return True
            return False
        return False
                    
    def validateAPIKey(self, api_key: str) -> bool:
        if not (api_key.startswith('sk-') and len(api_key) == 51):
            return False
        else:    
            return True
        
    #//////////// API BASE ////////////
    def getAPIBase(self, _oai: bool = True) -> str:
        if _oai:
            return openai.api_base
        _api_base = self.config.getOption("chat", "api_base")
        return _api_base
        
    def setAPIBase(self, _api_base: str) -> None:
        openai.api_base = self.api_base
        self.config.openConfig()
        self.config.setOption("chat", "api_base", f"{_api_base}")
        self.config.saveConfig()
        self.api_base = _api_base
        
    #//////////// API TYPE ////////////
    def getAPIType(self, _oai: bool = True) -> str:
        if _oai:
            return openai.api_type
        _api_type = self.config.getOption("chat", "api_type")
        return _api_type
    
    def setAPIType(self, _api_type: str) -> None:
        openai.api_type = self.api_type
        self.config.openConfig()
        self.config.setOption("chat", "api_type", f"{_api_type}")
        self.config.saveConfig()
        self.api_type = _api_type
        
    #//////////// API VERSION ////////////
    def getAPIVersion(self, _oai: bool = True) -> str:
        if _oai:
            return openai.api_version
        _api_version = self.config.getOption("chat", "api_version")
        return _api_version
        
    def setAPIVersion(self, _api_version: str) -> None:
        openai.api_version = _api_version
        self.config.openConfig()
        self.config.setOption("chat", "api_verion", f"{_api_version}")
        self.config.saveConfig()
        self.api_version = _api_version
    
    #//////////// ORGANIZATION ////////////
    def getOrganization(self, _oai: bool = True) -> str:
        if _oai:
            return openai.organization
        _organization = self.config.getOption("user", "oragnization")
        return _organization
    
    def setOrganization(self, _organization_id: str) -> None:
        openai.organization = _organization_id
        self.config.openConfig()
        self.config.setOption("user", "organization", f"{_organization_id}")
        self.config.saveConfig()
        self.organization = _organization_id
    
    #//////////// ENGINE ////////////
    def getEngine(self) -> str:
        _engine = self.config.getOption("chat", "chat_engine")
        return _engine
        
    def getEngines(self) -> list:
        model_lst = openai.Model.list()
        _engines = []
        for i in model_lst["data"]:
            _engines.append(i["id"])
        return _engines
    
    def setEngine(self, _engine: str) -> None:
        self.config.openConfig()
        self.config.setOption("chat", "chat_engine", f"{_engine}")
        self.config.saveConfig()
        self.engine = _engine
         
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
         
    #//////////// USE STOP LIST ////////////
    def getUseStopList(self) -> bool:
        _usl = self.config.getOption("chat", "use_stop_list")
        if _usl == "True":
            _usl = True
            return _usl
        _usl = False
        return _usl
    
    def setUseStopList(self, _use_stop_list: bool) -> None:
        self.config.openConfig()
        self.config.setOption("chat", "use_stop_list", _use_stop_list)
        self.config.saveConfig()
        self.use_stop_list = _use_stop_list
    
    #//////////// STOP LIST ////////////
    def getStopList(self) -> list:
        return self.stop_list
        
    def setStopList(self, _stoplist: str) -> None:
        self.stop_list = _stoplist.split()

    #//////////// CHAT ECHO ////////////    
    def getChatEcho(self) -> bool:
        _echo = self.config.getOption("chat", "echo_chat")
        if _echo == "True":
            _echo = True
            return _echo
        _echo = False
        return _echo
        
    def setChatEcho(self, _echo: bool) -> None:
        self.config.openConfig()
        self.config.setOption("chat", "echo_chat", _echo)
        self.config.saveConfig()
        self.echo = _echo
        
    #//////////// CHAT STREAM ////////////
    def getChatStream(self) -> bool:
        _stream = self.config.getOption("chat", "stream_chat")
        if _stream == "True":
            _stream = True
            return _stream
        _stream = False
        return _stream
    
    def setChatStream(self, _stream: bool) -> None:
        self.config.openConfig()
        self.config.setOption("chat", "stream_chat", _stream)
        self.config.saveConfig()
        self.stream = _stream
                
    #//////////// SAVE CHAT TO FILE ////////////
    def saveChat(self, file_path: str = None, content: str = None) -> bool:        
        if os.path.exists(file_path):
            if self.stdops.writeTofile(file_path, content, "a"):
                return True
            return False
        else:
            if self.stdops.writeTofile(file_path, content):
                return True
            return False
        
    def getSaveChat(self) -> bool:
        _save = self.config.getOption("chat", "chat_to_file")
        if _save == "True":
            _save = True
            return _save
        _save = False
        return _save
        
    def setSaveChat(self, _save) -> None:
        self.config.openConfig()
        self.config.setOption("chat", "chat_to_file", _save)
        self.config.saveConfig()
        self.stream = _save
        
    #//////////// CHAT TEMPERATURE ////////////
    def getTemperature(self) -> int:
        _temp = self.config.getOption("chat", "chat_temperature")
        return int(_temp)
    
    def setTemperature(self, _temperature: int) -> bool:
        if isinstance(_temperature, (int, float)):
            self.config.openConfig()
            self.config.setOption("chat", "chat_temperature", _temperature)
            self.config.saveConfig()
            self.temperature = _temperature
            return True
        return False
                        
    #//////////// FREQUENCY PENALTY ////////////
    def getFrequencyPenalty(self) -> (float | int):
        _freq_pen = self.config.getOption("chat", "frequency_penalty")
        return int(_freq_pen)
    
    def setFrequencyPenalty(self, _freq_penalty: (int | float)) -> bool:
        if isinstance(_freq_penalty, int) or isinstance(_freq_penalty, float):
            self.config.openConfig()
            self.config.setOption("chat", "frequency_penalty", _freq_penalty)
            self.config.saveConfig()
            self.frequency_penalty = _freq_penalty
            return True
        return False
    
    #//////////// PRESENCE PENALTY ////////////
    def getPresencePenalty(self) -> (float | int):
        _pres_pen = self.config.getOption("chat", "presence_penalty")
        return int(_pres_pen)
    
    def setPresencePenalty(self, _presence_penalty: (int | float)) -> bool:
        if isinstance(_presence_penalty, int) or isinstance(_presence_penalty, float):
            self.config.openConfig()
            self.config.setOption("chat", "presence_penalty", _presence_penalty)
            self.config.saveConfig()
            self.presence_penalty = _presence_penalty
            return True
        return False
    
    #//////////// RESPONSE COUNT ////////////
    def getResponseCount(self) -> int:
        _r_count = self.config.getOption("chat", "response_count")
        return int(_r_count)
     
    def setResponseCount(self, _response_count: int) -> bool:
        if isinstance(_response_count, int):
            self.config.openConfig()
            self.config.setOption("chat", "response_count", _response_count) 
            self.config.saveConfig()
            self.response_count = _response_count
            return True
        return False
            
    #//////////// RESPONSE TOKEN LIMIT ////////////
    def getResponseTokenLimit(self) -> int:
        _rt_limit = self.config.getOption("chat", "response_token_limit")
        return int(_rt_limit)
    
    def setResponseTokenLimit(self, _response_token_limit: int) -> bool: 
        if isinstance(_response_token_limit, int):
            self.config.openConfig()
            self.config.setOption("chat", "response_token_limit", _response_token_limit)
            self.config.saveConfig()
            self.response_token_limit = _response_token_limit
            return True
        return False
     
    #//////////// BEST OF ////////////
    def getBestOf(self) -> (float | int):
        _best_of = self.config.getOption("chat", "best_of")
        return int(_best_of)
    
    def setBestOf(self, _best_of: (int | float)) -> bool:
        if isinstance(_best_of, int) or isinstance(_best_of, float):
            self.config.openConfig()
            self.config.setOption("chat", "best_of", _best_of)
            self.config.saveConfig()
            self.best_of = _best_of
            return True
        return False

    #//////////// TIMEOUT ////////////
    def getTimeout(self) -> (float | int):
        _timeout = self.config.getOption("chat", "timeout")
        return int(_timeout)
    
    def setTimeout(self, _timeout: (int | float)) -> bool:
        if isinstance(_timeout, int) or isinstance(_timeout, float):
            self.config.openConfig()
            self.config.setOption("chat", "timeout", _timeout)
            self.config.saveConfig()
            self.timeout = _timeout
            return True
        return False
     
    #//////////// REQUEST TYPE ////////////
    def getRequestType(self) -> int:
        _req_type = self.config.getOption("chat", "request_type") 
        return int(_req_type)
    
    def setRequestType(self, _request_type: int) -> bool:
        if isinstance(_request_type, int):
            self.config.openConfig()
            self.config.setOption("chat", "request_type", _request_type)
            self.config.saveConfig()
            self.request_type = _request_type
            return True
        return False

    #//////////// REQUEST ////////////
    def getRequest(self) -> str:
        return self.request

    def setRequest(self, request: str) -> None:
        self.request = request
    
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
                    frequency_penalty=self.frequency_penalty,
                    presence_penalty=self.presence_penalty,
                    best_of=self.best_of,
                    timeout=self.timeout
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
                
