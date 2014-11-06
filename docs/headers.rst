Headers
=======

The headers of an email message are modified before being
sent. The headers are either added, deleted, or changed. The
:func:`gs.group.list.sender.modify_headers` function performs the
modification.

.. autofunction:: gs.group.list.sender.modify_headers

Each header is modified by a header adaptor.

Header adaptor
==============

Each header that needs to be modified is represented by a
named-adaptor. The adaptor is a class that adapts a ``group`` and
a ``request`` and provides an
:class:`gs.group.list.sender.interfaces.IEmailHeaderModifier`
interface.

.. py:class:: gs.group.list.sender.interfaces.IEmailHeaderModifier(group, request)

   An adaptor to modify an email header.

   :param group: A group object.
   :type group: :class:`gs.group.base.interfaces.IGSGroupMarker`
   :param request: An HTTP request.
   :type request: :class:`zope.publisher.interfaces.browser.IDefaultBrowserLayer`

   .. py:method:: modify_header(email)

      Modify the header in the email message

      :param email: The email message
      :type email: :class:`email.message.Message`
      :returns: The new value for the header
      :rtype: ``unicode``, ``bytes``, or ``None``

The :meth:`modify_header` method can return either a ``unicode``,
``bytes`` [#bytes]_, or ``None``. The
:func:`gs.group.list.sender.modify_headers` function will change
the header in one of three ways depending on the return type.

``None``:
    The header is deleted.

``str``:
    The header is set to the string.

``unicode``:
    The output is encoded (using :class:`email.header.Header`)
    and the header is set to the string.

Normally a header-adaptor is declared in the ZCML. For example,
the ``Precedence`` header:

.. code-block:: xml

  <adapter
    name="Precedence"
    for="gs.group.base.interfaces.IGSGroupMarker
         zope.publisher.interfaces.browser.IDefaultBrowserLayer"
    provides=".interfaces.IEmailHeaderModifier"
    factory=".headers.simpleadd.Precedence" />

:Note: The adaptors are **named**, with the name being the name
       of the header.

The :mod:`gs.group.list.sender` provides fourteen adaptors (see
:doc:`standard`).

.. [#bytes] In Python 2 ``bytes`` is a synonym for ``str``.
