#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A pure python ping implementation using raw sockets.

(This is Python 3 port of https://github.com/jedie/python-ping)
(Tested and working with python 2.7, should work with 2.6+)

Note that ICMP messages can only be sent from processes running as root
(in Windows, you must run this script as 'Administrator').

Derived from ping.c distributed in Linux's netkit. That code is
copyright (c) 1989 by The Regents of the University of California.
That code is in turn derived from code written by Mike Muuss of the
US Army Ballistic Research Laboratory in December, 1983 and
placed in the public domain. They have my thanks.

Bugs are naturally mine. I'd be glad to hear about them. There are
certainly word - size dependencies here.

Copyright (c) Matthew Dixon Cowles, <http://www.visi.com/~mdc/>.
Distributable under the terms of the GNU General Public License
version 2. Provided with no warranties of any sort.

Original Version from Matthew Dixon Cowles:
   -> ftp://ftp.visi.com/users/mdc/ping.py

Rewrite by Jens Diemer:
   -> http://www.python-forum.de/post-69122.html#69122

Rewrite by George Notaras:
   -> http://www.g-loaded.eu/2009/10/30/python-ping/

Enhancements by Martin Falatic:
   -> http://www.falatic.com/index.php/39/pinging-with-python

Enhancements and fixes by Georgi Kolev:
   -> http://github.com/jedie/python-ping/

Bug fix by Andrejs Rozitis:
   -> http://github.com/rozitis/python-ping/

Revision history
~~~~~~~~~~~~~~~~
May 1, 2014
-----------
Little modifications by Mohammad Emami <emamirazavi@gmail.com>
- Added Python 3 support. For now this project will just support
   python 3.x
- Tested with python 3.3
- version was upped to 0.6

March 19, 2013
--------------
* Fixing bug to prevent divide by 0 during run-time.

January 26, 2012
----------------
* Fixing BUG #4 - competability with python 2.x [tested with 2.7]
   - Packet data building is different for 2.x and 3.x.
   'cose of the string/bytes difference.
* Fixing BUG #10 - the multiple resolv issue.
   - When pinging domain names insted of hosts (for exmaple google.com)
   you can get different IP every time you try to resolv it, we should
   resolv the host only once and stick to that IP.
* Fixing BUGs #3 #10 - Doing hostname resolv only once.
* Fixing BUG #14 - Removing all 'global' stuff.
   - You should not use globul! Its bad for you...and its not thread safe!
* Fix - forcing the use of different times on linux/windows for
        more accurate mesurments. (time.time - linux/ time.clock - windows)
* Adding quiet_ping function - This way we'll be able to use this script
    as external lib.
* Changing default timeout to 3s. (1second is not enought)
* Switching data syze to packet size. It's easyer for the user to ignore the
    fact that the packet headr is 8b and the datasize 64 will make packet with
    size 72.

October 12, 2011
--------------
Merged updates from the main project
    -> https://github.com/jedie/python-ping

September 12, 2011
--------------
Bugfixes + cleanup by Jens Diemer
Tested with Ubuntu + Windows 7

September 6, 2011
--------------
Cleanup by Martin Falatic. Restored lost comments and docs. Improved
functionality: constant time between pings, internal times consistently
use milliseconds. Clarified annotations (e.g., in the checksum routine).
Using unsigned data in IP & ICMP header pack/unpack unless otherwise
necessary. Signal handling. Ping-style output formatting and stats.

August 3, 2011
--------------
Ported to py3k by Zach Ware. Mostly done by 2to3; also minor changes to
deal with bytes vs. string changes (no more ord() in checksum() because
>source_string< is actually bytes, added .encode() to data in
send_one_ping()).  That's about it.

March 11, 2010
--------------
changes by Samuel Stauffer:
- replaced time.clock with default_timer which is set to
    time.clock on windows and time.time on other systems.

November 8, 2009
----------------
Improved compatibility with GNU/Linux systems.

Fixes by:
    * George Notaras -- http://www.g-loaded.eu
Reported by:
    * Chris Hallman -- http://cdhallman.blogspot.com

Changes in this release:
    - Re-use time.time() instead of time.clock(). The 2007 implementation
    worked only under Microsoft Windows. Failed on GNU/Linux.
    time.clock() behaves differently under the two OSes[1].

[1] http://docs.python.org/library/time.html#time.clock

May 30, 2007
------------
little rewrite by Jens Diemer:
    -  change socket asterisk import to a normal import
    -  replace time.time() with time.clock()
    -  delete "return None" (or change to "return" only)
    -  in checksum() rename "str" to "source_string"

December 4, 2000
----------------
Changed the struct.pack() calls to pack the checksum and ID as
unsigned. My thanks to Jerome Poincheval for the fix.

November 22, 1997
-----------------
Initial hack. Doesn't do much, but rather than try to guess
what features I (or others) will want in the future, I've only
put in what I need now.

December 16, 1997
-----------------
For some reason, the checksum bytes are in the wrong order when
this is run under Solaris 2.X for SPARC but it works right under
Linux x86. Since I don't know just what's wrong, I'll swap the
bytes always and then do an htons().

===========================================================================
IP header info from RFC791
    -> http://tools.ietf.org/html/rfc791)

0                   1                   2                   3
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |Type of Service|          Total Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|      Fragment Offset    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Time to Live |    Protocol   |         Header Checksum       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Source Address                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Destination Address                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options                    |    Padding    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

===========================================================================
ICMP Echo / Echo Reply Message header info from RFC792
    -> http://tools.ietf.org/html/rfc792

    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |     Type      |     Code      |          Checksum             |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |           Identifier          |        Sequence Number        |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |     Data ...
    +-+-+-+-+-

===========================================================================
ICMP parameter info:
    -> http://www.iana.org/assignments/icmp-parameters/icmp-parameters.xml

===========================================================================
An example of ping's typical output:

PING heise.de (193.99.144.80): 56 data bytes
64 bytes from 193.99.144.80: icmp_seq=0 ttl=240 time=127 ms
64 bytes from 193.99.144.80: icmp_seq=1 ttl=240 time=127 ms
64 bytes from 193.99.144.80: icmp_seq=2 ttl=240 time=126 ms
64 bytes from 193.99.144.80: icmp_seq=3 ttl=240 time=126 ms
64 bytes from 193.99.144.80: icmp_seq=4 ttl=240 time=127 ms

----heise.de PING Statistics----
5 packets transmitted, 5 packets received, 0.0% packet loss
round-trip (ms)  min/avg/max/med = 126/127/127/127

===========================================================================
"""

import os
import sys
import socket
import struct
import select
import time
import signal

__description__ = 'A pure python ICMP ping implementation using raw sockets.'

if sys.platform == "win32":
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time

NUM_PACKETS = 3
PACKET_SIZE = 64
WAIT_TIMEOUT = 3.0

# ICMP parameters

ICMP_ECHOREPLY = 0  # Echo reply (per RFC792)
ICMP_ECHO = 8  # Echo request (per RFC792)
ICMP_MAX_RECV = 2048  # Max size of incoming buffer

MAX_SLEEP = 1000


class MyStats:
    thisIP = "0.0.0.0"
    pktsSent = 0
    pktsRcvd = 0
    minTime = 999999999
    maxTime = 0
    totTime = 0
    avrgTime = 0
    fracLoss = 1.0


myStats = MyStats  # NOT Used globally anymore.


def checksum(source_string):
    """
    A port of the functionality of in_cksum() from ping.c
    Ideally this would act on the string as a series of 16-bit ints (host
    packed), but this works.
    Network data is big-endian, hosts are typically little-endian
    """
    countTo = (int(len(source_string) / 2)) * 2
    sum = 0
    count = 0

    # Handle bytes in pairs (decoding as short ints)
    loByte = 0
    hiByte = 0
    while count < countTo:
        if (sys.byteorder == "little"):
            loByte = source_string[count]
            hiByte = source_string[count + 1]
        else:
            loByte = source_string[count + 1]
            hiByte = source_string[count]
        try:     # For Python3
            sum = sum + (hiByte * 256 + loByte)
        except Exception:  # For Python2
            sum = sum + (ord(hiByte) * 256 + ord(loByte))
        count += 2

    # Handle last byte if applicable (odd-number of bytes)
    # Endianness should be irrelevant in this case
    if countTo < len(source_string):  # Check for odd length
        loByte = source_string[len(source_string) - 1]
        try:      # For Python3
            sum += loByte
        except Exception:   # For Python2
            sum += ord(loByte)

    # Truncate sum to 32 bits (a variance from ping.c, which
    # uses signed ints, but overflow is unlikely in ping)
    sum &= 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)    # Add high 16 bits to low 16 bits
    sum += (sum >> 16)                    # Add carry from above (if any)
    answer = ~sum & 0xffff                # Invert and truncate to 16 bits
    answer = socket.htons(answer)

    return answer


def do_one(myStats,
           destIP,
           hostname,
           timeout,
           mySeqNumber,
           packet_size,
           quiet=False):
    """do_one
    Returns either the delay (in ms) or None on timeout.

    :param myStats:
    :param destIP:
    :param hostname:
    :param timeout:
    :param mySeqNumber:
    :param packet_size:
    :param quiet:
    """
    delay = None

    try:
        # One could use UDP here, but it's obscure
        mySocket = socket.socket(socket.AF_INET,
                                 socket.SOCK_RAW,
                                 socket.getprotobyname("icmp"))
    except socket.error as e:
        print("failed. (socket error: '%s')" % e.args[1])
        raise  # raise the original error

    my_ID = os.getpid() & 0xFFFF

    sentTime = send_one_ping(mySocket, destIP, my_ID, mySeqNumber, packet_size)
    if not sentTime:
        mySocket.close()
        return delay

    myStats.pktsSent += 1

    recvTime, dataSize, iphSrcIP, icmpSeqNumber, iphTTL = \
        receive_one_ping(
            mySocket,
            my_ID,
            timeout)

    mySocket.close()

    if recvTime:
        delay = (recvTime - sentTime) * 1000
        if not quiet:
            print("%d bytes from %s: icmp_seq=%d ttl=%d time=%d ms" % (
                dataSize,
                socket.inet_ntoa(struct.pack("!I",
                                             iphSrcIP)),
                icmpSeqNumber,
                iphTTL,
                delay)
            )
        myStats.pktsRcvd += 1
        myStats.totTime += delay
        if myStats.minTime > delay:
            myStats.minTime = delay
        if myStats.maxTime < delay:
            myStats.maxTime = delay
    else:
        delay = None
        print("Request timed out.")

    return delay


def send_one_ping(mySocket, destIP, myID, mySeqNumber, packet_size):
    """
    Send one ping to the given >destIP<.
    """
    # destIP  =  socket.gethostbyname(destIP)

    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    # (packet_size - 8) - Remove header size from packet size
    myChecksum = 0

    # Make a dummy heder with a 0 checksum.
    header = struct.pack(
        "!BBHHH", ICMP_ECHO, 0, myChecksum, myID, mySeqNumber
    )

    padBytes = []
    startVal = 0x42
    # 'cose of the string/byte changes in python 2/3 we have
    # to build the data differnely for different version
    # or it will make packets with unexpected size.
    if sys.version[:1] == '2':
        bytes = struct.calcsize("d")
        data = ((packet_size - 8) - bytes) * "Q"
        data = struct.pack("d", default_timer()) + data
    else:
        for i in range(startVal, startVal + (packet_size - 8)):
            padBytes += [(i & 0xff)]  # Keep chars in the 0-255 range
        # data = bytes(padBytes)
        data = bytearray(padBytes)

    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)  # Checksum is in network order

    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack(
        "!BBHHH", ICMP_ECHO, 0, myChecksum, myID, mySeqNumber
    )

    packet = header + data

    sendTime = default_timer()

    try:
        # Port number is irrelevant for ICMP
        mySocket.sendto(packet, (destIP, 1))
    except socket.error as e:
        print("General failure (%s)" % (e.args[1]))
        return

    return sendTime


def receive_one_ping(mySocket, myID, timeout):
    """receive_one_ping
    Receive the ping from the socket. Timeout = in ms

    :param mySocket:
    :param myID:
    :param timeout:
    """
    timeLeft = timeout / 1000

    while True:  # Loop while waiting for packet or timeout
        startedSelect = default_timer()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (default_timer() - startedSelect)
        if whatReady[0] == []:  # Timeout
            return None, 0, 0, 0, 0

        timeReceived = default_timer()

        recPacket, addr = mySocket.recvfrom(ICMP_MAX_RECV)

        ipHeader = recPacket[:20]
        iphVersion, iphTypeOfSvc, iphLength, \
            iphID, iphFlags, iphTTL, iphProtocol, \
            iphChecksum, iphSrcIP, iphDestIP = struct.unpack(
                "!BBHHHBBHII", ipHeader
            )

        icmpHeader = recPacket[20:28]
        icmpType, icmpCode, icmpChecksum, \
            icmpPacketID, icmpSeqNumber = struct.unpack(
                "!BBHHH", icmpHeader
            )

        if icmpPacketID == myID:  # Our packet
            dataSize = len(recPacket) - 28
            # print (len(recPacket.encode()))
            return (timeReceived,
                    (dataSize + 8),
                    iphSrcIP,
                    icmpSeqNumber,
                    iphTTL)

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return None, 0, 0, 0, 0


def dump_stats(myStats):
    """
    Show stats when pings are done
    """
    print("\n----%s PYTHON PING Statistics----" % (myStats.thisIP))

    if myStats.pktsSent > 0:
        myStats.fracLoss = (myStats.pktsSent - myStats.pktsRcvd) \
                / myStats.pktsSent

    print(("%d packets transmitted, %d packets received, "
           "%0.1f%% packet loss") % (
        myStats.pktsSent,
        myStats.pktsRcvd,
        100.0 * myStats.fracLoss
    ))

    if myStats.pktsRcvd > 0:
        print("round-trip (ms)  min/avg/max = %d/%0.1f/%d" % (
            myStats.minTime,
            myStats.totTime / myStats.pktsRcvd,
            myStats.maxTime
        ))

    print("")
    return


def signal_handler(signum, frame):
    """
    Handle exit via signals
    """
    dump_stats()
    print("\n(Terminated with signal %d)\n" % (signum))
    sys.exit(0)


def verbose_ping(hostname, timeout=WAIT_TIMEOUT, count=NUM_PACKETS,
                 packet_size=PACKET_SIZE, path_finder=False):
    """
    Send >count< ping to >destIP< with the given >timeout< and display
    the result.
    """
    signal.signal(signal.SIGINT, signal_handler)   # Handle Ctrl-C
    if hasattr(signal, "SIGBREAK"):
        # Handle Ctrl-Break e.g. under Windows
        signal.signal(signal.SIGBREAK, signal_handler)

    myStats = MyStats()  # Reset the stats

    mySeqNumber = 0  # Starting value

    try:
        destIP = socket.gethostbyname(hostname)
        print("\nPYTHON PING %s (%s): %d data bytes" %
              (hostname, destIP, packet_size))
    except socket.gaierror as e:
        print("\nPYTHON PING: Unknown host: %s (%s)" %
              (hostname, e.args[1]))
        print()
        return

    myStats.thisIP = destIP

    for i in range(count):
        delay = do_one(myStats,
                       destIP,
                       hostname,
                       timeout,
                       mySeqNumber,
                       packet_size)

        if not delay:
            delay = 0

        mySeqNumber += 1

        # Pause for the remainder of the MAX_SLEEP period (if applicable)
        if (MAX_SLEEP > delay):
            time.sleep((MAX_SLEEP - delay) / 1000)

    dump_stats(myStats)


def quiet_ping(hostname, timeout=WAIT_TIMEOUT, count=NUM_PACKETS,
               packet_size=PACKET_SIZE, path_finder=False):
    """
    Same as verbose_ping, but the results are returned as tuple
    """
    myStats = MyStats()  # Reset the stats
    mySeqNumber = 0  # Starting value

    try:
        destIP = socket.gethostbyname(hostname)
    except socket.gaierror:
        return False

    myStats.thisIP = destIP

    # This will send packet that we dont care
    # about 0.5 seconds before it starts
    # acrutally pinging. This is needed in big
    # MAN/LAN networks where you sometimes
    # loose the first packet.
    # (while the switches find the way... :/ )
    if path_finder:
        fakeStats = MyStats()
        do_one(fakeStats, destIP, hostname, timeout,
               mySeqNumber, packet_size, quiet=True)
        time.sleep(0.5)

    for i in range(count):
        delay = do_one(myStats, destIP, hostname, timeout,
                       mySeqNumber, packet_size, quiet=True)

        if not delay:
            delay = 0

        mySeqNumber += 1

        # Pause for the remainder of the MAX_SLEEP period (if applicable)
        if (MAX_SLEEP > delay):
            time.sleep((MAX_SLEEP - delay) / 1000)

    if myStats.pktsSent > 0:
        myStats.fracLoss = (myStats.pktsSent - myStats.pktsRcvd) \
                            / myStats.pktsSent
    if myStats.pktsRcvd > 0:
        myStats.avrgTime = myStats.totTime / myStats.pktsRcvd

    # return tuple(max_rtt, min_rtt, avrg_rtt, percent_lost)
    return myStats.maxTime, myStats.minTime, myStats.avrgTime, myStats.fracLoss


def main():

    dst = os.getenv(
                "ICMP_DST",
                "{}".format("localhost")
            ).strip().lstrip()
    packet_count = int(os.getenv(
                "ICMP_COUNT",
                "{}".format(NUM_PACKETS)
            ).strip().lstrip())
    packet_size = int(os.getenv(
                "ICMP_PACKET_SIZE",
                "{}".format(PACKET_SIZE)
            ).strip().lstrip())
    timeout = float(os.getenv(
                "ICMP_TIMEOUT",
                "2.0"
            ).strip().lstrip())
    silent = bool(os.getenv(
                "ICMP_SILENT",
                "0"
            ).strip().lstrip() == "1")

    ping = verbose_ping
    if silent:
        ping = quiet_ping

    ping(dst,
         timeout=timeout * 1000,
         count=packet_count,
         packet_size=packet_size)


if __name__ == '__main__':
    main()
