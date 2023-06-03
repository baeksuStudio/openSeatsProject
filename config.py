import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'openseats.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False



# secret KEY 가져오기
SECRET_KEY = os.environ.get('SECRET_KEY',str(1030))

# 파일 업로드 용량 제한하기 (16mb)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
