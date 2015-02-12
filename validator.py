"""
Generalized module for data validation. Provide a schema and it'll check if data
matches the schema.
"""

import logging

logger = logging.getLogger(__name__)

class ValidatorError(Exception):
    pass
class UnsupportedDataTypeError(ValidatorError):
    pass

class Validator:
    '''
    Given a schema and some data. Will check that the data agrees with the schema
    and emit warnings/errors where necessary.

    The schema is a dict with this format. Each field will have some default
    settings. If a setting is missing, then the default will be assumed.
    {
        'field': {
            'required': False, # whether to emit an error if field is absent
                                # note, does not guarantee value is not empty
            'type': str, # convert the field's value to these possible types:
                        # str, int, float, bool
            'recommended': False, # whether to emit a warning if field is missing
            'values': [] # accepted values for this field, accept any if empty
        }
    }
    '''
    def __init__(self, schema):
        '''
        Sets the schema for this validator.
        '''
        self.schema = schema

    def validate(self, data):
        '''
        Returns true if data matches against schema. False otherwise.
        '''
        for field, rules in self.schema.items():
            # ensure fields that are required exists
            required = rules.get('required', False)
            if required:
                if not field in data:
                    logging.debug("Missing required field: " + field)
                    return False
            # try to convert field to type desired, fail validation if we can't
            field_type = rules.get('type', str)
            if field in data and not isinstance(data[field], field_type):
                value = data[field]
                try:
                    if field_type == str:
                        value = str(value)
                    elif field_type == int:
                        value = int(value)
                    elif field_type == float:
                        value = float(value)
                    elif field_type == bool:
                        value = bool(value)
                    else:
                        msg = "Unknown data type for field '"+field+"'"
                        logging.error(msg)
                        raise UnsupportedDataTypeError(msg)
                except ValueError:
                    logging.debug("Can't convert data type in field: " + field)
                    return False
                data[field] = value
            # log warnings if a recommended field is missing
            recommended = rules.get('recommended', False)
            if recommended:
                if not field in data:
                    logging.warn("Recommended LTI field '"+field+"' is missing.")
            # ensure fields are restricted to specified values, if specified
            values = rules.get('values', [])
            if values:
                if field in data and not data.get(field) in values:
                    logging.debug("Invalid value in field: "+field)
                    return False
        return True

    def get_fields(self):
        '''
        Return a list of the fields that the schema is configured for.
        '''
        return self.schema.keys()

