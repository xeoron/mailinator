# mailinator.py
import requests
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse, parse_qs

_BASE_URL = 'http://www.mailinator.com'
_URLS = {
            'mailbox'     : '/maildir.jsp?email={email}',
            'text_detail' : '/showmail2.jsp?email={email}&msgid={msg_id}'
        }
# prepend base url to all urls
for key, value in _URLS.iteritems():
    _URLS[key] = _BASE_URL + value


class MailinatorException(Exception):
    pass


class Letter(object):
    """ Class for mail from Mailinator """
    def __init__(self, email=None, msg_id=None, preview_from=None,
            preview_subject=None, preview_received=None):
        self.email = email

        if msg_id is None:
            raise MailinatorException('msg_id cannot be None')
        self.msg_id = msg_id

        self.preview_from = preview_from
        self.preview_subject = preview_subject
        self.preview_received = preview_received

    def __str__(self):
        value = self.__unicode__()
        return value.encode('utf-8')

    def __unicode__(self):
        if self.preview_subject:
            return unicode(self.preview_subject)
        elif self.subject:
            return unicode(self.subject)
        else:
            return "<Letter>"

    def fetch(self):
        """ Download letter data from mailinator """
        url = _URLS['text_detail'].format(email=self.email, msg_id=self.msg_id)
        request = requests.get(url)

        if request.status_code != 200:
            raise MailinatorException('Non-200 status code received when fetching email')

        raw_text = request.text
        self.text_raw = raw_text

        lines = raw_text.split('\r\n')
        # blank line indicates split from headers and message
        message_break = lines.index('')

        headers = lines[:message_break]
        message = lines[message_break + 1:]

        # store message
        # TODO: convert to markdown?
        self.message_html = ''.join(message)
        self.message_raw = '\r\n'.join(message)

        # parse headers
        self.headers_raw = headers
        self._parse_headers(headers)

    def _parse_headers(self, headers):
        """ Pull out the data we care about from the headers """
        for header in headers:
            pieces = header.split(':')

            if len(pieces) < 2:
                continue

            key = pieces[0].lower()
            value = ':'.join(pieces[1:]).strip()

            if key == 'from':
                self.from_address = value
            elif key == 'to':
                self.to_address = value
            elif key == 'subject':
                self.subject = value
            elif key == 'date':
                self.date = value


def get_mail(name):
    """ Given a name, return a list of emails for the email {name}@mailinator.com """
    request = requests.get(_URLS['mailbox'].format(email=name))

    if request.status_code != 200:
        raise MailinatorException('Non-200 status code received when fetching inbox')

    soup = BeautifulSoup(request.text)

    # emails are table rows
    html_letters = soup.find(id='inboxList').findAll('tr')[1:]
    letters = []

    # parse each letter into an object
    for html_letter in html_letters:
        tds = html_letter.findAll('td')

        if len(tds) == 1 and 'No messages' in tds[0].text:
            continue

        # assume we have 3 fields: (name, subject, date)
        if len(tds) < 3:
            continue

        from_name = tds[0].text
        subject = tds[1].text
        link = tds[1].find('a')['href']
        # urlparse magic to grab msgid param from href
        msg_id = int(parse_qs(urlparse(link).query)['msgid'][0])
        received = tds[2].text

        letters.append(Letter(email=name,
                              msg_id=msg_id,
                              preview_from=from_name,
                              preview_subject=subject,
                              preview_received=received))

    return letters
