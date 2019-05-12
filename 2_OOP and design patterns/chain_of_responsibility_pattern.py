class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 6.4
        self.string_field = "str"


class EventGet:
    def __init__(self, name):
        self.name = name


class EventSet:
    def __init__(self, name):
        self.name = name


class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if type(event) == EventGet and event.name == int:
            return obj.integer_field
        elif type(event) == EventSet and type(event.name) == int:
            obj.integer_field = event.name
        else:
            return super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if type(event) == EventGet and event.name == float:
            return obj.float_field
        elif type(event) == EventSet and type(event.name) == float:
            obj.float_field = event.name
        else:
            return super().handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if type(event) == EventGet and event.name == str:
            return obj.string_field
        elif type(event) == EventSet and type(event.name) == str:
            obj.string_field = event.name
        else:
            return super().handle(obj, event)


chain = IntHandler(FloatHandler(StrHandler(NullHandler())))
obj1 = SomeObject()
events = [EventGet(int), EventGet(str),
          EventGet(float), EventSet(1),
          EventSet(1.1), EventSet("str")]

for event in events:
    print(chain.handle(obj1, event))