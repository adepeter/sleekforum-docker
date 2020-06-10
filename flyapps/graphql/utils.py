class DictifyInput:
    """Serialize an input and convert to dictionary"""
    def __init__(self, input_arg):
        """Initialize class by passing the input to serialize as dict"""
        self.__serialize_input(input_arg)

    def __serialize_input(self, obj):
        """Protected method to convert each input to instance attribute"""
        for k, v in obj.items():
            setattr(self, k, v)

    def get_fields_or_field(self, instance, field=None):
        """Returns a dictionary of fields or get specific field"""
        if hasattr(self, instance):
            instance = getattr(self, instance, None)
            fields = self._dictify(instance)
            if field is not None:
                try:
                    return fields[field]
                except KeyError:
                    return None
            else:
                return fields
        else:
            raise AttributeError('%s is not a valid input' % instance)

    @staticmethod
    def _dictify(param):
        """Converts supplied param to dict"""
        return {field: value for field, value in param.items()}
