import os
from dtale.app import build_app
from flask_bootstrap import Bootstrap
from config import Config

additional_templates = os.path.join(os.path.dirname(__file__), "templates")
app = build_app(reaper_on=False, additional_templates=additional_templates)
app.config.from_object(Config)

bootstrap = Bootstrap(app)

#workaround to circular imports, as routes module needs to import the app variable
from app import routes