import json
from ipaddress import IPv4Address
from unittest import TestCase, mock
from test import mock_response, mock_backup
import status


class test_status(TestCase):
    def test_determine_options_discovery(self):
        with mock.patch('discovery.requests.session') as mock_session:
            mock_resp = mock_response._mock_response(content=json.dumps(mock_backup.backup))
            mock_session.return_value = mock.MagicMock(get=mock.MagicMock(return_value=mock_resp))
            parsed = status.parameters(['--host', '10.0.0.100', 'discovery'])
            self.assertEqual(parsed.discovery, True)
            self.assertEqual(parsed.host.compressed, '10.0.0.100')
            self.assertIsInstance(parsed.host, IPv4Address)

    def test_determine_options_discovery_with_id_expect_exception(self):
        with mock.patch('discovery.requests.session') as mock_session:
            mock_resp = mock_response._mock_response(content=json.dumps(mock_backup.backup))
            mock_session.return_value = mock.MagicMock(get=mock.MagicMock(return_value=mock_resp))
            try:
                status.parameters(['--host', '10.0.0.100', 'discovery', 'id', '1'])
                self.fail("System should have exited")
            except SystemExit as se:
                self.assertEqual(se.code, 2)

    def test_determine_options_missing_id_and_discovery_expect_exception(self):
        with mock.patch('discovery.requests.session') as mock_session:
            mock_resp = mock_response._mock_response(content=json.dumps(mock_backup.backup))
            mock_session.return_value = mock.MagicMock(get=mock.MagicMock(return_value=mock_resp))
            try:
                status.parameters(['10.0.0.100'])
                self.fail("System should have exited")
            except SystemExit as se:
                self.assertEqual(se.code, 2)

    def test_determine_options_id(self):
        with mock.patch('discovery.requests.session') as mock_session:
            mock_resp = mock_response._mock_response(content=json.dumps(mock_backup.backup))
            mock_session.return_value = mock.MagicMock(get=mock.MagicMock(return_value=mock_resp))
            parsed = status.parameters(['--host', '10.0.0.100', 'id', '1'])
            self.assertEqual(parsed.id, 1)
            self.assertIsNone(vars(parsed).get('discovery'))
            self.assertEqual(parsed.host.compressed, '10.0.0.100')
            self.assertIsInstance(parsed.host, IPv4Address)