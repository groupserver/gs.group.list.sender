Changelog
=========

1.1.0 (2014-02-05)
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
