from flask_script import Manager
from app import create_app
from flask_migrate import MigrateCommand
import os

# 获取配置
config_name = os.environ.get('FLASK_CONFIG') or 'default'
app = create_app(config_name)

# 生成manage实例
manage = Manager(app)

# 配置迁移
manage.add_command('db',MigrateCommand)

# 启动
if __name__ == '__main__':
    manage.run()
