class Object:
    def __init__(self):
        self.__parent = None
        self.__children = set()

    def initUI(self):
        pass

    def update(self):
        pass

    def event(self, e0):
        pass

    def parent(self):
        return self.__parent

    def has(self, obj):
        return obj in self.__children

    def remove(self, obj):
        self.__children.remove(obj)

    def add(self, obj):
        self.__children.add(obj)

    def children(self):
        return list(self.__children)
