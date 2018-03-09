from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from zlkt import app
from exts import db
from models import User,Article

manager =  Manager(app)
#使用Migrate绑定APP和db
migrate = Migrate(app,db)
#添加迁移脚本的命令到manager中
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()