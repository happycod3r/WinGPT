from chatmemory import memory
import persistence
import openai
import sys
import os

class WinGTPCLI:
     
    def __init__(self) -> None:
        self.config = persistence.Persistence()
        self.CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
        self.CONFIG_DIR = f"{self.CURRENT_PATH}\\config"
        self.LOGS_DIR = f"{self.CURRENT_PATH}/\\logs"
        self.USER_SETTINGS_FILE = f"{self.CONFIG_DIR}\\settings.ini"
        self.KEY_CONFIG_FILE = f"{self.CONFIG_DIR}\\.api_key.ini"
        
        self.setAPIKeyPath(self.KEY_CONFIG_FILE)
                
        self.cli_options = [
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
            'help', # Prints this message. 
            'clear', # Clear the output box.
            'theme', # Change the theme. Requires theme as 1st argument.
            'color', # Change the output color
            'temp',  # Set the output temperature.
        ]   
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
        self.api_key_path = None
        self.api_key = None
        self.api_base = openai.api_base
        self.api_type = openai.api_type
        self.api_version = openai.api_version
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
        self.organization = openai.organization
        self.user_defined_filename = None
        self.temps = {"low":0, "medium":1, "high":2}
        self.temperature = self.temps["medium"]
        self.stop_list = None
        self.USE_STOPLIST = False
        openai.api_key_path = self.api_key_path
        openai.api_key = self.api_key
    
    def _clear(self) -> None:
        print('\033c', end='')
    
    def createDir(self, path: str) -> bool:
        if not os.path.exists(path):
            try:
                os.mkdir(path)
                return True
            except FileExistsError:
                print(f"Folder '{path}' already exists.")
                return False
            except Exception as e:
                print(repr(e))
                return False
        return False        
    
    def createFile(self, file_path: str) -> bool:
        if not os.path.exists(file_path):
            try:
                with open(file_path, 'w') as file:
                    return True
            except FileNotFoundError:
                print(f"File '{file_path}' already exists!")
                return False
            except IOError:
                return False
            except Exception as e:
                print(repr(e))
                return False
                    
    def writeTofile(self, file_path: str, content: str = None) -> bool:
        print(f"file_path: {file_path}")
        print(f"content: {content}")
        if os.path.exists(file_path):
            try:
                with open(f"{file_path}", 'w') as file:
                    if len(content) != 0:
                        if file.writable() :
                            file.write(content)
                            file.close()
                        else: 
                            return False
                print(f"File '{file_path}' created successfully.")
                return True
            except FileNotFoundError:
                print(f"File '{file_path}' not found!")
                return False
            except IOError:
                print(f"An error occurred while creating the file '{file_path}'.")
                return False
            except Exception as e:
                print(f"An error occurred while creating the file '{file_path}'.")
                return False
        return False
    
    def readFromFile(self, file_path: str) -> str:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as file:
                    contents = file.read()
                    if len(contents) != 0:
                        return contents
                    else: 
                        print(f"File @'{file_path}' is exists but is empty")
            except FileNotFoundError:
                print(f"File '{file_path}' not found.")
            except IOError:
                print(f"Error reading file '{file_path}'.")
            except Exception as e:
                print(f"Error reading file '{file_path}")
        else: 
            print(self.readFromFile.__name__, " File doesn't exist to read from!")
    
    def getPrompt(self) -> str:
        return self.prompt

    def setPrompt(self) -> None:
        if self.api_version != None:
            self.prompt = f"[{self.engine}] [{self.api_version}] >>> "
        else:
            self.prompt = f"WinGTP@0.1.0 > [{self.engine}] >>> "
        
    def getAPIBase(self) -> str:
        return openai.api_base
    
    def setAPIBase(self, api_base: str) -> None:
        self.api_base = api_base
        openai.api_base = self.api_base
        
    def getAPIType(self) -> str:
        return openai.api_type
    
    def setAPIType(self, api_type: str) -> None:
        self.api_type = api_type
        openai.api_type = self.api_type
        
    def getAPIVersion(self) -> str:
        return openai.api_version
    
    def setAPIVersion(self, api_version: str) -> None:
        self.api_version = api_version
        openai.api_version = self.api_version
        
    def getOrganization(self) -> str:
        return openai.organization
    
    def setOrganization(self, organization: str) -> None:
        self.organization = organization
        openai.organization = self.organization
        
    def getUserDefinedFileName(self) -> str:
        return self.user_defined_filename
    
    def setUserDefinedFileName(self, file_name: str) -> None:
        self.user_defined_filename = file_name

    def getAPIKeyPath(self) -> str:
        return openai.api_key_path

    def setAPIKeyPath(self, api_key_path: str) -> bool:
        if os.path.exists(api_key_path):
            self.api_key_path = api_key_path
            openai.api_key_path = api_key_path
            return True
        return False
        
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

    def getEngine(self) -> str:
        return self.engine

    def getEngines(self) -> list:
        model_lst = openai.Model.list()
        engines = []
        for i in model_lst["data"]:
            engines.append(i["id"])
        return engines
    
    def setEngine(self, engine: str) -> None:
        self.engine = engine
        
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
        
    def getResponseTokenLimit(self) -> int:
        return self.response_token_limit
    
    def setResponseTokenLimit(self, response_token_limit: int) -> None: 
        self.response_token_limit = response_token_limit
     
    def getResponseCount(self) -> int:
        return self.response_count
     
    def setResponseCount(self, response_count: int) -> None: 
        self.response_count = response_count
        
    def setTemperature(self, _temperature: int) -> None:
        if isinstance(_temperature, (int, float)):
            self.temperature = _temperature
        
    def getTemperature(self) -> int:
        return self.temperature
        
    def setStopList(self, _stoplist: str) -> None:
        self.stop_list = _stoplist.split()
    
    def getStopList(self) -> list:
        return self.stop_list
        
    def setChatEcho(self, echo: bool) -> None:
        self.echo = echo
        
    def getChatEcho(self) -> bool:
        return self.echo
        
    def setChatStream(self, stream: bool) -> None:
        self.stream = stream
        
    def getChatStream(self) -> bool:
        return self.stream
        
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
        
    def validateAPIKey(self, api_key: str) -> bool:
        if not (api_key.startswith('sk-') and len(api_key) == 51):
            return False
        else:    
            return True
        
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
        
    def getResponse(self) -> str:
        response = self.response.choices[0].text.strip() 
        return response

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
    
    def banner(self) -> None:
        """
WinGTP v0.1.0 - OpenAI Command-line Interface
        """
        
    def greetUser(self, user: str, key_path: str) -> str:
        if os.path.exists(key_path):
            try:
                self.setAPIKeyPath(key_path)
                self.setResponseTokenLimit(self.response_token_limit)
                self.setEngine(self.engine)
                self.setResponseCount(self.response_count)
                self.setRequest(f'Hello? I\'m {user}')
                self.requestData()
                greeting = self.getResponse()
            except openai.APIError:
                print("OpenAI API Error!")
            except openai.OpenAIError:
                print("OpenAI Error!")
            return greeting
                
    def converse(self) -> None:
        
        print(self.banner.__doc__)
        
        while True:   
            user_prompt = input(f"{self.prompt}")
            if user_prompt == self.cli_options[0]:
                print(f'\nGoodbye! ...\n')
                sys.exit()
            elif user_prompt == self.cli_options[1]:
                token_limit = input('Set the max amount of reponse tokens: ')
                self.setResponseTokenLimit(int(token_limit))
                print(f'Token limit set to {self.getResponseTokenLimit()} tokens per response.')
                continue
            elif user_prompt == self.cli_options[2]:
                engine = input("Set the engine: ")
                self.setEngine(engine)
                print(f'Engine set to {self.getEngine()}')
                continue
            elif user_prompt == self.cli_options[3]:
                response_count = input("Set the number of reponses: ")
                self.setResponseCount(int(response_count))
                print(f'The number of reponses is set to {self.getResponseCount()}')
                continue
            elif user_prompt == self.cli_options[4]:
                api_base = input("Set the API base: ")
                self.setAPIBase(str(api_base))
                print(f'The API base is set to {self.getAPIBase()}')
                continue
            elif user_prompt == self.cli_options[5]:
                api_type = input("Set the API type: ")
                self.setAPIType(str(api_type))
                print(f'The API type is set to {self.getAPIType()}')
                continue
            elif user_prompt == self.cli_options[6]:
                api_version = input("Set the API version: ")
                self.setAPIVersion(str(api_version))
                print(f'The API version is set to {self.getAPIVersion()}')
                continue
            elif user_prompt == self.cli_options[7]:
                organization = input("Set the organization name: ")
                self.setOrganization(str(organization))
                print(f'The API base is set to {self.getOrganization()}')
                continue
            elif user_prompt == self.cli_options[8]:
                user_defined_filename = input("Set a user defined file name: ")
                self.setUserDefinedFileName(str(user_defined_filename))
                print(f'The user defined file name is set to {self.getUserDefinedFileName()}')
                continue
            elif user_prompt == self.cli_options[9]:
                jsonl_file_path = input("Set a JSONL file: ")
                self.setJSONLDataFile(str(jsonl_file_path))
                print(f'The JSONL file is set to {self.getJSONLDataFile()}')
                continue
            elif user_prompt == self.cli_options[10]:
                print(self._help.__doc__)
            elif user_prompt == self.cli_options[11]:
                self._clear()
            else:
                self.setResponseTokenLimit(self.response_token_limit)
                self.setEngine(self.engine)
                self.setResponseCount(self.response_count)
                self.setRequest(str(user_prompt))
                self.requestData()
                print(self.getResponse())
