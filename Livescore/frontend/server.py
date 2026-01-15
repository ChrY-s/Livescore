import tornado.websocket
import asyncio

from Livescore.backend.match_updater import match_updater, clients


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class DetailHandler(tornado.web.RequestHandler):
    def get(self, match_id):
        print("Richiesta reinderizzamento")
        self.render("details.html", id = match_id)


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
            (r"/details/([0-9]+)", DetailHandler)
        ],
        template_path="templates",
    )

    app.listen(8888)
    print("Server Tornado avviato su http://localhost:8888")

    # Faccio partire l'updater
    asyncio.create_task(match_updater())

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
