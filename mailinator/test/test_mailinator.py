# test_mailinator.py
from mock import Mock, patch
import unittest

from mailinator import get_mail, Letter, MailinatorException


class RequestMock(Mock):
    """ Mock of the requests.Request object """
    def __init__(self, text=None, status_code=None, file_name=None):
        super(RequestMock, self).__init__()
        # if we got a file name, use that instead
        if file_name:
            with open(file_name, 'r') as f:
                self._text = f.read()
        else:
            self._text = text
        self._status_code = status_code

    @property
    def text(self):
        return Mock(return_value=self._text)()

    @property
    def status_code(self):
        return Mock(return_value=self._status_code)()


class test_get_mail(unittest.TestCase):
    def test_empty_mailbox(self):
        with patch('requests.get') as mock_request:
            mock_request.return_value = \
                RequestMock(status_code=200, file_name='test/html/inbox_empty.html')

            self.assertEqual(0, len(get_mail('pete')))

    def test_mailbox_with_emails(self):
        with patch('requests.get') as mock_request:
            mock_request.return_value = \
                RequestMock(status_code=200, file_name='test/html/inbox.html')

            self.assertNotEqual(0, len(get_mail('pete')))

    def test_mailbox_finds_all_emails(self):
        with patch('requests.get') as mock_request:
            mock_request.return_value = \
                RequestMock(status_code=200, file_name='test/html/inbox.html')

            self.assertEqual(16, len(get_mail('pete')))

    def test_mailbox_preview(self):
        with patch('requests.get') as mock_request:
            mock_request.return_value = \
                RequestMock(status_code=200, file_name='test/html/inbox.html')

            letters = get_mail('pete')

            letter = letters[0]
            self.assertEqual('Odis Rucker', letter.preview_from)
            self.assertTrue('Be Careful Using This Wonder!' in letter.preview_subject)
            self.assertEqual('03-04-2012 14:00', letter.preview_received)

            letter = letters[1]
            self.assertEqual('L.L.Bean', letter.preview_from)
            self.assertTrue("The Polo that's 5 Times" in letter.preview_subject)
            self.assertEqual('03-04-2012 14:07', letter.preview_received)

    def test_error_raise_on_status_code_404(self):
        with patch('requests.get') as mock_request:
            mock_request.return_value = \
                RequestMock(status_code=404, file_name='test/html/inbox.html')

            with self.assertRaises(MailinatorException):
                get_mail('pete')


class test_fetch_letter(unittest.TestCase):
    def test_basic_fetch(self):
        with patch('requests.get') as mock_request:
            mock_request.return_value = \
                RequestMock(status_code=200, file_name='test/html/detail_text.txt')

            l = Letter(email='pete', msg_id=5994491)
            l.fetch()

            self.assertTrue("Have A Big Curry!" in l.subject)
            self.assertTrue("Jackie Arroyo" in l.from_address)
            self.assertTrue("Healthcare Online" in l.message_html)

    def test_error_raise_on_status_code_404(self):
        with patch('requests.get') as mock_request:
            mock_request.return_value = \
                RequestMock(status_code=404, file_name='test/html/detail_text.txt')

            l = Letter(email='pete', msg_id=5994491)

            with self.assertRaises(MailinatorException):
                l.fetch()


if __name__ == '__main__':
    unittest.main()
