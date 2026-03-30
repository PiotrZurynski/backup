class Temperature:
    def __init__(self,celsius:float):
        self.__celsius=celsius

    @property
    def celsius(self)->float:
        return self.__celsius
    @celsius.setter
    def celsius(self,value:float):
        self.__celsius=value

    def fahrenheit(self)->float:
        return self.__celsius*1.8 +32

