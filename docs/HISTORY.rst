Changelog
=========

1.2.2 (2015-09-21)
------------------

* Using ``subject`` rather than ``Subject`` in ``mailto:`` URIs

1.2.1 (2015-04-07)
------------------

* Switch to using the ``subject``
  :class:`gs.group.list.base.EmailMessage` for the basis of the
  :mailheader:`Subject`

1.2.0 (2015-03-17)
------------------

* Acquiring the relay-address prefix from a configuration file,
  rather than hard-coding it in the :mailheader:`From` header

1.1.0 (2015-02-05)
------------------

* Adding support for the :mailheader:`List-ID` header, as
  described in :rfc:`2919`
* Adding more fall-backs for the short title with the 
  :mailheader:`Subject` header

1.0.2 (2015-02-02)
------------------

* Processing the message even if the list is missing a title

1.0.2 (2015-01-26)
------------------

* Updating the MANIFEST

1.0.1 (2014-11-17)
------------------

* Fixed the queries so they work
* Cope with a missing ``From`` address

1.0.0 (2014-11-07)
------------------

Initial version. Prior to the creation of this product the
:class:`Products.XWFMailingListManager.XWFMailingList` class
generated the list of recipients and modified the email headers.

..  LocalWords:  Changelog
