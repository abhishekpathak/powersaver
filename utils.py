import shlex
import subprocess
import logging


def run_os_command(command):
    """ feeds the command provided to it directly to the os to run as a
    process.

    If the command is simple, tries to run the command securely without a
    shell.
    Falls back to direct shell input in case of redirects and pipes.

    Args :
        command : string, the bash command to run
    Returns :
        Output of the command as a string, stripped of all leading spaces
        and new lines.
    Raises :
        CalledProcessError : error in running the command
    """
    logging.debug("Running OS command : %s " % command)
    if '|' in command or '>' in command or '<' in command or '&&' in command:
        proc = subprocess.Popen(command, shell = True,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                universal_newlines = True)
    else:
        proc = subprocess.Popen(shlex.split(command), shell = False,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                universal_newlines = True)
    try:
        out, err = proc.communicate()
        out, err = out.strip(), err.strip()
        logging.debug("output at stdout : %s " % out)
        logging.debug("output at stderr : %s " % err)
        return out
    except subprocess.CalledProcessError:
        logging.info("Error in running command : %s " % command)
