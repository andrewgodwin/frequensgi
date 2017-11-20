import aiohttp
import asyncio
import logging
from asgiref.server import StatelessServer

import frequensgi


logger = logging.getLogger(__name__)


class Server(StatelessServer):
    """
    APRS-IS server. Uses TCP.
    """

    software_name = "frequensgi"
    software_version = frequensgi.__version__

    def __init__(
            self,
            application,
            callsign,
            passcode,
            host=None,
            port=14580,
            max_applications=1000,
        ):
        super(Server, self).__init__(
            application=application,
            max_applications=max_applications,
        )
        # Parameters
        self.callsign = callsign
        self.passcode = passcode
        self.host = host or "rotate.aprs.net"
        self.port = port

    ### Mainloop and handling

    async def handle(self):
        """
        Main loop. Long-polls and dispatches updates to handlers.
        """
        # Open connection to APRS-IS server
        self.reader, self.writer = await asyncio.open_connection(
            host=self.host,
            port=self.port,
        )
        self.writer.write(b"user %s pass %s vers %s %s\r\n" % (
            self.callsign.encode("ascii"),
            self.passcode.encode("ascii"),
            self.software_name.encode("ascii"),
            self.software_version.encode("ascii"),
        ))
        await self.writer.drain()
        while True:
            line = await self.reader.readline()
            if not line.endswith(b"\n"):
                raise RuntimeError("Lost connection to APRS-IS")
            line = line.strip()
            print(line)

    async def application_send(self, scope, message):
        """
        Receives outbound sends from applications and handles them.
        """
        if message["type"] == "aprs.send_frame":
            #self.writer.write(frame + b"\r\n")
            await self.writer.drain()
        else:
            raise RuntimeError("Unknown outbound message type %s" % message["type"])
