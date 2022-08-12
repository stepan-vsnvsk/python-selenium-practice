class TestModel:
    _allowed_attr = ['duration', 'method', 'name', 'startTime', \
                     'start_time', 'endTime', 'end_time', 'status']

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
