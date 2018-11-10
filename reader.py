import imaplib
import traceback
import email
import credentials


class Reader:
    def __init__(self):
        # TODO Keep private!
        try:
            self.DOMAIN = credentials.DOMAIN
            self.EMAIL = credentials.EMAIL
            self.PWD = credentials.PWD
            self.SMTP_SERVER = credentials.SMTP_SERVER
            self.SMTP_PORT = credentials.SMTP_PORT
            self.mail = imaplib.IMAP4_SSL(self.SMTP_SERVER)
        except Exception as e:
            print("type error: " + str(e))
            print(traceback.format_exc())

    def get_mail(self):
        # Call this
        self._login()
        self.mail.select('inbox')
        self._process_mail()

    def _login(self):
        self.mail.login(self.EMAIL, self.PWD)

    def _process_mail(self):
        mail_type, data = self.mail.search(None, 'ALL')
        mail_ids = data[0]
        id_list = mail_ids.split()
        self._read_mail(id_list)

    def _read_mail(self, id_list):
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        for i in range(latest_email_id, first_email_id, -1):
            typ, data = self.mail.fetch(str(i), '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1].decode('cp1252'))

                    # TODO Move below to parser
                    # Potentially useful message keys: 'Delivered-To' 'Received' 'Date' 'From'
                    #                                  'To' 'Message-ID' 'Sender' 'Subject'
                    email_subject = msg['Subject']
                    email_from = msg['From']
                    print('From : ' + str(email_from) + '\n')
                    print('Subject : ' + str(email_subject) + '\n')
        self.mail.logout()

    # TODO Separate seminar/talk/workshop/misc


reader = Reader()
reader.get_mail()
