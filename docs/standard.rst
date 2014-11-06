Standard header adaptors
========================

There are fourteen standard adaptors. Two `delete headers`_,
there are nine adaptors that `add headers`_, and three complex
adaptors that `modify headers`_.

Delete headers
--------------

Both the :mailheader:`Disposition-Notification-To` and
:mailheader:`Return-Receipt-To` headers are deleted. The
:class:`gs.group.list.sender.headers.delete.DeleteHeader` defines
what little code is needed for these two adaptors (which share
the implementation).

.. autoclass:: gs.group.list.sender.headers.delete.DeleteHeader
   :members:

Add headers
-----------

The nine adaptors that add headers all define simple information
— generally about the group, but also about GroupServer.

.. automodule:: gs.group.list.sender.headers.simpleadd
   :members: Precedence, XMailer, Sender, ListHelp, ListUnsubscribe, 
             ListSubscribe, ListPost, ListOwner, ListArchive

Modify headers
--------------

The three headers that modify the pre-existing content are very
complex relative to the eleven other headers.


:mailheader:`From`
~~~~~~~~~~~~~~~~~~

.. autoclass:: gs.group.list.sender.headers.frm.FromHeader
   :members: get_user_address, get_anon_address, set_formally_from,
             modify_header

:mailheader:`Subject`
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: gs.group.list.sender.headers.subject.SubjectHeader
   :members: modify_header

:mailheader:`Reply-To`
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: gs.group.list.sender.headers.replyto.ReplyToHeader
   :members: modify_header

