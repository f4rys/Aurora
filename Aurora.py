from modules.gui import Application

class Aurora():
    def __init__(self):
        self.application = Application([])

    def restart(self):
        self.application.exit()
        self.application = Application([])

if __name__ == '__main__':
    aurora = Aurora()