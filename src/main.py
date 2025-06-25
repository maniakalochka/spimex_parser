from database.db import init_db
from services.spimex_services import SpimexTradingService

if __name__ == "__main__":
    init_db()
    service = SpimexTradingService()
    service.run()
