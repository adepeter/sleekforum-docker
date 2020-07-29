class DuplicateDataEntryError(Exception):

    def __init__(self, text, *args, **kwargs):
        super().__init__(text, *args, **kwargs)
