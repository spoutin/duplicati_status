from unittest import TestCase
import backups


class OccurrenceTest(TestCase):
    def test_backupOccurrence_size_of_1_incorrect_size(self):
        occurrence = '1'
        from exceptions import UnknownRepeat
        with self.assertRaises(UnknownRepeat):
            backups.Backup.Schedule.Repeat.check_repeat(occurrence)

    def test_backupOccurrence_size_2_correct_size_correct_period(self):
        occurrence = '1D'
        self.assertTrue(backups.Backup.Schedule.Repeat.check_repeat(occurrence))

    def test_backupOccurrence_size_2_correct_size_incorrect_period(self):
        occurrence = '12'
        from exceptions import UnknownPeriod
        with self.assertRaises(UnknownPeriod):
            backups.Backup.Schedule.Repeat.check_repeat(occurrence)

    def test_backupOccurrence_size_2_correct_size_incorrect_frequency(self):
        occurrence = 'DD'
        from exceptions import UnknownFrequency
        with self.assertRaises(UnknownFrequency):
            backups.Backup.Schedule.Repeat.check_repeat(occurrence)
