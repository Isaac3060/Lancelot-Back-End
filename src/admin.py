from flask_admin import Admin
import os
from flask_admin.contrib.sqla import ModelView
from models import Visit
from models import db,Visit, Business, Visitor
def setup_admin(app):
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='Lancelot', template_mode='bootstrap3')
    app.secret_key = os.environ.get('FLASK_APP_KEY','sample key')

    admin.add_view(ModelView(Visit, db.session))
    admin.add_view(ModelView(Business, db.session))
    admin.add_view(ModelView(Visitor, db.session))
