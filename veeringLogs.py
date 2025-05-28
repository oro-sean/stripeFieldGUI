import csv
import pandas as pd
import datetime
import xml.etree.ElementTree as ET

class VeeringLog:
    def __init__(self, logPath):
        self.logPath = logPath

    def Expedition_To_DF(self):
        with open(self.logPath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            labels = next(reader)
            num = next(reader)
            del labels[0]
            del num[0]
            columnLabels = dict(zip(num,labels))
            next(reader)
            values = []

            for row in reader:
                record ={}
                for i in range(0,(len(row)-1),2):
                    try:
                        key = row[i]
                        value = float(row[i+1])
                        record[key] = value
                    except:
                        break
                values.append(record)

        df = pd.DataFrame.from_records(values)
        df = df.rename(columns=columnLabels)
        self.log_df = df
        self.log_df.dropna(inplace=True)

    def Select_Variables(self, variables):
        self.log_df = self.log_df[variables].dropna()

    def Add_Time_Zone(self,timeZone):
        self.timeZone = datetime.timedelta(hours=timeZone)


    def Add_Time_Stamp(self):
        conv = lambda x: (datetime.datetime(1899,12,30) + datetime.timedelta(days=x)) + self.timeZone
        self.log_df['timeStamp'] = self.log_df['Utc'].apply(conv)

    def Get_Filter_TS(self,portMin, portMax, stbMin, stbMax, var):
        upwindPort = []
        upwindStb = []
        for i in range(len(portMin)):
            upwindPort = self.log_df['timeStamp'].loc[(self.log_df[var] < portMax) & (self.log_df[var] > portMin)]
            upwindStb = self.log_df['timeStamp'].loc[(self.log_df[var] < stbMax) & (self.log_df[var] > stbMin)]
        self.upwindStb = []
        self.upwindAll = []
        for ts in list(upwindStb):
            self.upwindStb.append(ts.to_pydatetime().replace(microsecond=0))
            self.upwindAll.append(ts.to_pydatetime().replace(microsecond=0))
        self.upwindPort =[]
        for ts in list(upwindPort):
            self.upwindPort.append(ts.to_pydatetime().replace(microsecond=0))
            self.upwindAll.append(ts.to_pydatetime().replace(microsecond=0))

class VeeringEvent:
    def __init__(self, eventPath):

        self.eventPath = eventPath

    def Load_XML(self):
        tree = ET.parse(self.eventPath)
        self.root = tree.getroot()
        for i  in range(len(self.root)):
            child = self.root[i]
            if child.tag == 'events':
                self.eventInd = i
            if child.tag == 'phases':
                self.phaseInd = i

    def Build_Event_Dict(self):
        self.events = {}
        for i in range(len(self.root[self.eventInd])):
            dateTime_string = str(self.root[self.eventInd][i].attrib['date'])+" "+str(self.root[self.eventInd][i].attrib['time'])
            dateTime_obj = datetime.datetime.strptime(dateTime_string, "%Y-%m-%d %H:%M:%S")
            datetime_obj = dateTime_obj + self.timeZone

            self.events[i] = [datetime_obj, self.root[self.eventInd][i].attrib['type'],self.root[self.eventInd][i].attrib['attribute']]

    def Build_Phase_Dict(self):
        self.phases = {}
        for i in range(len(self.root[self.phaseInd])):
            dateTime_string = self.root[self.phaseInd][0].find('startdatetime').attrib['val']
            dateTime_obj = datetime.datetime.strptime(dateTime_string, "%Y-%m-%d %H:%M:%S")
            datetime_obj = dateTime_obj + self.timeZone
            self.phases[i] = [datetime_obj, self.root[self.phaseInd][0].find('duration').attrib['val']]

    def Add_Time_Zone(self,timeZone):
        self.timeZone = datetime.timedelta(hours=int(timeZone))

    def build_Phase_DF(self):
        timeStamp_list = []
        for key in self.phases.keys():
            phase_start = self.phases[key][0]
            timeStamp_list.append(phase_start)
            for i in range(int(self.phases[key][1])):
                timeStep = phase_start + datetime.timedelta(seconds=int(1*i))
                timeStamp_list.append(timeStep.replace(microsecond=0))
        self.phase_df = pd.DataFrame(timeStamp_list)



