

class Singleton(type):
    '''Singleton metaclass'''
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__instance = None
        
    def __call__(self, *args, **kwargs):
        if not self.__instance:
            self.__instance = super().__call__(*args, **kwargs)
        return self.__instance