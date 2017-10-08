from pprint import pprint

from marshmallow import Schema, fields, post_load, validate
import backups


def get_model(data):
    schema = BackupAPISchema()
    result = schema.load(data)
    return result


def dump_model(data):
    schema = BackupAPISchema()
    result = schema.dumps(data).data
    return result


class ScheduleSchema(Schema):
    id = fields.Integer(required=True, load_from="ID")
    tags = fields.List(fields.String(), load_from="Tags", required=True)
    time = fields.DateTime(load_from="Time", required=True)
    repeat = fields.String(load_from="Repeat", required=True)
    lastRun = fields.DateTime(load_from="LastRun", required=True)
    rule = fields.String(load_from="Rule", required=True, allow_none=True)
    allowedDays = fields.List(fields.String(), load_from="AllowedDays", required=True, allow_none=True)


class MetadataSchema(Schema):
    LastDuration = fields.DateTime(load_from="LastDuration")
    LastStarted = fields.DateTime(load_from="LastStarted")
    LastFinished = fields.DateTime(load_from="LastFinished")
    LastBackupDate = fields.DateTime(load_from="LastBackupDate")
    BackupListCount = fields.String(load_from="BackupListCount")
    TotalQuotaSpace = fields.String(load_from="TotalQuotaSpace")
    FreeQuotaSpace = fields.String(load_from="FreeQuotaSpace")
    AssignedQuotaSpace = fields.String(load_from="AssignedQuotaSpace")
    TargetFilesSize = fields.String(load_from="TargetFilesSize")
    TargetFilesCount = fields.String(load_from="TargetFilesCount")
    TargetSizeString = fields.String(load_from="TargetSizeString")
    SourceFilesSize = fields.String(load_from="SourceFilesSize")
    SourceFilesCount = fields.String(load_from="SourceFilesCount")
    SourceSizeString = fields.String(load_from="SourceSizeString")
    LastBackupStarted = fields.DateTime(load_from="LastBackupStarted")
    LastBackupFinished = fields.DateTime(load_from="LastBackupFinished")


class BackupSchema(Schema):
    id = fields.String(load_from="ID", required=True, allow_none=False, validate=validate.Length(min=1))
    name = fields.String(required=True, load_from="Name")
    tags = fields.List(fields.String(), load_from="Tags", required=True, allow_none=True)
    targetURL = fields.String(required=True, load_from="TargetURL")
    dbPath = fields.String(required=True, load_from="DBPath")
    sources = fields.String(load_from="Sources", allow_none=True, required=True)
    settings = fields.String(load_from="Settings", allow_none=True, required=True)
    filters = fields.String(load_from="Filters", allow_none=True, required=True)
    metadata = fields.Nested(MetadataSchema, load_from="Metadata", allow_none=True, required=True)
    isTemporary = fields.Boolean(required=True, load_from="IsTemporary")


class BackupAPISchema(Schema):
    schedule = fields.Nested(ScheduleSchema, load_from="Schedule", required=True)
    backup = fields.Nested(BackupSchema, load_from="Backup", required=True)

    @post_load()
    def make_user(self, data):
        return backups.Backup(data)