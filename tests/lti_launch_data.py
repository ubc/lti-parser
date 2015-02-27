# coding=utf-8
"""
Provides example data of LTI launches to test the parser against.

Template:
{
    "secrets": {
        "key": "secret"
    }
    "method": "",
    "url": "",
    "http_headers": {},
    "get_params": {},
    "post_params": {}
}
"""

# Webwork launch using the Basic LTI Building Block
webwork_blti_launch = {
    "secrets": {
        "lti_secret": "secret"
    },
    "method": "POST",
    "url": "http://webworkdev1.elearning.ubc.ca:8080/webwork2/",
    "http_headers": {
            "Host": "webworkdev1.elearning.ubc.ca:8080",
            "Connection": "keep-alive",
            "Content-Length": "1783",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Origin": "http://137.82.12.84",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "http://137.82.12.84/webapps/osc-BasicLTI-BBLEARN/window.jsp?lti_page=ctools&course_id=_201_1&id=webworkdev&if=true",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-GB,en-US;q=0.8,en;q=0.6",
            "Cookie": "WeBWorKCourseAuthen.admin=admin%09R2gpmYuP1VcTjh50LlPWcRWNdWIvM9t0%091421193276; WeBWorKCourseAuthen.MATH101-201_2012W2=admin%09fYN1RBWTx30VHKguHWEVbodyQhSGCcCc%091421278630"
    },
    "get_params": {},
    "post_params": {
        'ext_lms': 'learn-9.1.130093',
        'tool_consumer_instance_url': 'http://137.82.12.84',
        'ext_ims_lis_resultvalue_sourcedids': 'decimal,percentage,ratio,passfail,letteraf,letterafplus,freetext',
        'oauth_consumer_key': 'lti_secret',
        'tool_consumer_info_product_family_code': 'learn',
        'oauth_signature': 'cbxlc8O7Gzqo2rYBu+LvUyPp19c=',
        'tool_consumer_instance_name': 'ubc',
        'tool_consumer_instance_description': 'University of British Columbia',
        'context_id': 'CL.UBC.MATH.101.201.2012W2.13204',
        'oauth_callback': 'about:blank',
        'launch_presentation_return_url': 'http://137.82.12.84/webapps/osc-BasicLTI-BBLEARN/return.jsp?id=webworkdev&course_id=_101_1&lti_page=ctools',
        'oauth_version': '1.0',
        'oauth_signature_method': 'HMAC-SHA1',
        'roles': 'Instructor',
        'lis_outcome_service_url': 'http://137.82.12.84/webapps/osc-BasicLTI-BBLEARN/service',
        'tool_consumer_instance_guid': 'lti_secret',
        'lis_person_name_full': 'John Hsu,ø',
        'context_label': 'CL.UBC.MATH.101.201.2012W2.13204',
        'ext_ims_lis_memberships_id': ':_101_1::webworkdev:1423873410',
        'lti_version': 'LTI-1p0',
        'user_id': '',
        'launch_presentation_document_target': 'iframe',
        'oauth_timestamp': '1423873410',
        'context_title': '2012W2-MATH101-201- Integral Calculus with Applications to Physical Sciences and Engineering-Instructors',
        'lis_person_sourcedid': 'john',
        'resource_link_title': 'webworkdev',
        'ext_ims_lis_memberships_url': 'http://137.82.12.84/webapps/osc-BasicLTI-BBLEARN/extension',
        'oauth_nonce': '12997106392824',
        'lis_course_offering_sourcedid': 'CL.UBC.MATH.101.201.2012W2.13204',
        'lti_message_type': 'basic-lti-launch-request',
        'tool_consumer_info_version': '9.1.130093',
        'launch_presentation_locale': 'en_GB',
        'lis_person_name_family': 'Hsu,ø',
        'lis_person_name_given': 'John',
        'ext_ims_lis_basic_outcome_url': 'http://137.82.12.84/webapps/osc-BasicLTI-BBLEARN/extension',
        'context_type': 'CourseSection',
        'lis_course_section_sourcedid': 'CL.UBC.MATH.101.201.2012W2.13204',
        'resource_link_id': 'CL.UBC.MATH.101.201.2012W2.13204'
    }
}

