# coding=utf-8

import unittest

import lti_launch_data
import oauth_data

from parser import Parser
from oauth_store import OAuthStore

def _get_parser(data):
    oauth_store = OAuthStore()
    for key, secret in data['secrets'].items():
        oauth_store.set_secret(key, secret)
    parser = Parser(data['method'], data["url"], data["http_headers"], 
        data["get_params"], data["post_params"], oauth_store)
    return parser

class TestOAuthSignature(unittest.TestCase):
    def test_signature_verification_using_basic_example(self):
        data = oauth_data.basic_example
        parser = _get_parser(data)
        self.assertTrue(parser.verify_signature(), 
           "OAuth signature verification should've been successful but failed.")

    def test_signature_verification_using_rfc5849_example(self):
        data = oauth_data.rfc_example
        parser = _get_parser(data)
        self.assertTrue(parser.verify_signature(), 
           "OAuth signature verification should've been successful but failed.")

    def test_signature_verification_using_non_ascii_example(self):
        data = oauth_data.non_ascii_example
        parser = _get_parser(data)
        self.assertTrue(parser.verify_signature(), 
            "OAuth signature verification should've been successful but failed.")

    def test_signature_verification_using_basic_lti_b2_webwork_launch_data(self):
        data = lti_launch_data.webwork_blti_launch
        parser = _get_parser(data)
        self.assertTrue(parser.verify_signature(), 
            "OAuth signature verification should've been successful but failed.")

