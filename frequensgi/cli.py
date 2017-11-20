import sys
import argparse
import logging
import importlib
from .server import Server


logger = logging.getLogger(__name__)


class CommandLineInterface(object):
    """
    Acts as the main CLI entry point for running the server.
    """

    description = "ASGI APRS-IS protocol server"

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description=self.description,
        )
        self.parser.add_argument(
            '-s',
            '--host',
            dest='host',
            help='APRS-IS server hostname',
            default=None,
        )
        self.parser.add_argument(
            '-f',
            '--full-feed',
            dest='full_feed',
            help='Request full feed (firehose) from APRS-IS server',
            action="store_true",
            default=False,
        )
        self.parser.add_argument(
            '-m',
            '--max-applications',
            dest='max_applications',
            help='Maximum number of application instances to allow at once',
            type=int,
            default=1000,
        )
        self.parser.add_argument(
            '-v',
            '--verbosity',
            type=int,
            help='How verbose to make the output',
            default=1,
        )
        self.parser.add_argument(
            'callsign',
            help='APRS callsign',
        )
        self.parser.add_argument(
            'passcode',
            help='APRS-IS passcode',
        )
        self.parser.add_argument(
            'application',
            help='The application to dispatch to as path.to.module:instance.path',
        )

        self.server = None

    @classmethod
    def entrypoint(cls):
        """
        Main entrypoint for external starts.
        """
        cls().run(sys.argv[1:])

    def run(self, args):
        """
        Pass in raw argument list and it will decode them
        and run the server.
        """
        # Decode args
        args = self.parser.parse_args(args)
        # Set up logging
        logging.basicConfig(
            level={
                0: logging.WARN,
                1: logging.INFO,
                2: logging.DEBUG,
            }[args.verbosity],
            format="%(asctime)-15s %(levelname)-8s %(message)s",
        )
        # Import application
        sys.path.insert(0, ".")
        application = self.import_by_path(args.application)
        # Start the server
        self.server = Server(
            application=application,
            callsign=args.callsign,
            passcode=args.passcode,
            host=args.host,
            port=10152 if args.full_feed else 14580,
            max_applications=args.max_applications,
        )
        self.server.run()

    @staticmethod
    def import_by_path(path):
        """
        Given a dotted/colon path, like project.module:ClassName.callable,
        returns the object at the end of the path.
        """
        module_path, object_path = path.split(":", 1)
        target = importlib.import_module(module_path)
        for bit in object_path.split("."):
            target = getattr(target, bit)
        return target
