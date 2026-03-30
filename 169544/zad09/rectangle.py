class Rectangle:
    def __init__(self,width:float,height:float)->None:
        self.width=width
        self.height=height
    def __eq__(self,other:Rectangle)->bool:
        prostokat1=self.width*self.height
        prostokat2=other.width*other.height
        return prostokat1 ==prostokat2
    def __lt__(self,other:Rectangle)->bool:
        prostokat1 = self.width * self.height
        prostokat2 = other.width * other.height
        return prostokat1 < prostokat2
    def __gt__(self, other:Rectangle)->bool:
        prostokat1 = self.width * self.height
        prostokat2 = other.width * other.height
        return prostokat1 > prostokat2

