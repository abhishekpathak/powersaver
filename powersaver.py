from sleepmodes import SleepModes
from utils import run_os_command
from activityinspector import ActivityInspector
import logging
import config


def put_to_sleep(sleep_time, sleep_mode):
    system_sleep_command = "rtc -s %s -m %s" % (sleep_time, sleep_mode)
    logging.debug("running the sleep command : %s" % system_sleep_command)
    run_os_command(system_sleep_command)


def check_server_active(activityinspector):
    """ Checks if overall, the server is active or not.

    Waterfall design of checking if everything is inactive.
    Aggressively, we do not check further is anything is found to be active.

    Args :
        activityinspector : activityinspector object

    Returns :
        True : if the server is active
        False : if the server is inactive
    """
    if activityinspector.inspect_samba().is_active():
        logging.info("samba is active.")
        return True
    else:
        logging.info("samba is inactive.")
    if activityinspector.inspect_sabnzbd().is_active():
        logging.info("sabnzbd is active.")
        return True
    else:
        logging.info("sabnzbd is inactive.")
    return False


def main():
    # configure the logging.
    numeric_log_level = getattr(logging, config.LOG_LEVEL.upper(), None)
    if not isinstance(numeric_log_level, int):
        raise ValueError('Invalid log level: %s' % config.LOG_LEVEL)
    logging.basicConfig(filename = config.LOG_FILE, level = numeric_log_level)

    logging.info("Running the powersaver... ")
    # Check for overall server activity. We'll need server reports.
    # We'll take the help of a specialist, an ActivityInspector for this.
    aci = ActivityInspector(sabnzbd_host = config.SERVER_IP, sabnzbd_port
    = config.SABNZBD_PORT, sabnzbd_api = config.SABNZBD_API_KEY, samba_host =
                            config.SERVER_IP)
    active = check_server_active(aci)

    # if inactive, put the server to sleep. Else, exit peacefully.
    if not active:
        logging.info("Server is inactive. Putting the server to sleep...")
        put_to_sleep(config.SLEEP_TIME, SleepModes[config.SLEEP_MODE])
    else:
        logging.info("Server is active. Doing nothing and exiting...")


if __name__ == "__main__":
    main()
