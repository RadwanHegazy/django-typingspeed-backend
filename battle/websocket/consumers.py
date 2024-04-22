from channels.generic.websocket import WebsocketConsumer


class SearchBattle (WebsocketConsumer): 
    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data):
        pass