class SlackResponse:

    @staticmethod
    def text(text):
        return text,None

    @staticmethod
    def attachment(title=None,image_url=None,pretext=None,text=None,author_name=None,author_link=None):
        attachment = {}

        if title is not None:
            attachment['title'] = title

        if image_url is not None:
            attachment['image_url'] = image_url

        if pretext is not None:
            attachment['pretext'] = pretext

        if text is not None:
            attachment['text'] = text

        if author_name is not None:
            attachment['author_name'] = author_name

        if author_link is not None:
            attachment['author_link'] = author_link

        return None,[attachment]
