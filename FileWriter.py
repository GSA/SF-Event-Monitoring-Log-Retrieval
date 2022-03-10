import os
import datetime
import re

class FileWriter:
    path = ''
    global strLogDateTime
    global strFormatedLogDateTime
    
    def __init__(self, eventLogFile, sfURL, debug=0):

#        self.path = 'data/'+sfURL+'/'+eventLogFile["EventType"]+'/'+eventLogFile["LogDate"]+'_'+eventLogFile["Id"]+'.csv'
        strLogDateTime = eventLogFile["LogDate"]
        strFormatedLogDateTime = str(datetime.datetime.strptime(strLogDateTime[0:19],"%Y-%m-%dT%H:%M:%S"))
        strFormatedLogDateTime = re.sub('[^a-zA-Z0-9 \n\.\-]', '', strFormatedLogDateTime).replace(" ", "_")
        self.path = 'data/'+sfURL+'/'+eventLogFile["EventType"]+'/'+strFormatedLogDateTime+'_'+eventLogFile["Id"]+'.csv'
        self.debug = debug
        if self.debug:
            print("writing file:" + self.path)

        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))

    def writeFile(self, input):
        with open(self.path, 'w') as file:
            file.write(input.decode())
