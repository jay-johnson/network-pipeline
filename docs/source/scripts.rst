Network Pipeline Scripts
========================

Capture Agents
--------------

Here are the AntiNex Network Pipeline Capture Agents. These scripts allow for capturing traffic on a network device and flattening it into JSON dictionaries before publishing to the aggregation message broker. Please refer to the ``handle_packets`` method for more details.

.. warning:: These tools will capture network traffic. Please be careful where you deploy them.

.. automodule:: network_pipeline.scripts.capture-arp
   :members: dev,default_filter,custom_filter,scapy

.. automodule:: network_pipeline.scripts.capture-icmp
   :members: dev,default_filter,custom_filter,scapy

.. automodule:: network_pipeline.scripts.capture-tcp
   :members: dev,default_filter,custom_filter,scapy

.. automodule:: network_pipeline.scripts.capture-udp
   :members: dev,default_filter,custom_filter,scapy

Publishers
----------

These tools are designed to show how to save captured packet dictionaries to CSVs and how to publish them for live predictions using a pre-trained Deep Neural Network.

.. automodule:: network_pipeline.scripts.packets-rabbitmq
   :members: agg,recv_msg,FORWARD_BROKER_URL,FORWARD_SSL_OPTIONS,FORWARD_QUEUE,sub,queue,seconds

.. automodule:: network_pipeline.scripts.packets-redis
   :members: agg,recv_msg,FORWARD_BROKER_URL,FORWARD_SSL_OPTIONS,FORWARD_QUEUE,sub,queue,seconds

Test Tools
----------

These will send mock traffic data to the targetd network device.

.. automodule:: network_pipeline.scripts.arp-send-msg
   :members: def,network_details,dst_ip,dst_msc,answered,unanswered

.. automodule:: network_pipeline.scripts.icmp-send-msg
   :members: main,checksum,do_one,send_one_ping,receive_one_ping,dump_stats,signal_handler,verbose_ping,quiet_ping

.. automodule:: network_pipeline.scripts.tcp-send-large-msg
   :members: client,msg

.. automodule:: network_pipeline.scripts.tcp-send-msg
   :members: client,msg

.. automodule:: network_pipeline.scripts.udp-send-msg
   :members: client,msg

.. automodule:: network_pipeline.scripts.listen-tcp-port
   :members: client,s

.. automodule:: network_pipeline.scripts.listen-udp-port
   :members: client,s
