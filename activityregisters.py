import logging


class SabnzbdActivityRegister(object):
    """ Registers details of sabnzbd activity going on.

    Attributes :
        jobs : list of jobs that are running/in the queue.
    """

    def __init__(self, jobs):
        self.jobs = jobs

    def is_active(self):
        # TODO naive, can be made more complex by including more details
        """ Summarises sabnzbd details and tells us if it is active

         Returns :
            True : if sabnzbd is active
            False : if sabnzbd is not active
        """
        logging.debug("sabnzbd jobs found : %s" % (",".join(self.jobs)))
        return len(self.jobs) > 0


class SambaActivityRegister(object):
    """ Registers details of samba activity going on.

    Attributes :
        clients : list of client IPs that are connected.
    """

    def __init__(self, clients):
        self.clients = clients

    def is_active(self):
        # TODO naive, can be made more complex by including more details
        """ Summaries samba details and tells us if it is active

         Returns :
            True : if sabnzbd is active
            False : if sabnzbd is not active
        """
        logging.debug("samba clients found : %s" % (",".join(self.clients)))
        return len(self.clients) > 0
