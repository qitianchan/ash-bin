import os
_basedir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(
                            os.path.dirname(__file__)))))

# LORIOT
GATEWAY_ID = "be7a009f"
LORIOT_TOKEN = "Rd6c66b0j2xi98cG6DW0Kg"
LORIOT_URL = "wss://ap1.loriot.io/app?id=" + GATEWAY_ID + "&token=" + LORIOT_TOKEN

# Default Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + _basedir + '/' + \
                          'test.sqlite'