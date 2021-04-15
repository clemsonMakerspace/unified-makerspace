from requests import Response

response_body = {
    'code': 200,
    'error': "EMAIL_IN_USE",
    'message': 'There is already an account '
               'with this email address.'
}