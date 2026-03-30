class Percentage:
    def __ini__(self,value:float)->None:
        self.value=value
    def __mul__(self,value1:float):
        return (self.value/100)*200
