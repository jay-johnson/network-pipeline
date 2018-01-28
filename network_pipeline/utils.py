import json
import datetime


def rnow(f="%Y-%m-%d %H:%M:%S"):
    """rnow

    :param f: format for the string
    """
    return datetime.datetime.now().strftime(f)
# end of rnow


def ppj(json_data):
    """ppj

    :param json_data: dictionary to print
    """
    return str(json.dumps(json_data,
                          sort_keys=True,
                          indent=4,
                          separators=(',', ': ')))
# end of ppj
