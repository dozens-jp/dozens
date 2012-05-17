class DozensException(StandardError):

    def __init__(self, code):
        StandardError.__init__(self)
        self.code = code
