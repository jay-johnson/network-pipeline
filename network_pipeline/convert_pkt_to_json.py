import json
from collections import defaultdict
from spylunking.log.setup_logging import console_logger
from network_pipeline.utils import ppj
from network_pipeline.consts import DEBUG_PACKETS


log = console_logger(
    name='ptoj')


def convert_pkt_to_json(pkg):
    """ convert_pkt_to_json
    Inspired by:
    https://gist.githubusercontent.com/cr0hn/1b0c2e672cd0721d3a07/raw/9144676ceb12dbd545e6dce366822bbedde8de2c/pkg_to_json.py
    This function convert a Scapy packet to JSON

    :param pkg: A scapy package
    :type pkg: objects

    :return: A JSON data
    :rtype: dict()

    """
    results = defaultdict(dict)

    try:
        for index in range(0, len(pkg)):

            layer = pkg[index]

            # Get layer name
            layer_tmp_name = str(layer.__dict__["aliastypes"][0])
            layer_start_pos = layer_tmp_name.rfind(".") + 1
            layer_name = layer_tmp_name[layer_start_pos:-2].lower()

            # Get the layer info
            tmp_t = {}
            for default_x, y in layer.__dict__["default_fields"].items():

                x = "default_{}".format(default_x)

                if DEBUG_PACKETS:
                    log.info("default: key={} val={}".format(x, y))

                try:
                    tmp_t["hex_default_{}".format(default_x)] = y.hex()
                except Exception:

                    # http://python3porting.com/differences.html#long
                    if y and not isinstance(y, (str,
                                                int,
                                                int,
                                                float,
                                                list,
                                                dict)):
                        if x in tmp_t:
                            tmp_t[x].update(convert_pkt_to_json(y))
                        else:
                            tmp_t[x] = y
                    else:
                        tmp_t[x] = y
            # end of fields

            results[layer_name] = tmp_t

            try:
                tmp_t = {}
                for fields_x, y in layer.__dict__["fields"].items():

                    if DEBUG_PACKETS:
                        log.info("fields: key={} val={}".format(x, y))

                    if fields_x == "qd":
                        if y:
                            tmp_t["fields_qd"] = json.loads(
                                    convert_pkt_to_json(y))
                    elif fields_x == "ar":
                        if y:
                            tmp_t["fields_ar"] = json.loads(
                                    convert_pkt_to_json(y))
                    elif fields_x == "an":
                        if y:
                            tmp_t["fields_an"] = json.loads(
                                    convert_pkt_to_json(y))
                    elif fields_x == "arcount":
                        if y:
                            tmp_t["fields_arcount"] = json.loads(
                                    convert_pkt_to_json(y))
                    elif fields_x == "ns":
                        if y:
                            """
                            'ns': <DNSRR  rrname='ubuntu.com.'
                            type=SOA rclass=IN ttl=1345
                            rdata=b'\x03ns1\tcanonical
                            \xc0\x19\nhostmaster\xc02xHl\x8e
                            \x00\x00*0\x00\x00\x0e\x10\x00
                            \t:\x80\x00\x00\x0e\x10' |>,
                            """
                            tmp_t["fields_ns"] = str(y)
                    elif fields_x == "proto":
                        if y:
                            tmp_t[x] = y
                    elif fields_x == "flags":
                        if y:
                            tmp_t[x] = y
                    elif fields_x == "ack":
                        if y:
                            tmp_t[x] = y
                    elif fields_x == "id":
                        if y:
                            tmp_t[x] = y
                    elif fields_x == "window":
                        if y:
                            tmp_t[x] = y
                    elif fields_x == "dataofs":
                        if y:
                            tmp_t[x] = y
                    elif fields_x == "frag":
                        if y:
                            tmp_t[x] = y
                    elif fields_x == "reserved":
                        if y:
                            tmp_t[x] = y
                    elif fields_x == "ttl":
                        if y:
                            tmp_t[x] = y
                    elif fields_x == "chksum":
                        if y:
                            tmp_t[x] = y
                    elif fields_x == "options":
                        if y:
                            cur_d = {}
                            try:
                                test = dict(y)
                                if "EOL" in test:
                                    cur_d["EOL"] = test["EOL"]
                                if "NOP" in test:
                                    cur_d["NOP"] = test["NOP"]
                                if "MSS" in test:
                                    cur_d["MSS"] = test["MSS"]
                                if "WScale" in test:
                                    cur_d["WScale"] = test["WScale"]
                                if "SAckOK" in test:
                                    cur_d["SAckOK"] = \
                                            test["SAckOK"].decode("utf-8")
                                if "SAck" in test:
                                    cur_d["SAck"] = test["SAck"]
                                if "Timestamp" in test:
                                    if test["Timestamp"]:
                                        cur_d["Timestamp"] = \
                                            test["Timestamp"][0]
                                if "AltChkSum" in test:
                                    cur_d["AltChkSum"] = test["AltChkSum"]
                                if "AltChkSumOpt" in test:
                                    cur_d["AltChkSumOpt"] = \
                                            test["AltChkSumOpt"]
                                if "Mood" in test:
                                    cur_d["Mood"] = test["Mood"]
                                if "Experiment" in test:
                                    cur_d["Experiment"] = test["Experiment"]
                            except Exception as exct:
                                log.error(("1 Failed parsing "
                                           "{}={} ex={}")
                                          .format(x,
                                                  y,
                                                  exct))
                                cur_d = str(y)
                            # end of parsing cur_d
                            tmp_t["fields_{}".format(fields_x)] = cur_d
                    elif fields_x == "urgptr":
                        if y:
                            cur_d = {}
                            try:
                                for f in y:
                                    cur_f = "{}_{}".format(fields_x,
                                                           f)
                                    try:
                                        cur_d[cur_f] = y.decode("utf-8")
                                    except Exception:
                                        cur_d["hex_" + cur_f] = y[f].hex()
                            except Exception as exct:
                                log.error(("2 Failed parsing "
                                           "{}={} ex={}")
                                          .format(x,
                                                  y,
                                                  exct))
                                cur_d = y
                            # end of parsing cur_d
                            tmp_t["fields_{}".format(fields_x)] = cur_d
                    else:
                        x = "{}".format(fields_x)

                        try:
                            hex_key = "hex_field_{}".format(fields_x)
                            if fields_x == "load":
                                try:
                                    tmp_t["load"] = y.decode("utf-8")
                                except Exception:
                                    tmp_t[hex_key] = y.hex()
                            else:
                                tmp_t[hex_key] = y.hex()
                        except Exception:
                            # http://python3porting.com/differences.html#long
                            if y and not isinstance(y, (str,
                                                        int,
                                                        int,
                                                        float,
                                                        list,
                                                        dict)):
                                if x in tmp_t:
                                    tmp_t[x].update(convert_pkt_to_json(y))
                                else:
                                    tmp_t[x] = y
                            else:
                                tmp_t[x] = y
                    # end of special handling:
                    # qd
                results[layer_name] = tmp_t

            except KeyError:
                # No custom fields
                pass

    except Exception:
        # Package finish -> do nothing
        pass

    if "padding" in results:
        try:
            if "load" in results["padding"]:
                results["padding"]["load"] = \
                    results["padding"]["load"].encode("utf-8").hex()
        except Exception:
            log.error(("failed parsing padding={}")
                      .format(results["padding"]))
    # end of fixing padding

    if "raw" in results:
        try:
            if "load" in results["raw"]:
                results["raw"]["load"] = \
                    results["raw"]["load"].encode("utf-8").hex()
        except Exception:
            log.error(("failed parsing raw={}")
                      .format(results["raw"]))
    # end of fixing raw

    if DEBUG_PACKETS:
        log.debug("")
        log.debug("pre json serialization:")
        log.debug(results)
        log.debug("post json.dumps:")
        log.debug(ppj(results))
        log.debug("")
    else:
        log.info(ppj(results))

    return results
# end of convert_pkt_to_json.py
