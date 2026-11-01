from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Shared extensions are initialized by the application factory.
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
