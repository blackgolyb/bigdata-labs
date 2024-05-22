class Signal:
    def __init__(self):
        self.clear()

    def connect(self, callback):
        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def disconnect(self, callback):
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def clear(self):
        self._callbacks: list = []

    def emit(self, *args, **kwargs):
        for callback in self._callbacks:
            callback(*args, **kwargs)


class AsyncSignal:
    def __init__(self):
        self.clear()

    def connect(self, callback):
        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def disconnect(self, callback):
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def clear(self):
        self._callbacks: list = []

    async def emit(self, *args, **kwargs):
        for callback in self._callbacks:
            await callback(*args, **kwargs)
