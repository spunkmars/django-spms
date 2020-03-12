# coding=utf-8

from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


user = 'admin'
payload = jwt_payload_handler(user)
token = jwt_encode_handler(payload)

print(token)

