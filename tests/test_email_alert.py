# tests/test_email_alert.py

import unittest
from unittest import skipIf
from unittest.mock import patch, MagicMock
from src.email_alert import EmailAlert

class TestEmailAlert(unittest.TestCase):
    @skipIf(True, 'Skip this test')
    @patch('src.email_alert.smtplib.SMTP')
    @patch('src.email_alert.ConfigManager')
    def test_send_email_alert(self, MockConfigManager, MockSMTP):
        mock_smtp = MockSMTP.return_value
        mock_config = MockConfigManager.return_value
        mock_config.config = {
            'EMAIL': {
                'SmtpServer': 'smtp.example.com',
                'SmtpPort': 587,
                'FromAddress': 'your_email@example.com',
                'ToAddress': 'admin@example.com',
                'Username': 'your_email@example.com',
                'Password': 'your_password'
            }
        }

        email_alert = EmailAlert()
        email_alert.send_email_alert('Test email message')

        msg = (
            'Content-Type: text/plain; charset="us-ascii"\n'
            'MIME-Version: 1.0\n'
            'Content-Transfer-Encoding: 7bit\n'
            'Subject: Error Alert\n'
            'From: your_email@example.com\n'
            'To: admin@example.com\n'
            '\n'
            'Test email message'
        )

        mock_smtp.sendmail.assert_called_once_with(
            'your_email@example.com',
            ['admin@example.com'],
            msg
        )

    @patch('src.email_alert.ConfigManager')
    @patch('src.email_alert.smtplib.SMTP')
    def test_sends_email_successfully(self, mock_smtp, mock_config_manager):
        mock_config_manager.return_value.get_smtp_server.return_value = 'smtp.example.com'
        mock_config_manager.return_value.get_smtp_port.return_value = 25
        mock_config_manager.return_value.get_from_address.return_value = 'from@example.com'
        mock_config_manager.return_value.get_to_address.return_value = 'to@example.com'

        mock_smtp_instance = MagicMock()
        mock_smtp.return_value = mock_smtp_instance
        mock_smtp_instance.sendmail = MagicMock()

        email_alert = EmailAlert()
        email_alert.send_email_alert('Test message')

        # Store the SMTP instance
        stored_smtp_instance = mock_smtp.return_value

        mock_smtp.assert_called_once_with('smtp.example.com', 25)
        stored_smtp_instance.sendmail.assert_called_once_with(
            'from@example.com', ['to@example.com'],
            'Content-Type: text/plain; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\nSubject: Error Alert\nFrom: from@example.com\nTo: to@example.com\n\nTest message'
        )

    @patch('src.email_alert.ConfigManager')
    @patch('src.email_alert.smtplib.SMTP')
    def test_handles_smtp_exception(self, mock_smtp, mock_config_manager):
        mock_config_manager.return_value.get_smtp_server.return_value = 'smtp.example.com'
        mock_config_manager.return_value.get_smtp_port.return_value = 25
        mock_config_manager.return_value.get_from_address.return_value = 'from@example.com'
        mock_config_manager.return_value.get_to_address.return_value = 'to@example.com'

        mock_smtp.side_effect = Exception('SMTP error')

        email_alert = EmailAlert()
        with self.assertLogs(level='ERROR') as log:
            email_alert.send_email_alert('Test message')
            self.assertIn('Failed to send email alert: SMTP error', log.output[0])


if __name__ == '__main__':
    unittest.main()