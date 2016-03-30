import requests


class MailGunEmail(object):
    def __init__(self, app=None):
        self.api_key = None
        self.domains = None
        self.mail = None
        self.name = None
        self.request_url = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.api_key = app.config['MAILGUN_API_KEY']
        self.mail = app.config['NO_REPLY_MAIL_ADDRESS']
        self.name = app.config['NO_REPLY_MAIL_NAME']
        self.request_url = app.config['REQUEST_URL']

    def send(self, recipient, subject, msg):
        return requests.post(self.request_url,
                             auth=("api", self.api_key),
                             data={"from": "%s <%s>" % (self.name, self.mail),
                                   "to": recipient,
                                   "subject": subject,
                                   "html": msg})
