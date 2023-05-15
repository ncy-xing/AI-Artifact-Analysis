class Article:

    def __init__(self, title, date, body):
        self.title = title
        self.date = date
        self.body = body

    def __str__(self):
        return f"title: {self.title}\ndate: {self.date}\nbody len: {len(self.body)}"