# coding=utf-8
"""
Provide examples of OAuth data to test verification against.

Same template as LTI launch data.
"""

# Basic Example from OAuth 1.0 tutorial: http://nouncer.com/oauth/authentication.html
basic_example = {
    "secrets": {
        "dpf43f3p2l4k3l03":"kd94hf93k423kf44",
        "nnch734d00sl2jdk":"pfkkdhi9sl3r4s00"
    },
    "method": "GET",
    "url": "http://photos.example.net/photos?size=original&file=vacation.jpg",
    "http_headers": {
        'Host': 'photos.example.net:80',
        'Authorization': """OAuth realm="http://photos.example.net/photos",
            oauth_consumer_key="dpf43f3p2l4k3l03",
            oauth_token="nnch734d00sl2jdk",
            oauth_nonce="kllo9940pd9333jh",
            oauth_timestamp="1191242096",
            oauth_signature_method="HMAC-SHA1",
            oauth_version="1.0",
            oauth_signature="tR3%2BTy81lMeYAr%2FFid0kMTYa%2FWM%3D\""""
    },
    "get_params": {
        "size":"original",
        "file":"vacation.jpg"
    },
    "post_params": {
    }
}
# also an example from OAuth tutorial
non_ascii_example = {
    "secrets": {
        "dpf43f3++p+#2l4k3l03":"kd9@4h%%4f93k423kf44",
        "nnch734d(0)0sl2jdk":"pfkkd#hi9_sl-3r=4s00"
    },
    "method": "GET",
    "url": "http://PHOTOS.example.net:8001/Photos?type=%D7%90%D7%u2022%D7%u02DC%D7%u2022%D7%u2018%D7%u2022%D7%A1&scenario=%D7%AA%D7%90%D7%u2022%D7%A0%D7%u201D",
    "http_headers": {
        "Host": "photos.example.net:8001",
        "Authorization": """OAuth realm="http://PHOTOS.example.net:8001/Photos",
                        oauth_consumer_key="dpf43f3%2B%2Bp%2B%232l4k3l03",
                        oauth_token="nnch734d%280%290sl2jdk",
                        oauth_nonce="kllo~9940~pd9333jh",
                        oauth_timestamp="1191242096",
                        oauth_signature_method="HMAC-SHA1",
                        oauth_version="1.0",
                        oauth_signature="MH9NDodF4I%2FV6GjYYVChGaKCtnk%3D\""""
    },
    "get_params": {
        "type": "××•×˜×•×‘×•×¡",
        # space in string below is a non-breaking space char, not a regular space
        "scenario": "×ª××•× ×”"
    },
    "post_params": {
    }
}

# Example HTTP request from RFC5894, only for testing OAuth signature calculation
# Note that signature was recalculated using the oauth signature tutorial at:
# http://nouncer.com/oauth/authentication.html
# The original signature from the example in the rfc was inconsistent with
# itself when it was reproduced from example to example.
rfc_example = {
    "secrets": {
        "9djdj82h48djs9d2": "j49sk3j29djd",
        "kkk9d7dh3k39sjv7": "dh893hdasih9"
    },
    "method": "POST",
    "url": "http://example.com/request?b5=%3D%253D&a3=a&c%40=&a2=r%20b",
    "http_headers": {
        "Host": "example.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": """OAuth realm="Example",
                        oauth_consumer_key="9djdj82h48djs9d2",
                        oauth_token="kkk9d7dh3k39sjv7",
                        oauth_signature_method="HMAC-SHA1",
                        oauth_timestamp="137131201",
                        oauth_nonce="7d8f3e4a",
                        oauth_version="1.0",
                        oauth_signature="OB33pYjWAnf%2BxtOHN4Gmbdil168%3D\""""
    },
    "get_params": {
        "b5": "=%3D",
        "a3": "a",
        "c@": "",
        "a2": "r b"
    },
    "post_params": {
        "c2":"",
        "a3":"2 q"
    }
}

