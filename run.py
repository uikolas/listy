import app
from dotenv import load_dotenv

load_dotenv('.env')

application = app.create_app()

