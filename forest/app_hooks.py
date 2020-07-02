import forest.main
import forest.cli.main
import forest.data as data


class DatabaseCallback:
    """Process to synchronize databases"""
    def __init__(self, file_groups):
        self.file_groups = file_groups

    def __call__(self):
        for group in self.file_groups:
            print(group)


def on_server_loaded(server_context):
    data.on_server_loaded()

    # Add periodic callback to keep database(s) up to date
    _, argv = forest.cli.main.parse_args()
    config = forest.main.configure(argv)
    interval_ms = 15 * 60 * 1000  # 15 minutes in miliseconds
    interval_ms = 60 * 1000  # 1 minute in miliseconds
    callback = DatabaseCallback(config.file_groups)
    server_context.add_periodic_callback(callback, interval_ms)


def on_session_destroyed(session_context):
    '''
    Function called when a session is closed 
    (e.g. tab closed or time out)
    '''
    if data.AUTO_SHUTDOWN:
        import sys 
        sys.exit('\033[1;31mThe session has ended - tab closed or timeout. \n\n --- Terminating the Forest progam and relinquishing control of port. ---\033[1;00m')
