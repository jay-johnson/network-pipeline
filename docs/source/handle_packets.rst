Source Code - Handle Packets from a Network Interface
=====================================================

This is the default handler for processing network packets received from the network interface with ``eth0`` or ``eth1``. In production, this is the starting point for making live predictions with the AntiNex REST API.

Here is the workflow for processing a network packet from a monitored interface:

#.  Get Available Layers in the Packet
#.  Convert the Packet to a JSON dictionary
#.  Publish the Message using Kombu with environment values setting the routing decision for the message in the aggregation message broker: ``FORWARD_EXCHANGE``, ``FORWARD_ROUTING_KEY``, ``FORWARD_QUEUE``.

.. automodule:: network_pipeline.handle_packets
   :members: handle_packets
