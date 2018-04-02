Network Pipeline Scripts
========================

Capture Agents
--------------

Here are the AntiNex Network Pipeline Capture Agents. These scripts allow for capturing traffic on a network device and flattening it into JSON dictionaries before publishing to the aggregation message broker. Please refer to the ``handle_packets`` method for more details.

.. warning:: These tools will capture network traffic. Please be careful where you deploy them.

.. automodule:: network_pipeline.scripts.capture_arp
   :members: capture_arp_packets

.. automodule:: network_pipeline.scripts.capture_icmp
   :members: capture_icmp_packets

.. automodule:: network_pipeline.scripts.capture_tcp
   :members: capture_tcp_packets

.. automodule:: network_pipeline.scripts.capture_udp
   :members: capture_udp_packets

Publishers
----------

These tools are designed to show how to save captured packet dictionaries to CSVs and how to publish them for live predictions using a pre-trained Deep Neural Network.

.. automodule:: network_pipeline.scripts.packets_rabbitmq
   :members: recv_msg,consume_network_packet_messages_from_rabbitmq

.. automodule:: network_pipeline.scripts.packets_redis
   :members: recv_msg,consume_network_packet_messages_from_redis

Test Tools
----------

These will send mock traffic data to the targeted network device.

.. automodule:: network_pipeline.scripts.base_capture
   :members: example_capture

.. automodule:: network_pipeline.scripts.arp_send_msg
   :members: send_arp_msg

.. automodule:: network_pipeline.scripts.tcp_send_large_msg
   :members: send_tcp_large_message

.. automodule:: network_pipeline.scripts.tcp_send_msg
   :members: send_tcp_message

.. automodule:: network_pipeline.scripts.udp_send_msg
   :members: send_udp_message

.. automodule:: network_pipeline.scripts.listen_tcp_port
   :members: listen_on_tcp_port

.. automodule:: network_pipeline.scripts.listen_udp_port
   :members: listen_on_udp_port

.. automodule:: network_pipeline.scripts.builders.prepare_dataset
   :members: find_all_headers,build_csv,find_all_pipeline_csvs,prepare_new_dataset

.. automodule:: network_pipeline.scripts.modelers.keras_dnn
   :members: build_new_deep_neural_network_from_env_variables

.. automodule:: network_pipeline.scripts.tools.arp_send_msg
   :members: Ethernet,Arp
