import unittest

from oauth_store import OAuthStore

class TestOAuthStore(unittest.TestCase):
    '''
    Test the built in basic in memory storage of the OAuthStore base class.
    '''
    def test_get_set_secret(self):
        '''
        Test getting the secret back from a key
        '''
        store = OAuthStore()
        # simple secret retrival test 
        expected_key = "expected key"
        expected_secret = "expected secret"
        store.set_secret(expected_key, expected_secret)
        self.assertTrue(store.has_key(expected_key))
        self.assertEqual(expected_secret, store.get_secret(expected_key))
        # unrecognized keys should return empty string for secret
        self.assertEqual("", store.get_secret("INVALID KEY"))
