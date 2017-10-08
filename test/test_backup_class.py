import copy
import datetime
from unittest import TestCase

import models
import test.mock_backup


class TestBackupClass(TestCase):
    def test_get_data_model(self):
        self.assertEqual(models.get_model(test.mock_backup.backup[1]).errors, {})
        self.assertEqual(models.get_model(test.mock_backup.backup[0]).errors, {})

    def test_get_data_model_with_missing_field(self):
        moch = copy.deepcopy(test.mock_backup.backup[0])
        moch["Backup"]["ID"] = ""
        self.assertEqual(models.get_model(moch).errors, {'Backup': {'ID': ['Shorter than minimum length 1.']}})
        moch["Backup"].pop("ID", None)
        self.assertEqual(models.get_model(moch).errors, {'Backup': {'ID': ['Missing data for required field.']}})

    def test_init_backup_with_mock(self):
        backup = models.get_model(test.mock_backup.backup[0])
        self.assertEqual(backup.errors, {})
        self.assertEqual(backup.data.schedule.id, 1)
        self.assertEqual(backup.data.schedule.repeat.frequency, 1)
        self.assertEqual(backup.data.schedule.repeat.period, 'D')
        self.assertEqual(backup.data.schedule.lastRun, datetime.datetime(2017, 9, 15, 0, 0, 0, 0,
                                                                         tzinfo=datetime.timezone.utc))
        self.assertEqual(backup.data.schedule.rule,
                         "AllowedWeekDays=Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday")
        self.assertEqual(backup.data.schedule.allowedDays, ["mon", "tue", "wed", "thu", "fri", "sat", "sun"])

        self.assertEqual(backup.data.id, '1')
        self.assertEqual(backup.data.name, "test")
        self.assertEqual(backup.data.tags, [])
        self.assertEqual(backup.data.targetURL, "file://d:\\test")
        self.assertEqual(backup.data.dbPath, 'C:\\Users\\someuser\\AppData\\Local\\Duplicati\\FFHQUUONSJ.sqlite')
        self.assertEqual(backup.data.isTemporary, False)

    def test_is_backup_old(self):
        backup = models.get_model(test.mock_backup.backup[0])
        self.assertEqual(backup.errors, {})
        self.assertTrue(backup.data.is_backup_old())
        backup.data.schedule.repeat.period = "h"
        self.assertTrue(backup.data.is_backup_old(
            datetime.datetime(2017, 9, 18, 6, 1, 0, tzinfo=datetime.timezone.utc)))
        backup.data.schedule.repeat.period = "m"
        backup.data.schedule.repeat.frequency = 9
        self.assertTrue(backup.data.is_backup_old(
            datetime.datetime(2017, 9, 18, 1, 10, 0, tzinfo=datetime.timezone.utc)))
        backup.data.schedule.repeat.period = "M"
        backup.data.schedule.repeat.frequency = 1
        self.assertTrue(backup.data.schedule.is_backup_old(
            datetime.datetime(2017, 10, 20, 5, 0, 0, tzinfo=datetime.timezone.utc)))
        backup.data.schedule.repeat.period = "Y"
        backup.data.schedule.repeat.frequency = 1
        self.assertTrue(backup.data.schedule.is_backup_old(
            datetime.datetime(2018, 9, 16, 5, 0, 0, tzinfo=datetime.timezone.utc)))

    def test_is_backup_old_false_day(self):
        backup = models.get_model(test.mock_backup.backup[0])
        self.assertFalse(backup.data.schedule.is_backup_old(
            datetime.datetime(2017, 9, 15, 5, 0, 0, tzinfo=datetime.timezone.utc)))

    def test_is_backup_old_false_hour(self):
        backup = models.get_model(test.mock_backup.backup[0])
        backup.data.schedule.repeat.period = "h"
        self.assertFalse(backup.data.schedule.is_backup_old(
            datetime.datetime(2017, 9, 15, 0, 59, 0, tzinfo=datetime.timezone.utc)))

    def test_is_backup_old_false_minute(self):
        backup = models.get_model(test.mock_backup.backup[0])
        backup.data.schedule.repeat.period = "m"
        backup.data.schedule.repeat.frequency = 10
        self.assertFalse(backup.data.schedule.is_backup_old(
            datetime.datetime(2017, 9, 15, 0, 9, 0, tzinfo=datetime.timezone.utc)))

    def test_is_backup_old_false_month(self):
        backup = models.get_model(test.mock_backup.backup[0])
        backup.data.schedule.repeat.period = "M"
        backup.data.schedule.repeat.frequency = 1
        self.assertFalse(backup.data.schedule.is_backup_old(
            datetime.datetime(2017, 10, 14, 0, 0, 0, tzinfo=datetime.timezone.utc)))

    def test_is_backup_old_false_year(self):
        backup = models.get_model(test.mock_backup.backup[0])
        backup.data.schedule.repeat.period = "Y"
        backup.data.schedule.repeat.frequency = 1
        self.assertFalse(backup.data.schedule.is_backup_old(
            datetime.datetime(2018, 9, 14, 0, 0, 0, tzinfo=datetime.timezone.utc)))

    def test_is_backup_old_invalid_date(self):
        backup = models.get_model(test.mock_backup.backup[0])
        with self.assertRaises(ValueError):
            backup.data.schedule.is_backup_old("20150506 12:45:34")
