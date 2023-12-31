import configparser
import paths
import os


class Persistence():
    def __init__(self) -> None:
        self.CONFIG_DIR = f"{paths.CONFIG_DIR}"
        self.KEY_CONFIG_FILE = f"{paths.KEY_CONFIG_FILE}"
        self.USER_SETTINGS_FILE = f"{paths.USER_SETTINGS_FILE}"
        
        self.config = configparser.ConfigParser()
        
    # Loads the config file for operations.
    def openConfig(self):
        try:
            self.config.read(f"{self.USER_SETTINGS_FILE}")
        except FileNotFoundError:
            return False
        except IOError:
            return False
        except Exception as e:
            print(repr(e))
            return False

    # Get the value of a given option.        
    def getOption(self, _section: str, _option: str) -> str:
        _value = self.config.get(f"{_section}", f"{_option}")
        return _value
    
    # Set the value of a given option.
    def setOption(self, _section: str, _option: str, _new_value: str):
        self.config.set(f"{_section}", f"{_option}", f"{_new_value}")

    # Create a new config option.
    def addOption(self, _section: str, _new_option: str, _value: str) -> bool:
        if not self.optionExists(f"{_section}", f"{_new_option}"):
            self.config.set(f"{_section}", f"{_new_option}", f"{_value}")

    #Remove a config option
    def removeOption(self, _section: str, _option: str) -> None:
        self.config.remove_option(f"{_section}", f"{_option}")
        
    # Check if a config section exists.        
    def sectionExists(self, _section: str) -> bool:
        if self.config.has_section(f"{_section}"):
            return True
        else:
            return False

    # Check if a config option exists
    def optionExists(self, _section: str, _option: str) -> bool:
        if self.config.has_section(f"{_section}"):
            if self.config.has_option(f"{_section}", f"{_option}"):
                return True
            else:
                return False
        else:
            return False

    # Add a new config section.
    def addSection(self, _section: str) -> None:
        if not self.sectionExists((f"{_section}")):
            self.config.add_section(f"{_section}")

    # Remove a config section.
    def removeSection(self, _section: str) -> bool:
        if self.config.has_section(f"{_section}"):
            self.config.remove_section(f"{_section}")
            return True
        else:
            print(f"Section '{_section}' doesn't exist.")
            return False    

    # Set the name of the default section.
    def setDefaultSection(self, _section_name: str) -> None:
        if len(_section_name) == 0:
            self.config.default_section = "DEFAULT"
        else:
            self.config.default_section = _section_name
        
    # Retrieve a dictionary containing the default values from the parser.
    # The dictionary represents the options and their corresponding default 
    # values present in the default section.     
    def getDefaultOptionValues(self) -> dict:
        return self.config.defaults()
        
    # Save the configuration after operations. 
    def saveConfig(self) -> bool:
        try:
            with open(self.USER_SETTINGS_FILE, "w") as config_file:
                self.config.write(config_file)
                return True
        except FileNotFoundError:
            print(f"{self.USER_SETTINGS_FILE} not found! Can't save configuration")
            return False
        except IOError:
            print("IO error")
            return False
        except Exception as e:
            print(repr(e))
            return False

    # Merge another config file with this one.
    def updateConfig(self, _parser: configparser.ConfigParser):
        self.config.update(_parser)

    # Reset all sections and options.
    def resetConfig(self):
        self.config.clear()
    

