import os

AMAZON_APPLICATION_ID = os.environ.get('AMAZON_APPLICATION_ID', '')

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SKILL_INVOCATION_NAME = 'the Roku'
SKILL_NAME = 'My Roku'
SKILL_VERSION = '0.2.0'

ROKU_ADDRESS = os.environ.get('ROKU_ADDRESS', '')
