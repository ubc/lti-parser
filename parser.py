"""
OAuth, creating the signature base string requires gathering parameters from 3
sources:
    - Parameters in the OAuth HTTP Authorization header, excluding the realm parameter (don't know if this inclues other authorization params?)
    - Parameters in the HTTP POST request body (with a content-type of application/x-www-form-urlencoded). 
    - HTTP GET parameters
"""
from hashlib import sha1
import hmac
import logging
import urllib
import urllib2
from urlparse import urlparse

from validator import Validator

logger = logging.getLogger(__name__)

# LTI common params
# LTI v1 requires resource_link_id also
#lti_common_launch_schema = Schema({
#        Required('lti_message_type'): 'basic-lti-launch-request',
#        Required('lti_version'): ['LTI-1p0', 'LTI-2p0'],
#        Required('resource_link_id'): str
#    },
#    extra=True
#)
#lti_v2_common_schema = Schema({
#        Required('lti_message_type'): ['basic-lti-launch-request', 'ToolProxyRegistrationRequest'],
#        Required('lti_version'): 'LTI-2p0'
#    },
#    extra=True
#)

oauth_schema = {
    'oauth_consumer_key': {'required': True},
    'oauth_signature_method': {'required': True, 'values': ['HMAC-SHA1']},
    'oauth_timestamp': {'required': True, 'type': int},
    'oauth_nonce': {'required': True},
    'oauth_signature': {'required': True},
    'oauth_version': {'values': ['1.0']}, # oauth 1.0 specs say this is optional
    'oauth_callback': {}, # ignored by lti, can be any value
    'oauth_token': {} # ignored by lti, can be any value
}

class LTIParserError(Exception):
    pass
class SignatureVerificationError(LTIParserError):
    pass
class UnsupportedError(LTIParserError):
    pass

def _percent_encode(val):
    '''
    Percent encode strings according to RFC3986.

    Note: Due to url encoding stating that spaces should be encoded to '+' 
    instead of '%20', we can't use urllib.urlencode.

    urllib.quote doesn't have this problem, but it does leave '/' alone, we
    want '/' to be encoded too. So an additional parameter has to be passed 
    in to take '/' off the safe list.

    Also need to add '~' to the safe list, since apparently that's not considered
    safe by Python but the OAuth spec lists it as being safe.
    '''
    return urllib.quote(str(val), '~')

class Parser:
    '''
    Parses LTI requests.
    '''
    def __init__(self, method, url, http_headers, get_params, post_params, oauth_store):
        '''
        url - the url of of the LTI request target, must include http/https, does
            not include GET params, e.g.: http://example.com/some/path
            if not using the default ports, must include the port
        http_headers - http headers stored in a dict
        get_params - GET parameters stored in a dict
        post_params - POST parameters stored in a dict
        '''
        self.method = method
        self.url = url
        self.http_headers = http_headers
        self.get_params = get_params
        self.post_params = post_params
        self.oauth_store = oauth_store

    def verify_signature(self):
        """
        Check that the OAuth signature is valid. LTI uses OAuth 1.0 signing.
        """
        oauth_params = OAuthParams(
                self.http_headers, self.get_params, self.post_params)
        # build the signature base string
        method = _percent_encode(self.method.upper())
        url_parts = urlparse(self.url)
        # scheme and host part of the url must be lower case
        base_uri = url_parts.scheme.lower() +'://'+ url_parts.netloc.lower() + \
            url_parts.path
        base_uri = _percent_encode(base_uri)
        ## OAuth signature calculation requires that GET, POST, OAuth params
        ## to be combined and then sorted into order. 
        ## Problematic: OAuth params can be in HTTP header, so need to add it in.
        ##  but if OAuth params in GET or POST, will end up with duplicates.
        ## Edge case: POST and GET can have params with the same names. So have
        ## to allow that during sorting
        params = self.get_params.items() + self.post_params.items()
        if oauth_params.isInHttpHeader():
            params += oauth_params.get().items()
        # percent encode the name and value of each parameter
        encoded_params = []
        for param in params:
            if param[0] == 'oauth_signature': continue # can't use sig in base
            param=(_percent_encode(param[0]), _percent_encode(param[1]))
            encoded_params.append(param)
        # sort by byte order, key first, if identical key, then sort by val
        encoded_params.sort()
        # concat params into a single string
        params_str = ""
        for param in encoded_params:
            if params_str:
                params_str += '&'
            params_str += param[0] + '=' + param[1]
        # build base string
        basestr = method +'&'+ base_uri +'&'+ _percent_encode(params_str)

        client_secret=self.oauth_store.get_secret(oauth_params.get_client_key())
        token_secret = self.oauth_store.get_secret(oauth_params.get_token_key())
        client_secret = _percent_encode(client_secret)
        token_secret = _percent_encode(token_secret)

        secret = client_secret + "&" + token_secret
        hashed = hmac.new(secret, basestr, sha1)
        # The signature
        actual_sig = hashed.digest().encode("base64").rstrip('\n')
        expected_sig = oauth_params.get_signature()
        if actual_sig == expected_sig:
            return True
        return False

class OAuthParams:
    '''
    Retrives the OAuth parameters from wherever it's located.
    
    There are 3 possible places we can look for the OAuth headers:
    - Authorization header in http headers
        - Expecting the Authorization header to look like:
            Authorization: OAuth realm="Example",
                oauth_consumer_key="jd83jd92dhsh93js",
                oauth_token="hdk48Djdsa",
                oauth_signature_method="PLAINTEXT",
                oauth_verifier="473f82d3",
                oauth_signature="ja893SD9%26xyz4992k83j47x0b"
        - It might already be parsed into a list, if not, we'll have to do it
    - POST body
    - GET request - this is technically not in spec, not sure if we should
        support it except that webwork uses it
    '''
    def __init__(self, http_headers, get_params, post_params):
        self.oauth_params = {}
        self.found_in_http_headers = False # True if OAuth params in http headers
        validator = Validator(oauth_schema)
        auth_params = []
        if "Authorization" in http_headers:
            auth_val = http_headers["Authorization"]
            if isinstance(auth_val, list):
                auth_params = auth_val
            else: # have to parse the auth header values into a list
                auth_params = urllib2.parse_http_list(auth_val)
                auth_params = urllib2.parse_keqv_list(auth_params)
                # since these are raw headers, need to percent decode them
                auth_params = { urllib.unquote(key) : urllib.unquote(val) 
                        for key, val in auth_params.items() }
        # find out which set of params has OAuth fields in them
        oauth_params = None
        if validator.validate(post_params):
            oauth_params = post_params
        elif auth_params and validator.validate(auth_params):
            oauth_params = auth_params
            self.found_in_http_headers = True
        elif validator.validate(get_params):
            oauth_params = get_params
        else:
            raise SignatureVerificationError("Could not locate OAuth fields.")
        # filter out non-oauth fields
        self.oauth_params = {x: oauth_params[x] for x in validator.get_fields() 
                if x in oauth_params}

    def get(self):
        '''
        Returns all the OAuth parameters
        '''
        return self.oauth_params
    def get_signature(self):
        '''
        Returns the signature string.
        '''
        return self.oauth_params['oauth_signature']
    def get_client_key(self):
        '''
        Returns the oauth consumer key, this is the key to the client shared
        secret that is used to calculate the signature.
        '''
        return self.oauth_params['oauth_consumer_key']
    def get_token_key(self):
        '''
        Returns the oauth token key, which is used to retrieve the token secret
        that is used to calculate the signature.
        '''
        return self.oauth_params.get('oauth_token', '')

    def isInHttpHeader(self):
        return self.found_in_http_headers
