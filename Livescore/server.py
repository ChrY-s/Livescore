import tornado.websocket
import asyncio

from backend.match_updater import match_updater, clients


class MainHandler(tornado.web.RequestHandler):
    def get(self, match_id = 0):
        if match_id == 0:
            self.render("index.html")
        else:
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
            (r"/([0-9]+)", MainHandler),
            (r"/ws", WSHandler),
            (r"/(.*)", tornado.web.StaticFileHandler, {"path": "frontend/templates"}),
        ],
        template_path="frontend/templates",
    )

    app.listen(8888)
    print("Server Tornado avviato su http://localhost:8888")

    # Faccio partire l'updater
    asyncio.create_task(match_updater())

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
