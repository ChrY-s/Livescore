import json, asyncio

from backend.database import running_matches, scheduled_matches, ended_matches

clients = set()


# Funzione che trova tutti gli elementi di una collezione e li trasforma in una lista
async def read_collection(c):
    match_list = []

    async for m in c.find():
        match_list.append(m)

    return match_list


# Task che comunica tra DBe client WS
async def match_updater():
    while True:
        # Ricavo i dati dal DB
        rn = await read_collection(running_matches)
        nd = await read_collection(ended_matches)
        st = await read_collection(scheduled_matches)

        # Converto gli id BSON in STR
        for m in rn + nd + st:
            m["_id"] = str(m["_id"])
            m["schedule"] = str(m["schedule"])

        # Dati che invio alla pagina WS
        match_data = json.dumps({
            "live": rn,
            "end": nd,
            "start": st
        })

        # inoltro i dati ai client WebSocket
        for c in list(clients):
            await c.write_message(match_data)

        await asyncio.sleep(1)