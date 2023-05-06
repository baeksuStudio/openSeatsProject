import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'openseats.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "1030"

# 파일 업로드 용량 제한하기 (16mb)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
