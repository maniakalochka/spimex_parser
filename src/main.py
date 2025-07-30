import asyncio
from services.spimex_services import SpimexTradingService

async def main():
    await SpimexTradingService().run()

if __name__ == "__main__":
    asyncio.run(main())
