Message recipients
==================

.. currentmodule:: gs.group.list.sender.emailaddresses

The class :class:`EmailPerPostAddresses` determines the email
address that the message should be sent to, providing the
addresses through the :attr:`EmailPerPostAddresses.addresses`
property.

.. class:: EmailPerPostAddresses

   The email addresses for the group-members who get one email
   per post.

   :param group: A group object.
   :type group: :class:`gs.group.base.interfaces.IGSGroupMarker`

   .. attribute:: addresses

      The list of addresses

      :returns: The list of email addresses
      :rtype: A list of strings

      The addresses are for each of the group members that have

      * Verified email addresses,
      * Are on *one email per post*, and
      * Have not been blacklisted.

      Each address is guarinteed to appear only once, and they
      are sorted by the **reverse string**, so all the addresses
      from the same domain are next to each other. This makes the
      batching slightly more efficient.
