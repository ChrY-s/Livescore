import tornado.websocket
import asyncio

from Livescore.backend.match_updater import match_updater

# stadiums = numero partite inizializzate contemporaneamente
stadiums = 2

clients = set()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class DetailHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("details.html")


class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("WebSocket aperto")
        clients.add(self)

    def on_close(self):
        print("WebSocket chiuso")
        clients.remove(self)


async def main():
    # Creo l'app web
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/ws", WSHandler),
            (r"/details", DetailHandler)
        ],
        template_path="templates",
    )

    app.listen(8888)
    print("Server Tornado avviato su http://localhost:8888")

    # Faccio partire l'updater
    asyncio.create_task(match_updater())

    # Avvio i publisher delle partite
    # asyncio.create_task(run_matches(stadiums))

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
