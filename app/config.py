import os

# 获取根目录
base_dir = os.path.abspath(os.path.dirname(__file__))


# 通用配置
class Config:
    # 秘钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_SERVE_LOCAL = True

    # 邮件配置
    MAIL_SERVER = 'smtp.163.com'
    MAIL_USERNAME = '14715908439@163.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'lwj209003'

    # 配置上传文件目录
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir,'static/upload')
    # 配置上传文件大小
    MAX_CONTENT_LENGTH = 1024*1024 * 10

    # 额外的初始化
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog.sqlite')


# 测试环境
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog.sqlite')


# 生产环境
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig

}
