import os
import datetime

class FileWriter:
    path = ''

    def __init__(self, eventLogFile, sfURL):
        self.path = 'data/'+sfURL+'/'+eventLogFile["EventType"]+'/'+eventLogFile["LogDate"]+'_'+eventLogFile["Id"]+'.csv'

        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))

    def writeFile(self, input):
        with open(self.path, 'w') as file:
            file.write(str(input))
