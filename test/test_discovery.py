import json
from unittest import TestCase, mock

import discovery
import backups
import test.mock_backup
from test import mock_response


class TestDiscovery(TestCase):

    def test_discovery_mock_request(self):
        with mock.patch('discovery.requests.session') as mock_session:
            mock_resp = mock_response._mock_response(content=json.dumps(test.mock_backup.backup))

            mock_session.return_value = mock.MagicMock(get=mock.MagicMock(return_value=mock_resp))
            result = discovery.discovery()
            self.assertIsInstance(result[0], backups.Backup)
            self.assertIsInstance(result[0], backups.Backup)
            self.failUnless(mock_session.return_value.get.return_value.cookies.get.called)

    def test_id_mock_request_valid_id(self):
        with mock.patch('discovery.requests.session') as mock_session:
            mock_resp = mock_response._mock_response(content=json.dumps(test.mock_backup.backup))

            mock_session.return_value = mock.MagicMock(get=mock.MagicMock(return_value=mock_resp))
            result = discovery.get_backup_details(1)
            self.assertIsInstance(result, backups.Backup)

    def test_id_mock_request_invalid_id(self):
        with mock.patch('discovery.requests.session') as mock_session:
            mock_resp = mock_response._mock_response(content=json.dumps(test.mock_backup.backup))

            mock_session.return_value = mock.MagicMock(get=mock.MagicMock(return_value=mock_resp))
            with self.assertRaises(discovery.BackupIdNotFound):
                discovery.get_backup_details(5)


