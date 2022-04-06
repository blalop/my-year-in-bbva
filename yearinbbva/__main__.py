import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

from app import app

app.run_server()
