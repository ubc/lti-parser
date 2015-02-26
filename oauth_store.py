class OAuthStoreError(Exception):
    pass
class OAuthStoreSaveError(OAuthStoreError):
    '''
    Throw this error if saving to the data store fails.
    '''
    pass

class OAuthStore:
    '''
    Base class for OAuth data storage.

    This is intended to abstract the actual details of the storage of data
    necessary for OAuth verification into a unified interface. A simple 
    implementation which stores the data in memory as a dict is provided. More
    complex implementations should inherit from this class and override 
    appropriate methods.
    '''
    def __init__(self):
        '''
        Inherited classes don't have to call this constructor. This is only
        for the in memory dict implementation.
        '''
        self.secrets = {}

    def set_secret(self, key, secret):
        '''
        Save a key and secret pair into the database.
        '''
        self.secrets[key] = secret

    def get_secret(self, key):
        '''
        Given a key, return the associated secret. If the key is unfamiliar,
        then just return an empty string.
        '''
        return self.secrets.get(key, "")

    def has_key(self, key):
        '''
        Returns true if we know key exists, false otherwise.
        '''
        return key in self.secrets

