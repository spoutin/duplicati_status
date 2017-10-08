import datetime
import exceptions


class Backup(object):
    def __init__(self, data):
        self.id = data['backup']['id']
        self.name = data['backup']['name']
        self.tags = data['backup']['tags']
        self.targetURL = data['backup']['targetURL']
        self.dbPath = data['backup']['dbPath']
        self.sources = data['backup']['sources']
        self.settings = data['backup']['settings']
        self.filters = data['backup']['filters']
        self.metadata = Backup.Metadata(**data['backup']['metadata'])
        self.isTemporary = data['backup']['isTemporary']
        self.schedule = Backup.Schedule(**data['schedule'])
        self.original_backup_object = data

    def __repr__(self):
        return self.discovery()

    def discovery(self):
        return {"id": self.id, "name": self.name}

    def calculate_delta(self, now=datetime.datetime.now()):
        if not isinstance(now, datetime.datetime):
            raise ValueError("Need to provide an instance of datetime object")
        return now - self.metadata.LastBackupFinished

    def is_backup_old(self, now=datetime.datetime.now(datetime.timezone.utc)):
        if self.metadata.LastBackupFinished is None:
            return True

        delta = self.calculate_delta(now=now)

        if self.schedule.repeat.period == "D":
            if delta.days > self.schedule.repeat.frequency:
                return True
        elif self.schedule.repeat.period == "W":
            if delta.days > self.schedule.repeat.frequency * 7:
                return True
        elif self.schedule.repeat.period == "M":
            if delta.days > self.schedule.repeat.frequency * 31:
                return True
        elif self.schedule.repeat.period == "Y":
            if delta.days > self.schedule.repeat.frequency * 365:
                return True
        elif self.schedule.repeat.period == "m":
            if delta.seconds > self.schedule.repeat.frequency * 60 and delta.days == 0:
                return True
        elif self.schedule.repeat.period == "h":
            if delta.seconds > self.schedule.repeat.frequency * 60 * 60 and delta.days == 0:
                return True
        else:
            raise ValueError("unknown period received, unable to calculate last backup")
        return False


    class Metadata(object):
        def __init__(self, **kwargs):
            self.LastDuration = None
            self.LastStarted = None
            self.LastFinished = None
            self.LastBackupDate = None
            self.BackupListCount = None
            self.TotalQuotaSpace = None
            self.FreeQuotaSpace = None
            self.AssignedQuotaSpace = None
            self.TargetFilesSize = None
            self.TargetFilesCount = None
            self.TargetSizeString = None
            self.SourceFilesSize = None
            self.SourceFilesCount = None
            self.SourceSizeString = None
            self.LastBackupStarted = None
            self.LastBackupFinished = None

            for key, value in kwargs.items():
                setattr(self, key, value)

    class Schedule(object):
        def __init__(self, **kwargs):
            self.id = kwargs['id']
            self.tags = kwargs['tags']
            self.time = kwargs['time']
            self.repeat = Backup.Schedule.Repeat(kwargs['repeat'])
            self.lastRun = kwargs['lastRun']
            self.rule = kwargs['rule']
            self.allowedDays = kwargs['allowedDays']

        def calculate_delta(self, now=datetime.datetime.now()):
            if not isinstance(now, datetime.datetime):
                raise ValueError("Need to provide an instance of datetime object")
            return now - self.lastRun

        def is_backup_old(self, now=datetime.datetime.now(datetime.timezone.utc)):
            delta = self.calculate_delta(now=now)
            if self.repeat.period == "D":
                if delta.days > self.repeat.frequency:
                    return True
            elif self.repeat.period == "W":
                if delta.days > self.repeat.frequency*7:
                    return True
            elif self.repeat.period == "M":
                if delta.days > self.repeat.frequency*31:
                    return True
            elif self.repeat.period == "Y":
                if delta.days > self.repeat.frequency*365:
                    return True
            elif self.repeat.period == "m":
                if delta.seconds > self.repeat.frequency*60 and delta.days == 0:
                    return True
            elif self.repeat.period == "h":
                if delta.seconds > self.repeat.frequency*60*60 and delta.days == 0:
                    return True
            else:
                raise ValueError("unknown period received, unable to calculate last backup")
            return False

        class Repeat:
            def __init__(self, repeat):
                self.check_repeat(repeat)
                self.frequency = int(repeat[0])
                self.period = repeat[1]

            @staticmethod
            def check_repeat(repeat):
                if len(repeat) != 2:
                    raise exceptions.UnknownRepeat
                frequency, period = repeat
                if not period.isalpha():
                    raise exceptions.UnknownPeriod
                if not frequency.isdigit():
                    raise exceptions.UnknownFrequency
                return True
