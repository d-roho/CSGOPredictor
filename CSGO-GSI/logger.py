class LogFile():
    def __init__(self, timestamp):
        self.name = str(timestamp).replace(' ', '_').replace(':', '-')
        print(self.name)
        self.path = 'logs/' + self.name + '.txt'
        self.create_file()

    def create_file(self):
        file = open(self.path, 'w', encoding='utf-8')
        file.write('Log file created at ' + self.name + '\n')
        file.close()

    def log_event(self, timestamp, event):
        file = open(self.path, 'a', encoding='utf-8')
        file.write("snapshot" + '\n' + timestamp + '\n')
        file.write(str(event))
        file.write('\n')
        file.close()