import os
import sys
import json
import pandas as pd
from pandas.io.json import json_normalize
from celery_connectors.utils import ev
from spylunking.log.setup_logging import console_logger
from network_pipeline.utils import ppj
from network_pipeline.utils import rnow
from network_pipeline.build_packet_key import build_packet_key
from antinex_client.consts import SUCCESS
from antinex_client.consts import FAILED
from antinex_client.consts import ERROR
from antinex_client.consts import LOGIN_FAILED
from antinex_client.consts import ANTINEX_PUBLISH_ENABLED
from antinex_client.consts import ANTINEX_PUBLISH_REQUEST_FILE
from antinex_client.consts import ANTINEX_USE_MODEL_NAME
from antinex_client.consts import ANTINEX_URL
from antinex_client.consts import ANTINEX_USER
from antinex_client.consts import ANTINEX_MISSING_VALUE
from antinex_client.build_ai_client_from_env import build_ai_client_from_env
from antinex_client.generate_ai_request import generate_ai_request


log = console_logger(
        name='csv')


class RecordPacketsToCSV:
    """RecordPacketsToCSV"""

    def __init__(self):
        """__init__"""

        self.recv_msgs = []

        # save every nth number of messages
        self.save_after_num = int(
            ev("SAVE_AFTER_NUM",
               "100"))

        # shutdown after this number of messages
        self.stop_after_num = int(
            ev("STOP_AFTER_NUM",
               "-1"))

        if self.save_after_num < 0:
            self.save_after_num = 1
        if self.stop_after_num < 0:
            self.stop_after_num = None

        # shutdown if this file is found
        self.stop_for_file = ev(
                "STOP_FILE",
                "/tmp/stop-recording-csv")

        self.dataset_name = ev(
                "DS_NAME",
                "netdata")

        self.save_dir = ev(
                "DS_DIR",
                "/tmp")

        self.save_to_file = ev(
                "OUTPUT_CSV",
                "{}/{}-{}.csv".format(
                    self.save_dir,
                    self.dataset_name,
                    rnow("%Y-%m-%d-%H-%M-%S")))

        self.archive_file = ev(
                "ARCHIVE_JSON",
                "{}/packets-{}-{}.json".format(
                    self.save_dir,
                    self.dataset_name,
                    rnow("%Y-%m-%d-%H-%M-%S")))

        self.debug = bool(ev(
                "DEBUG_PACKETS",
                "0") == "1")

        self.df = None
        self.last_df = None

        self.eth_keys = {"eth_id": "id"}
        self.ip_keys = {"ip_id": "id"}
        self.ipvsix_keys = {"ipvsix_id": "id"}
        self.icmp_keys = {"icmp_id": "id"}
        self.arp_keys = {"arp_id": "id"}
        self.tcp_keys = {"tcp_id": "id"}
        self.udp_keys = {"udp_id": "id"}
        self.dns_keys = {"dns_id": "id"}
        self.raw_keys = {"raw_id": "id"}
        self.pad_keys = {"pad_id": "id"}
        self.all_keys = {}
        self.all_keys_list = []

        self.all_eth = []
        self.all_ip = []
        self.all_ipvsix = []
        self.all_icmp = []
        self.all_arp = []
        self.all_tcp = []
        self.all_udp = []
        self.all_dns = []
        self.all_raw = []
        self.all_pad = []
        self.all_flat = []
        self.all_rows = []

        # noqa https://github.com/jay-johnson/antinex-client/blob/5fbcefaaed3d979b3c0829447b61592d5910ef22/antinex_client/build_ai_client_from_env.py#L19
        self.client = build_ai_client_from_env()

        # the client uses environment variables:
        # noqa https://github.com/jay-johnson/antinex-client/blob/5fbcefaaed3d979b3c0829447b61592d5910ef22/antinex_client/consts.py#L23
        # here is an example of what to export:
        # noqa https://github.com/jay-johnson/antinex-client/blob/master/examples/example-prediction.env
        self.request_dict = {}
        if ANTINEX_PUBLISH_ENABLED:
            if os.path.exists(ANTINEX_PUBLISH_REQUEST_FILE):
                with open(ANTINEX_PUBLISH_REQUEST_FILE, "r") as f:
                    self.request_dict = json.loads(f.read())
        # if publishing is enabled

    # end of __init__

    def process_ether_frame(self,
                            id=None,
                            msg=None):
        """process_ether_frame

        Convert a complex nested json dictionary
        to a flattened dictionary and capture
        all unique keys for table construction

        :param id: key for this msg
        :param msg: ether frame for packet
        """

        # normalize into a dataframe
        df = json_normalize(msg)
        # convert to a flattened dictionary
        dt = json.loads(df.to_json())

        flat_msg = {}

        for k in dt:
            new_key = "eth_{}".format(k)
            flat_msg[new_key] = dt[k]["0"]
            if new_key not in self.eth_keys:
                self.eth_keys[new_key] = k
        # end of capturing all unique keys

        dt["eth_id"] = id
        self.all_eth.append(dt)

        log.debug("ETHER data updated:")
        log.debug(self.eth_keys)
        log.debug(self.all_eth)
        log.debug("")

        return flat_msg
    # end of process_ether_frame

    def process_ip_frame(self,
                         id=None,
                         msg=None):
        """process_ip_frame

        Convert a complex nested json dictionary
        to a flattened dictionary and capture
        all unique keys for table construction

        :param id: key for this msg
        :param msg: ip frame for packet
        """

        # normalize into a dataframe
        df = json_normalize(msg)
        # convert to a flattened dictionary
        dt = json.loads(df.to_json())

        flat_msg = {}

        for k in dt:
            new_key = "ip_{}".format(k)
            flat_msg[new_key] = dt[k]["0"]
            if new_key not in self.ip_keys:
                self.ip_keys[new_key] = k
        # end of capturing all unique keys

        dt["ip_id"] = id
        self.all_ip.append(dt)

        log.debug("IP data updated:")
        log.debug(self.ip_keys)
        log.debug(self.all_ip)
        log.debug("")

        return flat_msg
    # end of process_ip_frame

    def process_ipvsix_frame(self,
                             id=None,
                             msg=None):
        """process_ipvsix_frame

        Convert a complex nested json dictionary
        to a flattened dictionary and capture
        all unique keys for table construction

        :param id: key for this msg
        :param msg: ipv6 frame for packet
        """

        # normalize into a dataframe
        df = json_normalize(msg)
        # convert to a flattened dictionary
        dt = json.loads(df.to_json())

        flat_msg = {}

        for k in dt:
            new_key = "ipv6_{}".format(k)
            flat_msg[new_key] = dt[k]["0"]
            if new_key not in self.ipvsix_keys:
                self.ipvsix_keys[new_key] = k
        # end of capturing all unique keys

        dt["ipv6_id"] = id
        self.all_ipvsix.append(dt)

        log.debug("IPV6 data updated:")
        log.debug(self.ipvsix_keys)
        log.debug(self.all_ipvsix)
        log.debug("")

        return flat_msg
    # end of process_ip_frame

    def process_tcp_frame(self,
                          id=None,
                          msg=None):
        """process_tcp_frame

        Convert a complex nested json dictionary
        to a flattened dictionary and capture
        all unique keys for table construction

        :param id: key for this msg
        :param msg: tcp frame for packet
        """

        # normalize into a dataframe
        df = json_normalize(msg)
        # convert to a flattened dictionary
        dt = json.loads(df.to_json())

        flat_msg = {}

        for k in dt:
            new_key = "tcp_{}".format(k)
            flat_msg[new_key] = dt[k]["0"]
            if new_key not in self.tcp_keys:
                self.tcp_keys[new_key] = k
        # end of capturing all unique keys

        dt["tcp_id"] = id
        self.all_tcp.append(dt)

        log.debug("TCP data updated:")
        log.debug(self.tcp_keys)
        log.debug(self.all_tcp)
        log.debug("")

        return flat_msg
    # end of process_tcp_frame

    def process_udp_frame(self,
                          id=None,
                          msg=None):
        """process_udp_frame

        Convert a complex nested json dictionary
        to a flattened dictionary and capture
        all unique keys for table construction

        :param id: key for this msg
        :param msg: udp frame for packet
        """

        # normalize into a dataframe
        df = json_normalize(msg)
        # convert to a flattened dictionary
        dt = json.loads(df.to_json())

        flat_msg = {}

        for k in dt:
            new_key = "udp_{}".format(k)
            flat_msg[new_key] = dt[k]["0"]
            if new_key not in self.udp_keys:
                self.udp_keys[new_key] = k
        # end of capturing all unique keys

        dt["udp_id"] = id
        self.all_udp.append(dt)

        log.debug("UDP data updated:")
        log.debug(self.udp_keys)
        log.debug(self.all_udp)
        log.debug("")

        return flat_msg
    # end of process_udp_frame

    def process_dns_frame(self,
                          id=None,
                          msg=None):
        """process_dns_frame

        Convert a complex nested json dictionary
        to a flattened dictionary and capture
        all unique keys for table construction

        :param id: key for this msg
        :param msg: dns frame for packet
        """

        # normalize into a dataframe
        df = json_normalize(msg)
        # convert to a flattened dictionary
        dt = json.loads(df.to_json())

        flat_msg = {}

        for k in dt:
            new_key = "dns_{}".format(k)
            flat_msg[new_key] = dt[k]["0"]
            if new_key not in self.dns_keys:
                self.dns_keys[new_key] = k
        # end of capturing all unique keys

        dt["dns_id"] = id
        self.all_dns.append(dt)

        log.debug("DNS data updated:")
        log.debug(self.dns_keys)
        log.debug(self.all_dns)
        log.debug("")

        return flat_msg
    # end of process_dns_frame

    def process_icmp_frame(self,
                           id=None,
                           msg=None):
        """process_icmp_frame

        Convert a complex nested json dictionary
        to a flattened dictionary and capture
        all unique keys for table construction

        :param id: key for this msg
        :param msg: icmp frame for packet
        """

        # normalize into a dataframe
        df = json_normalize(msg)
        # convert to a flattened dictionary
        dt = json.loads(df.to_json())

        flat_msg = {}

        for k in dt:
            new_key = "icmp_{}".format(k)
            flat_msg[new_key] = dt[k]["0"]
            if new_key not in self.icmp_keys:
                self.icmp_keys[new_key] = k
        # end of capturing all unique keys

        dt["icmp_id"] = id
        self.all_icmp.append(dt)

        log.debug("ICMP data updated:")
        log.debug(self.icmp_keys)
        log.debug(self.all_icmp)
        log.debug("")

        return flat_msg
    # end of process_icmp_frame

    def process_arp_frame(self,
                          id=None,
                          msg=None):
        """process_arp_frame

        Convert a complex nested json dictionary
        to a flattened dictionary and capture
        all unique keys for table construction

        :param id: key for this msg
        :param msg: arp frame for packet
        """

        # normalize into a dataframe
        df = json_normalize(msg)
        # convert to a flattened dictionary
        dt = json.loads(df.to_json())

        flat_msg = {}

        for k in dt:
            new_key = "arp_{}".format(k)
            flat_msg[new_key] = dt[k]["0"]
            if new_key not in self.arp_keys:
                self.arp_keys[new_key] = k
        # end of capturing all unique keys

        dt["arp_id"] = id
        self.all_arp.append(dt)

        log.debug("ARP data updated:")
        log.debug(self.arp_keys)
        log.debug(self.all_arp)
        log.debug("")

        return flat_msg
    # end of process_arp_frame

    def process_raw_frame(self,
                          id=None,
                          msg=None):
        """process_raw_frame

        Convert a complex nested json dictionary
        to a flattened dictionary and capture
        all unique keys for table construction

        :param id: key for this msg
        :param msg: raw frame for packet
        """

        # normalize into a dataframe
        df = json_normalize(msg)
        # convert to a flattened dictionary
        dt = json.loads(df.to_json())

        flat_msg = {}

        for k in dt:
            new_key = "raw_{}".format(k)
            flat_msg[new_key] = dt[k]["0"]
            if new_key not in self.raw_keys:
                self.raw_keys[new_key] = k
        # end of capturing all unique keys

        dt["raw_id"] = id
        self.all_raw.append(dt)

        log.debug("RAW data updated:")
        log.debug(self.raw_keys)
        log.debug(self.all_raw)
        log.debug("")

        return flat_msg
    # end of process_raw_frame

    def process_pad_frame(self,
                          id=None,
                          msg=None):
        """process_pad_frame

        Convert a complex nested json dictionary
        to a flattened dictionary and capture
        all unique keys for table construction

        :param id: key for this msg
        :param msg: pad frame for packet
        """

        # normalize into a dataframe
        df = json_normalize(msg)
        # convert to a flattened dictionary
        dt = json.loads(df.to_json())

        flat_msg = {}

        for k in dt:
            new_key = "pad_{}".format(k)
            flat_msg[new_key] = dt[k]["0"]
            if new_key not in self.pad_keys:
                self.pad_keys[new_key] = k
        # end of capturing all unique keys

        dt["pad_id"] = id
        self.all_pad.append(dt)

        log.debug("PAD data updated:")
        log.debug(self.pad_keys)
        log.debug(self.all_pad)
        log.debug("")

        return flat_msg
    # end of process_pad_frame

    def build_flat_msg(self,
                       id=None,
                       msg=None):
        """build_flat_msg

        :param id: unique id for this message
        :param msg: message dictionary to flatten
        """

        flat_msg = {}

        if not id:
            log.error("Please pass in an id")
            return None
        if not msg:
            log.error("Please pass in a msg")
            return None

        for k in msg["data"]:
            if k == "ether":
                flat_msg.update(self.process_ether_frame(
                                    id=id,
                                    msg=msg["data"][k]))
            # end of ether
            elif k == "ip":
                flat_msg.update(self.process_ip_frame(
                                    id=id,
                                    msg=msg["data"][k]))
            # end of ip
            elif k == "ipv6":
                flat_msg.update(self.process_ipvsix_frame(
                                    id=id,
                                    msg=msg["data"][k]))
            # end of ipv6
            elif k == "tcp":
                flat_msg.update(self.process_tcp_frame(
                                    id=id,
                                    msg=msg["data"][k]))
            # end of tcp
            elif k == "udp":
                flat_msg.update(self.process_udp_frame(
                                    id=id,
                                    msg=msg["data"][k]))
            # end of udp
            elif k == "dns":
                flat_msg.update(self.process_dns_frame(
                                    id=id,
                                    msg=msg["data"][k]))
            # end of dns
            elif k == "icmp":
                flat_msg.update(self.process_icmp_frame(
                                    id=id,
                                    msg=msg["data"][k]))
            # end of icmp
            elif k == "arp":
                flat_msg.update(self.process_arp_frame(
                                    id=id,
                                    msg=msg["data"][k]))
            # end of arp
            elif k == "raw":
                flat_msg.update(self.process_raw_frame(
                                    id=id,
                                    msg=msg["data"][k]))
            # end of raw
            elif k == "padding":
                flat_msg.update(self.process_pad_frame(
                                    id=id,
                                    msg=msg["data"][k]))
            # end of pad
            else:
                log.error(("Unsupported frame type={} "
                           "please file an issue to track this "
                           "with data={} msg={}")
                          .format(k,
                                  ppj(msg["data"][k]),
                                  msg["data"]))
        # end of processing new message

        return flat_msg
    # end of build_flat_msg

    def build_all_keys_dict(self):
        """build_all_keys_dict"""

        log.info("finding keys")
        for k in self.eth_keys:
            ak = "{}".format(k)
            if ak not in self.all_keys:
                self.all_keys[ak] = k
        # end of building all eths
        for k in self.ip_keys:
            ak = "{}".format(k)
            if ak not in self.all_keys:
                self.all_keys[ak] = k
        # end of building all ips
        for k in self.ipvsix_keys:
            ak = "{}".format(k)
            if ak not in self.all_keys:
                self.all_keys[ak] = k
        # end of building all ipvsixs
        for k in self.icmp_keys:
            ak = "{}".format(k)
            if ak not in self.all_keys:
                self.all_keys[ak] = k
        # end of building all icmps
        for k in self.arp_keys:
            ak = "{}".format(k)
            if ak not in self.all_keys:
                self.all_keys[ak] = k
        # end of building all arps
        for k in self.tcp_keys:
            ak = "{}".format(k)
            if ak not in self.all_keys:
                self.all_keys[ak] = k
        # end of building all tcps
        for k in self.udp_keys:
            ak = "{}".format(k)
            if ak not in self.all_keys:
                self.all_keys[ak] = k
        # end of building all udps
        for k in self.dns_keys:
            ak = "{}".format(k)
            if ak not in self.all_keys:
                self.all_keys[ak] = k
        # end of building all dnss
        for k in self.raw_keys:
            ak = "{}".format(k)
            if ak not in self.all_keys:
                self.all_keys[ak] = k
        # end of building all raws
        for k in self.pad_keys:
            ak = "{}".format(k)
            if ak not in self.all_keys:
                self.all_keys[ak] = k
        # end of building all pads

        # this will be the columns for the csv
        for k in self.all_keys:
            self.all_keys_list.append(k)

        log.debug(("unique all_keys keys={} values={}")
                  .format(len(self.all_keys_list),
                          self.all_keys))

    # end of build_all_keys_dict

    def flatten_all(self):
        """flatten_all"""

        log.info("flattening - START")

        self.all_rows = []

        for idx, r in enumerate(self.all_flat):

            new_row = {"idx": idx}

            for k in self.all_keys_list:
                if k in r:
                    new_row[k] = r[k]
                else:
                    new_row[k] = None
            # end of for all keys

            self.all_rows.append(new_row)

        # end of all_keys

        log.info("flattening - END")
    # end of flatten_all

    def create_json_archive(self):
        """create_json_archive"""

        archive_data = {"packets": self.recv_msgs,
                        "dataset": self.dataset_name,
                        "num_packets": len(self.recv_msgs),
                        "created": rnow()}
        self.write_to_file(archive_data,
                           self.archive_file)

    # end of create_json_archive

    def convert_to_df(self):
        """convert_to_df"""

        log.info(("converting={}")
                 .format(len(self.all_rows)))

        if len(self.all_rows) == 0:
            return

        self.df = pd.DataFrame(self.all_rows).set_index("idx")

        if len(self.df) != len(self.all_rows):
            log.error(("Failed converting={} to rows={}")
                      .format(len(self.all_rows),
                              len(self.df)))
        else:
            log.info(("converted={} into rows={}")
                     .format(len(self.all_rows),
                             len(self.df)))

    # end of convert_to_df

    def write_to_file(self,
                      data_dict,
                      output_file_path):
        """write_to_file

        :param data_dict:
        :param output_file_path:
        """

        log.info("saving={}".format(output_file_path))
        with open(output_file_path, "w") as output_file:
            output_file.write(str(ppj(data_dict)))
    # end of write_to_file

    def save_df_as_csv(self):
        """save_df_as_csv"""

        if len(self.all_rows) == 0:
            log.info(("no df={} to save")
                     .format(self.df))
            return
        else:

            log.info(("saving "
                      "packets={} file={} rows={}")
                     .format(len(self.recv_msgs),
                             self.save_to_file,
                             len(self.df)))

            self.df.to_csv(self.save_to_file,
                           sep=",",
                           encoding="utf-8",
                           index=True)

            log.info(("done saving={}")
                     .format(self.save_to_file))
        # end of saving if the dataframe is there
    # end of save_df_as_csv

    def save_data(self):
        """save_data"""

        state = ""
        try:

            state = "create_json_archive"
            log.info("creating json archive")
            self.create_json_archive()

            state = "building_unique_keys"
            log.info("processing all unique keys")
            self.build_all_keys_dict()

            state = "flattening"
            log.info("flattening all data")
            self.flatten_all()

            state = "converting"
            log.info("converting to df")
            self.convert_to_df()

            state = "saving"
            log.info("saving to df")
            self.save_df_as_csv()

            if ANTINEX_PUBLISH_ENABLED:
                log.info(("publishing stream to rest={}")
                         .format(
                            ANTINEX_URL))
                self.publish_predictions_to_core()
            # end of if publishing to the core

        except Exception as e:
            log.error(("Failed state={} with ex={} to "
                       "save={}")
                      .format(state,
                              e,
                              self.save_to_file))
    # end of save_data

    def handle_msg(self,
                   body,
                   org_message):
        """handle_msg

        :param body: dictionary contents from the message body
        :param org_message: message object can ack, requeue or reject
        """

        if os.path.exists(self.stop_for_file):
            log.info(("Detected stop_file={} "
                      "shutting down")
                     .format(self.stop_for_file))

            # drop the message back in the queue
            # for next time
            org_message.requeue()

            sys.exit(1)
        # end of stop file detection

        try:

            log.debug(("handle body={}")
                      .format(ppj(body)))

            msg = body
            id = build_packet_key()
            recv_time = rnow()

            # this could be made into celery tasks...

            flat_msg = self.build_flat_msg(
                            id=id,
                            msg=msg)

            if not flat_msg:
                log.error(("Failed to build a flat message "
                           "for message={}")
                          .format(msg))
                return

            msg["id"] = id
            msg["received"] = recv_time
            if len(flat_msg) > 0:
                if self.debug:
                    log.info(ppj(flat_msg))
                flat_msg["id"] = id
                flat_msg["received"] = recv_time
                self.all_flat.append(flat_msg)
                self.recv_msgs.append(msg)
            # end of adding all flat messages

            already_saved = False
            num_recv = len(self.recv_msgs)
            if (num_recv % self.save_after_num) == 0:
                already_saved = False
                self.save_data()
            # end of saving a snapshot

            if self.stop_after_num:
                if num_recv >= self.stop_after_num:
                    if not already_saved:
                        self.save_data()
                    # avoid waiting on the save again
                    log.info("archive successful - purging buffer")
                    sys.exit(2)
                # shutdown - good for testing
            # if now set up for infinite consuming

        except Exception as e:
            log.error(("Failed processing msg={} "
                       "ex={}")
                      .format(body,
                              e))
        # end of processing message

        try:
            org_message.ack()
        except Exception as e:
            log.error(("Failed ack-ing msg={} "
                       "ex={}")
                      .format(body,
                              e))
        # end of acknowleding message was processed

        log.info("done handle")
    # end of handle_message

    def publish_predictions_to_core(self):
        """publish_predictions_to_core"""

        status = FAILED
        msg = "not started"

        try:

            msg = "generating request"
            log.info(msg)

            # noqa https://stackoverflow.com/questions/29815129/pandas-dataframe-to-list-of-dictionaries
            publish_req = generate_ai_request(
                predict_rows=self.df.fillna(
                    ANTINEX_MISSING_VALUE).to_dict("records"),
                req_dict=self.request_dict)

            if publish_req["status"] != SUCCESS:
                log.error(("failed generate_ai_request with err={}")
                          .format(
                            publish_req["error"]))
                status = ERROR

            else:

                msg = "publishing as user={} url={} model={}".format(
                    ANTINEX_USER,
                    ANTINEX_URL,
                    ANTINEX_USE_MODEL_NAME)

                log.info(msg)

                response = self.client.run_job(
                    body=publish_req["data"])

                if response["status"] == SUCCESS:
                    log.info("predictions sent")
                    status = SUCCESS
                elif response["status"] == FAILED:
                    log.error(("job failed with error='{}' with response={}")
                              .format(
                                response["error"],
                                response["data"]))
                    status = ERROR
                elif response["status"] == ERROR:
                    log.error(("job had an error='{}' with response={}")
                              .format(
                                response["error"],
                                response["data"]))
                    status = ERROR
                elif response["status"] == LOGIN_FAILED:
                    log.error(("job reported user was not able to log in "
                               "with an error='{}' with response={}")
                              .format(
                                response["error"],
                                response["data"]))
                    status = ERROR
                # logging for good/bad cases during publish
            # if generated a good request
        except Exception as e:
            log.error(("failed generating request last_step='{}' ex={}")
                      .format(
                        msg,
                        e))
        # end of try/ex

        return status
    # end of publish_predictions_to_core

# end of RecordPacketsToCSV
