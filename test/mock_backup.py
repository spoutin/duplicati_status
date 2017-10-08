
backup = [
             {
                 "Schedule": {
                     "ID": 1,
                     "Tags": [
                         "ID=1"
                     ],
                     "Time": "2017-09-18T01:00:00Z",
                     "Repeat": "1D",
                     "LastRun": "2017-09-15T00:00:00Z",
                     "Rule": "AllowedWeekDays=Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday",
                     "AllowedDays": [
                         "mon",
                         "tue",
                         "wed",
                         "thu",
                         "fri",
                         "sat",
                         "sun"
                     ],
                 },
                 "Backup": {
                     "ID": "1",
                     "Name": "test",
                     "Tags": [],
                     "TargetURL": "file://d:\\test",
                     "DBPath": "C:\\Users\\someuser\\AppData\\Local\\Duplicati\\FFHQUUONSJ.sqlite",
                     "Sources": None,
                     "Settings": None,
                     "Filters": None,
                     "Metadata": {
                         "LastDuration": "00:00:01.1470004",
                         "LastStarted": "20170918T005616Z",
                         "LastFinished": "20170918T005617Z",
                         "LastBackupDate": "20170916T210707Z",
                         "BackupListCount": "1",
                         "TotalQuotaSpace": "250048507904",
                         "FreeQuotaSpace": "149693239296",
                         "AssignedQuotaSpace": "-1",
                         "TargetFilesSize": "14391",
                         "TargetFilesCount": "3",
                         "TargetSizeString": "14.05 KB",
                         "SourceFilesSize": "116113",
                         "SourceFilesCount": "1",
                         "SourceSizeString": "113.39 KB",
                         "LastBackupStarted": "20170918T005616Z",
                         "LastBackupFinished": "20170918T005617Z"
                     },
                     "IsTemporary": False
                 }
             },
{
    "Schedule": {
      "ID": 2,
      "Tags": [
        "ID=2"
      ],
      "Time": "2017-09-16T17:00:00Z",
      "Repeat": "1M",
      "LastRun": "0001-01-01T05:00:00Z",
      "Rule": "AllowedWeekDays=Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday",
      "AllowedDays": [
        "mon",
        "tue",
        "wed",
        "thu",
        "fri",
        "sat",
        "sun"
      ]
    },
    "Backup": {
      "ID": "2",
      "Name": "test2",
      "Tags": [],
      "TargetURL": "file://d:\\test2",
      "DBPath": "C:\\Users\\someuser\\AppData\\Local\\Duplicati\\FFHQUUONSJ.sqlite",
      "Sources": None,
      "Settings": None,
      "Filters": None,
      "Metadata": {},
      "IsTemporary": False
    }
  }
]