import aiosqlite
import asyncio
import os

DB_FILE = os.getenv("DB_FILE", "menu.db")

async def create_menu() -> bool:
    """
    This will create the menu table in the DB_FILE
    """
    async with aiosqlite.connect(DB_FILE) as db:
        sql = "CREATE TABLE IF NOT EXISTS MENU (item CHAR(50), description CHAR(250), price REAL);"
        await db.execute(sql)
    return True


if __name__ == "__main__":
    asyncio.run(create_menu())

