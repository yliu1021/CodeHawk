import sys

import CLI
import settings


if __name__ == '__main__':
    try:
        if len(sys.argv) == 1:
            # Update settings
            settings.update_settings()
        elif len(sys.argv) == 2:
            # Run normally with CLI
            CLI.run(sys.argv[1])
        else:
            print('Received many arguments!', file=sys.stderr)
            exit(1)
    except KeyboardInterrupt:
        print()
