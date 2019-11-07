from crim.omas import meiinfo
from crim.omas import meislicer
from crim.omas.exceptions import CannotReadMEIException
from crim.omas.exceptions import BadApiRequest
from crim.omas.exceptions import CannotWriteMEIException
from crim.omas.exceptions import CannotAccessRemoteMEIException
from crim.omas.exceptions import UnknownMEIReadException
from crim.omas.exceptions import UnsupportedEncoding

from pymei import documentToText


def slice_from_file(mei_file, ema):
    # If an MEI file is request in full (all/all/@all), just return it as string
    if ema == 'all/all/@all':
        return mei_file

    measures, staves, beats = ema.split('/')

    try:
        parsed_mei = meiinfo.read_MEI(mei_file).getMeiDocument()
    except CannotReadMEIException as ex:
        print(ex.message)
        return mei_file

    try:
        slicer = meislicer.MeiSlicer(
            parsed_mei,
            measures,
            staves,
            beats
        )
        mei_slice = slicer.slice()
    except BadApiRequest as ex:
        print(ex.message)
        return mei_file
    except UnsupportedEncoding as ex:
        print(ex.message)
        return mei_file

    return documentToText(mei_slice)
