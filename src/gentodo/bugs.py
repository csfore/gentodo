import bugzilla
from gentodo import config

class Bugs:

    def __init__(self):
        conf = config.Config()
        token = conf.get_token()
        self.urls = conf.get_urls()
        self.emails = conf.get_emails()
        
        self.bz = bugzilla.Bugzilla(self.urls[0], api_key=token)

    def get_assigned(self):
        query = self.bz.build_query(assigned_to=self.emails[0])
        result = self.bz.query(query)
        summaries = []
        for bug in result:
            summaries.append(bug.summary)

        return summaries

    def get_cced(self):
        query = self.bz.build_query(cc=self.emails[0])
        result = self.bz.query(query)
        summaries = []
        for bug in result:
            summaries.append(bug.summary)
        return summaries

    def get_reported(self):
        query = self.bz.build_query(reporter=self.emails[0])
        result = self.bz.query(query)
        summaries = []
        for bug in result:
            summaries.append(bug.summary)
        return summaries
