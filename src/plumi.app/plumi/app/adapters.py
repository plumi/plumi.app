class FavoriteConversation(object):
    def __init__(self, context):
        self.context = context
        self.total_comments = 0
    
    def enabled(self):
        return False
