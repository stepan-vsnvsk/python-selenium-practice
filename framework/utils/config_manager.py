from framework.utils.json_utils import JsonUtils


class ConfigManager:
    """Methods for parsing and getting config data."""

    _config = {}

    @staticmethod
    def parse_config_for_driver(config='config.json'):
        """Parse data for Webdriver's settings ."""
        if not ConfigManager._config:
            ConfigManager._config = JsonUtils.read_from_json(config) 
        options = []
        methods = []
        if 'flags' in ConfigManager._config: 
            for k, v in ConfigManager._config['flags'].items():                
                if v == 'True':                    
                    if k == 'incognito':                        
                        options.append("--incognito")                    
                    if k == 'maximize_window':
                        methods.append("maximize_window")  
        if 'language' in ConfigManager._config:
            options.append("--lang=" + ConfigManager._config['language'])
        return options, methods

    @staticmethod
    def get_value_from_config(key, config='config.json'):        
        """Get specific value by key from config data."""
        data = JsonUtils.read_from_json(config)
        return data.get(key) 
