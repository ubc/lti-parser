# coding=utf-8

from mock import patch
import unittest

from validator import Validator, UnsupportedDataTypeError

class TestValidator(unittest.TestCase):
    def test_get_fields(self):
        schema = {'field1': 'a', 'field2': 'b'}
        validator = Validator(schema)
        self.assertEqual(schema.keys(), validator.get_fields())

class TestValidtorValidate(unittest.TestCase):
    def test_validate_required_fields(self):
        # Validation when a required field is specified
        schema = {
            'this_field_should_be_required': {
                'required': True
            }
        }
        data_without_required = {
            'some_field': 'abc'
        }
        data_with_required = {
            'this_field_should_be_required': 'abc',
            'some_field': 'abc'
        }
        validator = Validator(schema)
        ## Should fail since field not present
        with patch('validator.logging') as mock_logging:
            self.assertFalse(validator.validate(data_without_required))
            mock_logging.debug.assert_called_with(
                "Missing required field: this_field_should_be_required")
        ## Should pass since field present
        self.assertTrue(validator.validate(data_with_required))
        
        # Validation passes when a field is explicitly set to not required
        schema = {
            'this_field_should_be_required': {
                'required': False
            }
        }
        validator = Validator(schema)
        self.assertTrue(validator.validate(data_without_required))

        # Validation passes when a field is implicitly defaulted to not required
        schema = {
            'this_field_should_be_required': {}
        }
        validator = Validator(schema)
        self.assertTrue(validator.validate(data_without_required))

    def test_validate_recommended_warnings(self):
        # Validate should log warnings if a recommended field is missing
        schema = {
            'recommended_field': {
                'recommended': True
            }
        }
        data = {
            'field': 'abc'
        }
        validator = Validator(schema)
        with patch('validator.logging') as mock_logging:
            validator.validate(data)
            mock_logging.warn.assert_called_with(
                "Recommended LTI field 'recommended_field' is missing.")

    def test_validate_type_conversion(self):
        # During validate, try to convert fields to specified type
        schema = {
            'field': {
                'type': int
            }
        }
        data = {
            'field': '1'
        }
        validator = Validator(schema)
        self.assertTrue(validator.validate(data))
        self.assertTrue(isinstance(data['field'], int))
        # Should fail validate if can't convert to specified type
        data = {
            'field': 'a'
        }
        with patch('validator.logging') as mock_logging:
            self.assertFalse(validator.validate(data))
            mock_logging.debug.assert_called_with(
                    "Can't convert data type in field: field")
        # Try to convert to a float
        schema = {'field': { 'type': float }}
        data = {'field': '3.14'}
        validator = Validator(schema)
        self.assertTrue(validator.validate(data))
        self.assertTrue(isinstance(data['field'], float))
        # Try to convert to a boolean
        schema = {'field': { 'type': bool }}
        data = {'field': 'True'}
        validator = Validator(schema)
        self.assertTrue(validator.validate(data))
        self.assertTrue(isinstance(data['field'], bool))
        # Try to convert to a str
        schema = {'field': { 'type': str }}
        data = {'field': 3.14}
        validator = Validator(schema)
        self.assertTrue(validator.validate(data))
        self.assertTrue(isinstance(data['field'], str))
        self.assertEqual(data['field'], "3.14")
        # Convert to an unsupported type
        schema = {'field': {'type': dict}}
        data = {'field': 'abc'}
        validator = Validator(schema)
        with self.assertRaises(UnsupportedDataTypeError):
            with patch('validator.logging') as mock_logging:
                validator.validate(data)
                mock_logging.warn.assert_called_with(
                        "Unknown data type for field 'field'")

    def test_validate_values(self):
        # Validation for limiting a field to a specific set of values
        schema = {
            'field': {
                'values': ['abc', 'def']
            }
        }
        data_with_wrong_values = {
            'field': 'hij'
        }
        data_with_right_values = {
            'field': 'def'
        }
        validator = Validator(schema)
        with patch('validator.logging') as mock_logging:
            self.assertFalse(validator.validate(data_with_wrong_values))
            mock_logging.debug.assert_called_with(
                    "Invalid value in field: field")
        self.assertTrue(validator.validate(data_with_right_values))

    def test_validate_multiple_restrictions(self):
        # put multiple restrictions on a field, see if it validates correctly
        schema = {
            'field': {
                'required': True,
                'type': int,
                'values': [1, 2]
            }
        }
        data_all_correct = {'field': '2'}
        data_missing_field = {'blah': 'abc'}
        data_wrong_type = {'field': 'abc'}
        data_wrong_value = {'field': '3'}
        validator = Validator(schema)
        self.assertTrue(validator.validate(data_all_correct))
        self.assertFalse(validator.validate(data_missing_field))
        self.assertFalse(validator.validate(data_wrong_type))
        self.assertFalse(validator.validate(data_wrong_value))

    def test_validate_multiple_fields(self):
        # check if validate deals with multiple fields properly
        schema = {
                'field1': {'required': True},
                'field2': {'required': True},
                'field3': {'type': int},
                'field4': {'values': ['abc']}
        }
        data_all_correct={'field1':'a','field2':'b','field3':'1','field4':'abc'}
        data_required_only = {'field1':'a', 'field2':'b'}
        data_missing_required = {'field1':'a'}
        data_wrong_type = {'field1':'a', 'field2':'b', 'field3':'c'}
        data_wrong_value = {'field1':'a', 'field2':'b', 'field4':'c'}
        validator = Validator(schema)
        self.assertTrue(validator.validate(data_all_correct))
        self.assertTrue(validator.validate(data_required_only))
        self.assertFalse(validator.validate(data_missing_required))
        self.assertFalse(validator.validate(data_wrong_type))
        self.assertFalse(validator.validate(data_wrong_value))


