from models import session, User, GroupUsers
import configparser
config = configparser.ConfigParser()
config.read('superuser.ini')
group = GroupUsers(str(config['DEFAULT']['namegroup']))
session.add(group)
user = User(str(config['DEFAULT']['username']), '', '', 1)
user.set_password(str(config['DEFAULT']['password']))
session.add(user)
session.commit()
