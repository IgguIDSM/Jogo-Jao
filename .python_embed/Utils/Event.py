class Event:
    def __init__(self):
        self._listeners = []

    def subscribe(self, listener):
        self._listeners.append(listener)

    def unsubscribe(self, listener):
        self._listeners.remove(listener)

    def Trigger(self, *args, **kwargs):
        for listener in self._listeners:
            listener(*args, **kwargs)