import sys
from framework.utils.str_utils import StrUtils


class TestModel:
    """Data class for a test."""
    __test__ = False

    _allowed_attr = ['duration', 'method', 'name', 'startTime', 'start_time', 'endTime', 'end_time', 
                     'status', 'sid', 'project', 'host', 'browser', 'test_id', 'log', 'attachment']
    
    def __init__(self, test_data):        
        for key, value in test_data.items():
            if key in self._allowed_attr:
                if key == 'startTime':
                    setattr(self, 'start_time', value)
                    continue                     
                if key == 'endTime':
                    setattr(self, 'end_time', value)
                    continue
                else:
                    setattr(self, key, value)        

    def __eq__(self, other_user):
        if type(self) == type(other_user):
            return self.__dict__ == other_user.__dict__
        else:
            return False    

    def __str__(self):
        attr = ''
        for k, v in self.__dict__.items():
            attr += str(k) + ': ' + str(v) + '\n'        
        return f"Test:\n{attr}"

    def __call__(self):
        return sys.stdout.write(str(self))

    def add_log(self, logfile):
        log_content = StrUtils.read_text(logfile)
        self.log = log_content

    @staticmethod
    def generate_mock_object():
        """Create poor class' instance with proper attributes."""
        attributes = ['sid', 'project', 'name', 'method', 'host']        
        data_for_test_obj = {k: StrUtils.generate_text() for k in attributes}
        return TestModel(data_for_test_obj)
