import requests
import logging
from customexceptions import APIError
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

    def __init__(self, **kwargs):
        # TODO can we wrap all these in a config object somewhere?
        self.sabnzbd_host = kwargs.get("sabnzbd_host", "127.0.0.1")
        self.sabnzbd_port = kwargs.get("sabnzbd_port", 8080)
        self.sabnzbd_api  = kwargs.get("sabnzbd_api")
        self.samba_host   = kwargs.get("samba_host", "127.0.0.1")

    def _get_sabnzbd_queuedetails(self):
        """ Retrieves the queue details from sabnzbd

        Returns:
            dict with all the queue details

        Raises :
            API Error : Error code mentioned.
        """
        api = "http://%s:%d/sabnzbd/api?apikey=%s&output=json&mode=qstatus" \
            % (self.sabnzbd_host, self.sabnzbd_port, self.sabnzbd_api)
        logging.debug("Checking status from : %s" % api)
        resp = requests.get(api)
        logging.debug("HTTP response code is %d." % resp.status_code)
        if resp.status_code != 200:
            logging.error("Error in sabnzbd api call. HTTP response code "
                          "returned : %d" % resp.status_code)
            raise APIError("Error in sabnzbd api call. HTTP response code "
                           "returned: %d" % resp.status_code)
        else:
            return resp.json()

    def _get_samba_clients(self):
        """ Retrieves the clients list from samba

        Returns:
            list of all connected clients
        """
        # TODO preferably use a library, don't assume localhost.
        logging.debug("inspecting samba...")
        command = 'sudo smbstatus -p | sed -n 5p | tr -s " " | cut -d" " -f4'
        output = utils.run_os_command(command)
        return output.strip().split("\n")

    def inspect_sabnzbd(self):
        """ Checks on sabnzbd activities.

        Returns:
           a SabnzbdActivityRegister object.
        """
        sabnzbd_activity_register = SabnzbdActivityRegister(self._get_sabnzbd_queuedetails()["jobs"])
        logging.debug("sabnzbd register prepared.")
        return sabnzbd_activity_register

    def inspect_samba(self):
        """ Checks on samba activities.

        Returns :
            a SambaActivityRegister object
        """
        samba_register = SambaActivityRegister(self._get_samba_clients()["clients"])
        logging.debug("samba register prepared.")
        return samba_register
