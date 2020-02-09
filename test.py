import airflow
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser
user = PasswordUser(models.User())
user.username = 'fsalemag'
user.email = 'francisco.salema.g@gmail.com'
user.password = 'bgtyrtt1'
session = settings.Session()
session.add(user)
session.commit()
session.close()
exit()