'''
Utilities for tasks to interact with the Mathematica kernel.
'''

from subprocess import check_output
from tempfile import NamedTemporaryFile


def run_mathematica(command):
    '''
    Runs a string command in a new Mathematica kernel and returns the output.

    Parameters
    ----------
    command : str
        The command to run. Must be a valid Mathematica language string.

    Returns
    -------
    str
        Output from the Mathematica kernel.

    Raises
    ------
    RuntimeError
        If the Mathematica kernel produces no output, indicating an error.
    '''
    print_command = 'Print[{}]'.format(command)  # Wrap command in a Print[]
    output = None

    with NamedTemporaryFile() as f:
        f.write(bytes(print_command, 'utf-8'))
        f.seek(0)
        output = check_output(['wolfram', '-script', f.name])

    if not output:
        raise RuntimeError('Invalid Mathematica code')

    return output.decode()
