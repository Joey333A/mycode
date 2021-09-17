import json
import os

from aiohttp import web
import aiosqlite

HOST = os.getenv("MENU_HOST", "0.0.0.0")
PORT = os.getenv("MENU_PORT", 2227)
DB_FILE = os.getenv("DB_FILE", "menu.db")


def routes(app: web.Application) -> None:
    """
    These are the paths that may be appended to the URL.
    Each one has a Request type
    (get == GET, post == POST, put == PUT, delete == DELETE)
    and a different function is called for each type of request
    """

    app.add_routes(
        [
            web.get("/", menu),
            web.get("/menu", menu),
            web.put("/menu", update_menu),
            web.post("/menu", add_item),
            web.delete("/menu", delete_item)
        ]
    )


async def read_menu(search_item=None):
    """Read all of the information from the menu table of the database and return it as an iterable"""
    async with aiosqlite.connect(DB_FILE) as db:
        if search_item:
            sql = f"SELECT * FROM menu where item like '{search_item}'"
        else:
            sql = f"SELECT * FROM menu"
        data = await db.execute(sql)
        return await data.fetchall()


async def menu(request) -> json:
    """
    This will select everything from the menu table in the DB_FILE and return a JSON based web response
    """
    print(request)
    search = request.query.get('item')
    print(search)
    data = await read_menu(search)
    foods = []
    for food in data:
        foods.append({"item": food[0], "description": food[1], "price": food[2]})
    return web.json_response(foods)

async def add_item(request: web.Request) -> web.Response:
    print(request)
    post = await request.json()
    print(post)
    item = post['item']
    desc = post['description']
    price = post['price']
    sql = f"INSERT INTO MENU (item, description, price) VALUES ('{item}', '{desc}', {price});"
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(sql)
        await db.commit()
        return web.Response(body="Successfully Updated the Database")


async def update_menu(request: web.Request) -> web.Response:
    print(request)
    put = await request.json()
    print(put)
    item = put['item']
    desc = put['description']
    price = put['price']
    data = await read_menu()
    sql = ""
    for row in data:
        print(row)
        if item == row[0]:
            # If this item already exists, update the description and price
            sql = f"UPDATE MENU SET description = '{desc}', price = {price} where item like '{item}';"
        elif desc == row[1]:
            # If the description matches exactly, update the item name and the price
            sql = f"UPDATE MENU SET item = '{item}', price = {price} where description like '{desc}';"
        else:
            # If the item and desc do not exist, this is a new item to be added to the database
            sql = f"INSERT INTO MENU (item, description, price) VALUES ('{item}', '{desc}', {price});"
    if sql != "":
        async with aiosqlite.connect(DB_FILE) as db:
            await db.execute(sql)
            await db.commit()
            return web.Response(body="Successfully Updated the Database")

async def delete_item(request: web.Request) -> web.Response:
    """
    This function will read the 'item' query string and attempt to
    DELETE the value from the database
    """
    item = request.query.get('item')
    print(f"Trying to delete {item}")
    sql = f"DELETE FROM MENU WHERE item = '{item}'"
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(sql)
        await db.commit()
        return web.Response(body=f"Successfully Deleted {item} from the database")


def main():
    """
    This is the main process for the aiohttp server.

    This works by instantiating the app as a web.Application(),
    then applying the setup function we built in our routes
    function to add routes to our app, then by starting the async
    event loop with web.run_app().
    """

    print("This aiohttp web server is starting up!")
    app = web.Application()
    routes(app)
    web.run_app(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()


