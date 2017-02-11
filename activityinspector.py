import requests
import logging
from customexceptions import ApiError
import utils
from activityregisters import SabnzbdActivityRegister, SambaActivityRegister


class ActivityInspector(object):
    """ Checks and records the activities happening on the machine.

    This class will have information about the various programs typically
    running on the system.It will know how to communicate with these programs,
    and extract relevant information from them. If we want to know whether some
    service is running currently, what are its details, ActivityInspector is
    the guy to talk to.

    Attributes :
        sabnzbd_host : host IP of sabnzbd
        sabnzbd_port : port where sabnzbd api listens to
        sabnzbd_api : API key of sabnzbd
        samba_host : host where samba server is running
    """
    # TODO add couchpotato, sonarr, plex support (file renames etc. going on)

    def __init__(self, sabnzbd_host = "127.0.0.1", sabnzbd_port = 8080,
                 sabnzbd_api = None, samba_host = "127.0.0.1"):
        # TODO can we wrap all these in a config object somewhere?
        self.sabnzbd_host = sabnzbd_host
        self.sabnzbd_port = sabnzbd_port
        self.sabnzbd_api = sabnzbd_api
        self.samba_host = samba_host

    def inspect_sabnzbd(self):
        """ Checks on sabnzbd activities.

        Returns:
           a SabnzbdActivityRegister object

        Raises :
            API Error : Error code mentioned.
        """
        api_url = "http://%s:%d/sabnzbd/api?apikey=%s&output=json&mode" \
                  "=qstatus" \
                  % (self.sabnzbd_host, self.sabnzbd_port, self.sabnzbd_api)
        logging.debug("Checking status from : %s" % api_url)
        resp = requests.get(api_url)
        logging.debug("HTTP response code is %d." % resp.status_code)
        if resp.status_code != 200:
            logging.error("Error in api call. HTTP response code returned"
                           " : %d" % resp.status_code)
            raise ApiError("Error in api call. HTTP response code returned"
                           " : %d" % resp.status_code)
        snr = SabnzbdActivityRegister(resp.json()["jobs"])
        logging.debug("sabnzbd register prepared.")
        return snr

    def inspect_samba(self):
        """ Checks on samba activities.

        Returns :
            a SambaActivityRegister object
        """
        # TODO preferably use a library, don't assume localhost.
        clients_list_command = 'sudo smbstatus -p | sed -n 5p | tr -s " " ' \
                               '| cut -d" " -f4'
        logging.debug("inspecting samba...")
        output = utils.run_os_command(clients_list_command)
        clients = output.strip().split("\n")
        smr = SambaActivityRegister(clients)
        logging.debug("samba register prepared.")
        return smr
