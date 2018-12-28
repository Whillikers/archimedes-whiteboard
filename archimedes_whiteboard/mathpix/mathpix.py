'''
Utilities for doing OCR via the Mathpix API.
'''

from archimedes_whiteboard.mathpix import credentials


def get_latex(image, min_confidence=None):
    '''
    Convert math and text in an image into LaTeX.

    If min_confidence is specified, raise a RuntimeError if the Mathpix
    confidence is below that threshold.

    Parameters
    ----------
    image : opencv BGR image
        The input image. Should be cropped to as small as possible and contain
        only math and text, clearly written.
    min_confidence (optional) : number in [0, 1] or None
        If not None, the minimum confidence required to not raise a
        RuntimeError.

    Returns
    -------
    str
        The contents of the image as a LaTeX string. The contents can be any
        symbol in https://docs.mathpix.com/#vocabulary, which may include
        the nonvalid LaTeX token \longdiv.

    Raises
    ------
    RuntimeError
        If min_confidence is specified and Mathpix yields too low a confidence.
    '''
    raise NotImplementedError('TODO')
