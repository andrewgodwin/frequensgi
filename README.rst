frequensgi
==========

APRS-IS ASGI protocol server. Allows receiving messages from, and sending
messages to, the APRS network.



ASGI Protocol Specification
---------------------------

Connection Scope
''''''''''''''''

Incoming frames are scoped by their callsign.

The scope and application instance will be made when a frame with that callsign
is received after process start, and will be lost either when
the callsign has been inactive for some time and it is garbage-collected or when
the current process ends.

If you want to manage long-lasting, per-callsign state, it's recommended you use
a database or some kind of session store.

The scope contains:

* ``type``: ``aprs``

* ``callsign``: APRS callsign, including SSID suffix if nonzero (e.g. ``K3AEA-1``).


Frame (Incoming)
''''''''''''''''

An incoming frame. Might be targeted at the callsign of the APRS server,
or if the server is configured for full-feed or location-based, to any callsign.

Frequensgi will try to decode the frame as much as it can and give you high-level
values, but the raw frame will always be included in case there is custom packing
logic involved.

Keys:

* ``type``: ``asgi.frame``

* ``frame``: Byte string of the entire received frame.

* ``from


Frame (Outgoing)
''''''''''''''''

An outgoing frame. Will be sent from the server's configured callsign out into
the APRS-IS system.

Keys:

* ``type``: ``asgi.send_frame``

* ``frame``: Byte string of the frame to send. If provided, no other
  keys are used.

* ``from
