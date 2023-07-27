import paths
import modules.persistence as persistence
import openai
import modules.debug as dbg
import modules.stdops as stdops
import os
import modules.logger as logger

class OpenAIInterface:
     
    def __init__(self) -> None:
        self.stdops = stdops.StdOps()
        self.log = logger.LogManager()
        self.config = persistence.Persistence()
        self.config.openConfig()
        
        self.CURRENT_PATH = paths.CURRENT_PATH
        self.CONFIG_DIR = paths.CONFIG_DIR
        self.LOGS_DIR = paths.LOGS_DIR
        self.TMP_DIR = paths.TMP_DIR
        self.USER_SETTINGS_FILE = paths.USER_SETTINGS_FILE
        self.KEY_CONFIG_FILE = paths.KEY_CONFIG_FILE
        
        self.setAPIKeyPath(self.KEY_CONFIG_FILE)
        
        self.username = self.config.getOption("user", "username")
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
        
        self.temps = {"low":0, "med_low":1, "medium":2, "med_high":3, "high":4}
        self.temperature = self.config.getOption("chat", "chat_temperature")
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
            "translation": 8,
            "sentement": 9,
            "qa": 10,
            "summarization": 11,
            "code_gen": 12,
            "edits": 13
        }
        self.request_type = int(self.config.getOption("chat", "request_type"))
        self.request = "What's todays date?"
        self.timeout = int(self.config.getOption("chat", "timeout"))
        self.use_img_edit = int(self.config.getOption("image_requests", "use_edit"))
        self.use_img_var = int(self.config.getOption("image_requests", "use_variation"))
        self.use_img_new = int(self.config.getOption("image_requests", "use_new"))
        self.image_response_format = self.config.getOption("image_requests", "response_format")
        self.audio_file = self.config.getOption("audio_transcription", "audio_file")
        self.instruction = self.config.getOption("edits", "instruction")
        self.config.saveConfig()
    
    #//////////// USERNAME ////////////
    def getUserName(self):
        pass
    
    def setUsername(self, _user):
        pass
    
    #//////////// API KEY ////////////
    def getAPIKeyPath(self, oai: bool = True) -> str:
        if oai:
            return openai.api_key_path

        _path = self.api_key_path
        self.config.saveConfig()
        return _path

    def setAPIKeyPath(self, _api_key_path: str) -> bool:
        if os.path.exists(_api_key_path):
            openai.api_key_path = _api_key_path
            self.config.openConfig()
            self.config.setOption("user", "api_key_path", f"{_api_key_path}")
            self.config.saveConfig()
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
    
    def getAPIKey(self, oai: bool = True) -> str: #UNCALLED
        if oai:
            return openai.api_key
        return self.api_key
        
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
        _api_base = self.api_base
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
        _api_type = self.api_type
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
        _api_version = self.api_version
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
        _organization = self.organization
        return _organization
    
    def setOrganization(self, _organization_id: str) -> None:
        openai.organization = _organization_id
        self.config.openConfig()
        self.config.setOption("user", "organization", f"{_organization_id}")
        self.config.saveConfig()
        self.organization = _organization_id
    
    #//////////// ENGINE ////////////
    def getEngine(self) -> str:
        _engine = self.engine
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
    
    def setUserDefinedFileName(self, _file_name: str) -> None:
        self.config.openConfig()
        self.config.setOption("chat", "user_defined_file_name", _file_name)
        self.config.saveConfig()
        self.user_defined_filename = _file_name

    #//////////// JSONL DATA FILE ////////////
    def getJSONLDataFile(self):
        return self.jsonl_data_file 

    def setJSONLDataFile(self, _jsonl_file_path: str) -> None:
        self.config.openConfig()
        self.config.setOption("chat", "jsonl_data_file", _jsonl_file_path)
        self.config.saveConfig()
        self.jsonl_data_file = _jsonl_file_path
        
        self.jsonl_data_file = file_obj = openai.File.create(
                file=open(f'{_jsonl_file_path}', 'rb'),
                purpose='fine-tune'
                # model=self.engine,
                # api_key=self.api_key,
                # api_base=self.api_base,
                # api_type=self.api_type,
                # api_version=self.api_version,
                # organization=self.organization,
                # user_provided_filename=self.user_defined_filename,     
            )
    
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
        
    def setStopList(self, _stoplist: str, _list_num: int = 1) -> None:
        self.config.openConfig()
        self.config.setOption("stop_lists", f"stop_list{_list_num}", _stoplist)
        self.config.saveConfig()
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
    def getTemperature(self) -> (int | float):
        _temp = self.temperature
        return _temp
    
    def setTemperature(self, _temperature: (int | float)) -> bool:
        if isinstance(_temperature, (int, float)):
            self.config.openConfig()
            self.config.setOption("chat", "chat_temperature", _temperature)
            self.config.saveConfig()
            self.temperature = _temperature
            return True
        return False
                        
    #//////////// FREQUENCY PENALTY ////////////
    def getFrequencyPenalty(self) -> (float | int):
        _freq_pen = self.frequency_penalty
        return _freq_pen
    
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
        _pres_pen = self.presence_penalty
        return _pres_pen
    
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
        _r_count = self.response_count
        return _r_count
     
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
        _rt_limit = self.response_token_limit
        return _rt_limit
    
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
        _best_of = self.best_of
        return _best_of
    
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
        _timeout = self.timeout
        return _timeout
    
    def setTimeout(self, _timeout: (int | float)) -> None:
        if isinstance(_timeout, int):
            self.config.openConfig()
            self.config.setOption("chat", "timeout", _timeout)
            self.config.saveConfig()
            self.timeout = _timeout
     
    def getUseImageEdit(self) -> int:
        return self.use_img_edit
    
    def setUseImageEdit(self, _use_edit: int) -> None:
        self.config.openConfig()
        self.config.setOption("image_requests", "use_edit", int(_use_edit))
        self.config.saveConfig()
        
    def getUseImageVariation(self) -> int:
        return self.use_img_var
    
    def setUseImageVariation(self, _use_variation: int) -> None:
        self.config.openConfig()
        self.config.setOption("image_requests", "use_variation", int(_use_variation))
        self.config.saveConfig()
        
    def getUseImageNew(self) -> int: 
        return self.use_img_new
    
    def setUseImageNew(self, _use_new: int) -> None:
        self.config.openConfig()
        self.config.setOption("image_requests", "use_new", int(_use_new))
        self.config.saveConfig()
    
    #//////////// AUDIO ////////////
    def getAudioFiles(self) -> str:
        return self.audio_file
    
    def setAudioFile(self, _audio_file: str) -> None:
        self.config.openConfig()
        self.config.setOption("audio_transcription", "audio_file", _audio_file)
        self.config.saveConfig()
        
    #//////////// EDIT ////////////
    def getInstruction(self) -> str:
        return self.audio_file
    
    def setInstruction(self, _audio_file: str) -> None:
        self.config.openConfig()
        self.config.setOption("edits", "instruction", _audio_file)
        self.config.saveConfig()
        
    #//////////// REQUEST TYPE ////////////
    def getRequestType(self) -> int:
        _req_type = self.request_type
        return _req_type
    
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

    def setRequest(self, _request: str) -> None:
        self.config.openConfig()
        self.config.setOption("requests", "previous_request", self.config.getOption("requests", "current_request"))
        self.config.setOption("requests", "current_request", _request)
        self.config.saveConfig()
        self.request = _request
    
    def requestData(self) -> None: 
        _respone = None
        try:
            #//////////// CHAT (WinGTP default request type) ////////////
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
                    timeout=self.timeout,
                    user=self.username
                )
                
            #//////////// IMAGES ////////////
            elif self.request_type == 1:
                _img_size = self.config.getOption("image_requests", "img_size")
                #//////////// IMAGE EDIT ////////////
                if self.use_img_edit == 1:  
                    print("cli use edit")
                    _mask_path = self.config.getOption("image_requests", "mask_path")
                    _img_path = self.config.getOption("image_requests", "img_path")
                    _response = openai.Image.create_edit(
                        image=open(f"{_img_path}", "rb"),
                        mask=open(f"{_mask_path}", "rb"),
                        prompt=self.request,
                        n=self.response_count,
                        size=_img_size,
                        response_format=self.image_response_format,
                        user=self.username
                    )
                #//////////// IMAGE VARIATION ////////////
                elif self.use_img_var == 1:  
                    _img_path = self.config.getOption("image_requests", "img_path")
                    _response = openai.Image.create_variation(
                        image=open(f"{_img_path}", "rb"),
                        n=self.response_count,
                        size=_img_size,
                        response_format=self.image_response_format,
                        user=self.username
                    )
                    
                #//////////// NEW IMAGE ////////////
                elif self.use_img_new == 1:
                    _response = openai.Image.create(
                        prompt=self.request,
                        n=self.response_count,
                        size=_img_size,
                        response_format=self.image_response_format,
                        user=self.username
                    )
                    
            #//////////// AUDIO ////////////
            elif self.request_type == 2:
                _audio_file = open(self.audio_file, "rb")
                _response = openai.Audio.transcribe(
                    self.engine,        # "whisper-1", 
                    _audio_file
                )
            #//////////// EMBEDDINGS ////////////
            elif self.request_type == 3:
                _response = openai.Embedding.create(
                    model=self.engine,              # "text-embedding-ada-002",
                    input=self.request,
                    user=self.username
                )
                
            #//////////// FILES ////////////
            elif self.request_type == 4:
                _response = openai.File.list()
            #//////////// FINE-TUNING ////////////
            elif self.request_type == 5:
                pass
            #//////////// MODERATIONS ////////////
            elif self.request_type == 6:
                _response = openai.Moderation.create(
                    input=self.request,
                )
            #//////////// BUILD REQUESTS ////////////
            elif self.request_type == 7:
                pass
            
            #//////////// TRANSLATIONS //   //////////
            elif self.request_type == 8:
                lang1 = self.config.getOption("translations", "lang1")
                lang2 = self.config.getOption("translations", "lang2")
                _prompt_string = f"Translate from {lang1} to {lang2}: {self.request}"
                _response = openai.Completion.create(
                    # Add more options later.
                    engine=self.engine,
                    prompt=_prompt_string,
                    max_tokens=self.response_token_limit,
                    user=self.username
                )
    
            #//////////// SENTIMENT ANALYSIS ////////////
            elif self.request_type == 9:
                _prompt_string = f"Sentiment analysis: {self.request}"
                _response = openai.Completion.create(
                    engine=self.engine,
                    prompt=_prompt_string,
                    max_tokens=self.response_token_limit,
                    user=self.username
                )
                
            #//////////// QUESTION ANSWERING ////////////
            elif self.request_type == 10:
                _context = self.config.getOption("qa", "context_1")
                _question = self.request
                _prompt_string = f"Question answering:\nContext: {_context}\nQuestion: {_question}"
                _response = openai.Completion.create(
                    engine=self.engine,
                    prompt=_prompt_string,
                    max_tokens=self.response_token_limit,
                    user=self.username
                )
            
            #//////////// SUMMARIZATION ////////////
            elif self.request_type == 11:
                _prompt_string = f"Summarize:\n{self.request}"
                _response = openai.Completion.create(
                    engine=self.engine,
                    prompt=_prompt_string,
                    max_tokens=self.response_token_limit,
                    user=self.username
                )
                
            #//////////// CODE GENERATION ////////////
            elif self.request_type == 12:
                _prompt_string = f"Code generation:\n{self.request}"
                _response = openai.Completion.create(
                    engine=self.engine,
                    prompt=_prompt_string,
                    max_tokens=self.response_token_limit,
                    user=self.username
                )
                
            #//////////// EDITS ////////////
            elif self.request_type == 13:
                _response = openai.Edit.create(
                    model=self.engine,
                    input=self.request,
                    instruction=f"{self.instruction} and don't change the original text.",
                    n=self.response_count,
                    temperature=1
                )
                
            self.response = _response
            
        except openai.APIError:
            print("OpenAI API Error")
        except openai.OpenAIError:
            print("OpenAI Error")
        except Exception as e:
            print(repr(e))
    
    #//////////// RESPONSES ////////////
    def getResponse(self) -> str:
        _response = self.response.choices[0].text.strip() 
        return _response  
    
    def createTempTranscriptFile(self, _transcript) -> bool:
        self.stdops.createFile(f"{paths.TMP_TRANSCRIPT_FILE}")
        if self.stdops.writeTofile(f"{paths.TMP_TRANSCRIPT_FILE}", _transcript, "w"):
            return True
        return False     
    
    def getTranscriptResponse(self) -> str:
        _response = self.response
        self.createTempTranscriptFile(str(_response))
        return _response
    
    def createTempURLFile(self, _url) -> bool:
        self.stdops.createFile(f"{paths.TMP_IMAGE_URL_FILE}")
        if self.stdops.writeTofile(f"{paths.TMP_IMAGE_URL_FILE}", _url, "w"):
            return True
        return False        

    def getFilesResponse(self) -> str:
        _response = self.response
        return _response

    def getImageURLResponse(self) -> str:
        _image_url = self.response['data'][0]['url']
        self.createTempURLFile(_image_url)
        return _image_url
    
    def createTempEmbeddingsFile(self, _embedding: str) -> bool:
        self.stdops.createFile(f"{paths.TMP_EMBEDDINGS_FILE}")
        if self.stdops.writeTofile(f"{paths.TMP_EMBEDDINGS_FILE}", _embedding, "w"):
            return True
        return False
    
    def getEmbeddingsResponse(self) -> str:
        _response = self.response["data"][0]
        self.createTempEmbeddingsFile(str(_response["embedding"]))
        return _response["embedding"]
        
    def getModerationResponse(self) -> str:
        _response = self.response["results"]
        return _response
    
    def getEditResponse(self) -> str:
        _response = self.response["choices"][0]["text"]
        return _response
    
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
                self.setRequest(f'Hi I\'m {user}.')
                self.requestData()
                greeting = self.getResponse()
            except openai.APIError:
                print("OpenAI API Error!")
            except openai.OpenAIError:
                print("OpenAI Error!")
            return greeting
                
