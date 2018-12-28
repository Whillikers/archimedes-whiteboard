'''
Utilities for doing OCR via the Mathpix API.
'''

from archimedes_whiteboard.mathpix import credentials


def get_latex(image, allow_text=True, out_format='latex_simplified',
              min_confidence=None, min_char_confidence=None):
    '''
    Convert math and text in an image into LaTeX.

    If min_confidence is specified, raise a RuntimeError if the Mathpix
    confidence is below that threshold.

    Parameters
    ----------
    image : opencv BGR image
        The input image. Should be cropped to as small as possible and contain
        only math and text, clearly written.
    allow_text (optional) : bool
        If True, text will be recognized and put in a text LaTeX environment.
        Otherwise, text will be ignored.
    out_format (optional) : format field specified at https://docs.mathpix.com/
        Format to output. If using a format other than latex_simplified,
        output may contain \longdiv.
    min_confidence (optional) : number in [0, 1] or None
        If not None, the minimum confidence required to not raise a
        RuntimeError.
    min_char_confidence (optional) : number in [0, 1] or None
        If not None, the minimum per-character confidence required to not
        raise a RuntimeError.

    Returns
    -------
    str
        The contents of the image as a LaTeX string, or other supported format.
        The contents can be any symbol in https://docs.mathpix.com/#vocabulary,
        which may include the nonvalid LaTeX token \longdiv.

    Raises
    ------
    RuntimeError
        If min_confidence is specified and Mathpix yields too low a confidence.
    '''
    raise NotImplementedError('TODO')
