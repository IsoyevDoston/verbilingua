from environs import Env
import os
# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = str(os.environ.get("BOT_TOKEN"))  # Bot token
ADMINS = list(os.environ.get("ADMINS"))

CHANNELS = ["@Portifolio_Doston","-1001596165960"]

DB_USER = str(os.environ.get("DB_USER"))
DB_PASS = str(os.environ.get("DB_PASS"))
DB_NAME = str(os.environ.get("DB_NAME"))
DB_HOST = str(os.environ.get("DB_HOST"))