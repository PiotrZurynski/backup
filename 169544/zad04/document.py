import re
class Document:
    def __init__(self,title:str,authors:list[str],metadata:dict[str,str],version:str)->None:
        pattern = "\d+\.\d+\.\d+"
        if len(title)>0 and len(title)<201:
            self.__title=title
        else:
            raise ValueError("zla waga")
        if authors is None:
            raise ValueError("Brak authorwo")
        self.__authors=authors
        if metadata is None:
            self.__metadata=dict[str,str]
        self.__metadata=metadata
        if not isinstance(version,str):
            raise ValueError("nie string")
        elif not re.findall(pattern,version):
            raise ValueError("zly pattern")
        else:
            self.version=version

    @property
    def version(self):
        return self.__version
    @version.setter
    def version(self,value):
        pattern = "\d+\.\d+\.\d+"
        if not re.findall(pattern,value):
            raise ValueError("zly pattern dla nowej wartosci")
        if value> self.version:
            self.__version=value

doc=Document("tyl",['sd','ds'],{'sds':'dsds'},"1.1.1")

doc.version="2.1.1"
print(doc.version)
