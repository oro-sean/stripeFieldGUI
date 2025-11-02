import csv
import pandas as pd
import datetime
import xml.etree.ElementTree as ET

class VeeringLog:
    def __init__(self, logPath):
        self.logPath = logPath

    def Expedition_To_DF(self):
        with open(self.logPath, newline='') as csvfile:
            print("Reading log file")
            reader = csv.reader(csvfile, delimiter=',')
            labels = next(reader)
            num = next(reader)
            del labels[0]
            del num[0]
            columnLabels = dict(zip(num,labels))
            next(reader)
            values = []

            for row in reader:
                print("Iterate over rows")
                print(row)
                record ={}
                for i in range(0,(len(row)-1),2):
                    print(i)
                    try:
                        print("in Try")
                        key = row[i]
                        value = float(row[i+1])
                        record[key] = value
                    except:
                        print("error")
                print("exit i")
                values.append(record)
                print("values appended")

        df = pd.DataFrame.from_records(values)
        print("Made DF")
        df = df.rename(columns=columnLabels)
        self.log_df = df

    def Select_Variables(self, variables):
        print("Select variables - "+str(variables))
        print(self.log_df.shape)
        self.log_df = self.log_df[variables].dropna()
        print(self.log_df.shape)

    def Add_Time_Zone(self,timeZone):
        self.timeZone = datetime.timedelta(hours=timeZone)

    def Add_Time_Stamp(self):
        self.log_df.dropna(subset=['Utc'], inplace=True)
        conv = lambda x: (datetime.datetime(1899,12,30) + datetime.timedelta(days=x)) + self.timeZone
        self.log_df['timeStamp'] = self.log_df['Utc'].apply(conv)

    def Get_Filter_TS(self,portMin, portMax, stbMin, stbMax, var):
        upwindPort_all = set()
        upwindStb_all = set()
        for i in range(len(portMin)):
            upwindPort = set(self.log_df['timeStamp'].loc[(self.log_df[var] < float(portMax[i])) & (self.log_df[var] > float(portMin[i]))])
            upwindStb = set(self.log_df['timeStamp'].loc[(self.log_df[var] < float(stbMax[i])) & (self.log_df[var] > float(stbMin[i]))])
            upwindPort_all = upwindPort_all.union(upwindPort)
            upwindStb_all = upwindStb.union(upwindStb)

        upwindPort_all_list = []
        upwindStb_all_list = []

        for ts in list(upwindStb_all):
            upwindStb_all_list.append(ts.replace(microsecond=0))

        for ts in list(upwindPort_all):
            upwindPort_all_list.append(ts.replace(microsecond=0))

        return upwindPort_all_list, upwindStb_all_list

class VeeringEvent:
    def __init__(self, eventPath):
        self.eventPath = eventPath
        self.phases_df_check = False

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
            dateTime_string = self.root[self.phaseInd][i].find('startdatetime').attrib['val']
            dateTime_obj = datetime.datetime.strptime(dateTime_string, "%Y-%m-%d %H:%M:%S")
            datetime_obj = dateTime_obj + self.timeZone
            self.phases[i] = [datetime_obj, self.root[self.phaseInd][i].find('duration').attrib['val']]

    def Add_Time_Zone(self,timeZone):
        self.timeZone = datetime.timedelta(hours=int(timeZone))

    def Build_Phase_DF(self):
        timeStamp_list = []
        for key in self.phases.keys():
            phase_start = self.phases[key][0].replace(microsecond=0)
            timeStamp_list.append(phase_start)
            for i in range(1, int(self.phases[key][1])):
                timeStep = phase_start + datetime.timedelta(seconds=int(1*i))
                timeStamp_list.append(timeStep.replace(microsecond=0))
        self.phase_df = pd.DataFrame(timeStamp_list, columns=['timeStamp'])
        self.phases_df_check = True

    def Make_Data_Frame(self, startTime, endTime, colNames, colValues, fill):
        currentTime = startTime
        data = []
        if fill == True:
            while currentTime < endTime:
                entry = []
                entry.append(currentTime.replace(microsecond=0))
                for i in range(len(colNames)):
                    entry.append(colValues[i])
                data.append(entry)
                currentTime += datetime.timedelta(seconds=1)
        else:
            entry = []
            entry.append(currentTime.replace(microsecond=0))
            for i in range(len(colNames)):
                entry.append(colValues[i])
            data.append(entry)

        colNames.insert(0, "timeStamp")

        return pd.DataFrame(data, columns=colNames)

    def Build_Event_DF(self):
        dayStart_ts = []
        dayStart_attrib = []
        sails_ts = []
        sails_attrib = []
        manual_ts = []
        manual_attrib = []
        race_ts = []
        race_attrib = []
        lastEvent_time = []
        dayStart_check = False
        sails_check = False
        manual_check = False
        races_check = False
        timeStamp_list = []
        for key in self.events.keys():
            timeStamp_list.append(self.events[key][0])

        timeStamp_list.sort()
        lastEvent_time = timeStamp_list[-1]

        for key in self.events.keys():
           if self.events[key][1] == "DayStart":
                stopFound = False
                searchKeyInd = 0
                keys = list(self.events.keys())
                while stopFound == False:
                    if self.events[keys[searchKeyInd]][1] == "DayStop":
                        dayStop_time = self.events[keys[searchKeyInd]][0]
                        stopFound = True
                    else:
                        searchKeyInd += 1
                dayStart_ts.append(self.events[key][0])
                dayStart_ts.append(dayStop_time)
                dayStart_attrib.append({"Day": 1})
                dayStart_check = True

           if self.events[key][1] == "SailsUp":
               sails_ts.append(self.events[key][0])
               sail = {}
               type = ['Mainsail', 'Jib', 'Staysail', 'Spinaker']
               for i in range(len(type)):
                   sail[type[i]] = str(self.events[key][2]).split(';')[i]
               sails_attrib.append(sail)
               sails_check = True

           if self.events[key][1] == "ManualEntry":
               manual = {}
               manual_ts.append(self.events[key][0])
               attributes = str(self.events[key][2]).split(';')
               for i in range(len(attributes)):
                   if "=" in attributes[i]:
                    try:
                        manual[attributes[i].split('=')[0]] = attributes[i].split('=')[1]
                    except:
                        print("Failed to extract manual")

               manual_attrib.append(manual)
               manual_check = True

           if self.events[key][1] == "RaceStartGun":
               keys = list(self.events.keys())
               raceStart = self.events[key][0]
               raceNumber = self.events[key][2]
               race_ts.append(raceStart)
               race_attrib.append({"Race": raceNumber, "Leg": 1})
               for i in range(len(keys)):
                   if self.events[keys[i]][1] == "RaceFinish" and self.events[keys[i]][2] == raceNumber:
                       raceFinish = self.events[keys[i]][0]


               for i in range(len(keys)):
                   if self.events[keys[i]][1] == "RaceMark" and self.events[keys[i]][0] < raceFinish and self.events[keys[i]][0] > raceStart:
                       raceMark_ts = self.events[keys[i]][0]
                       raceLeg = int(self.events[keys[i]][2])+1
                       race_ts.append(raceMark_ts)
                       race_attrib.append({"Race": raceNumber, "Leg": raceLeg})

               race_ts.append(raceFinish)
               race_attrib.append({"Race": "NaN", "Leg": "NaN"})
               races_check = True

        event_types = [dayStart_check, sails_check, manual_check, races_check]
        event_ts = [dayStart_ts, sails_ts, manual_ts, race_ts]
        event_attrib = [dayStart_attrib, sails_attrib, manual_attrib, race_attrib]
        data_frames = []

        for i in range(len(event_types)):
            if event_types[i] == True:
                event_ts[i].append(lastEvent_time)
                event_attrib[i].append(event_attrib[i][-1])
                for n in range(len(event_ts[i])-1):
                    if n == 0:
                        event_df = self.Make_Data_Frame(startTime=event_ts[i][n],
                                                    endTime=event_ts[i][n+1],
                                                    colNames=list(event_attrib[i][n].keys()),
                                                    colValues=list(event_attrib[i][n].values()),
                                                    fill=True)
                    elif event_ts[i][n] != event_ts[i][n+1]:
                        new_df = self.Make_Data_Frame(startTime=event_ts[i][n],
                                                    endTime=event_ts[i][n+1],
                                                    colNames=list(event_attrib[i][n].keys()),
                                                    colValues=list(event_attrib[i][n].values()),
                                                    fill=True)
                        event_df.merge(new_df, on='timeStamp', how='outer')

                data_frames.append(event_df)

        if len(data_frames) == 1:
            events_df = data_frames[0]
        elif len(data_frames) == 2:
            events_df = pd.merge(left=data_frames[0], right=data_frames[1], on='timeStamp', how='outer')
        else:
            events_df = pd.merge(left=data_frames[0], right=data_frames[1], on='timeStamp', how='outer')
            for i in range(2, len(data_frames)):
                events_df = pd.merge(left=events_df, right=data_frames[i], on='timeStamp', how='outer')

        self.events_df = events_df




















