import os
import datetime

class FileWriter:
    path = ''

    def __init__(self, eventLogFile=0):
        self.path = 'data/'+eventLogFile["EventType"]+'/'+eventLogFile["LogDate"]+'_'+eventLogFile["Id"]+'.csv'

        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))

    def writeFile(self, input):
        with open(self.path, 'a') as outputlog:
            outputlog.write(str(input))
            outputlog.write("\n")
