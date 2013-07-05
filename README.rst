Add new meta tags to you Plone site, for better controlling how your items are **shared on Facebook**. 

.. contents:: **Table of contents**

Introduction
============

Are you commonly sharing contents from your Plone site or a site page to a `Facebook`__ account?

__ http://www.facebook.com/

When you use the nice Facebook sharing interface, you have a simple way to customize additional data for the item
that will be published (mainly: choose a proper image from the remote page).
However when trying to do this automatically (e.g: you are publishing the link in a `Twitter`__ account that also
feed a Facebook page) Facebook is choosing an image for you... and often this is not the image you want.

__ http://twitter.com/

How can you solve this? In general you can provide some additional ``meta`` tag information using
`Open Graph standard`__, customizing many aspect of the way of sharing contents on Facebook.

__ http://developers.facebook.com/docs/opengraph/

Product detail
==============

Installing *collective.fbshare* product and add some additional ``meta`` tags in the *head* section of your site.

Plone site metas
----------------

When sharing the site root, you'll get:

``og:type``
    Always ``website``
``og:url``
    The URL to the site
``og:image``
    See next section
``og:title``
    The name of the site
``og:description``
    The description of the site

When sharing site content's you'll get:

``og:type``
    Always ``article``
``og:url``
    The URL to the content
``og:site_name``
    The name of the Plone site
``og:image``
    See next section
``og:title``
    The title of the content
``og:description``
    The description of the content
``article:published_time``
    The publication date of the content (when present)
``article:expiration_time``
    The expiration date of the content (when present)
``article:author``
    A link to the creator's page. This will be used only when you choose to display
    the *about* info of site user's
``article:tag``
    List of content tags

About images
============

In the site control panel you can access a new configuration panel named "*Open Graph sharing settings*".
From there you can:

* provide a custom image content to be used as ``og:image``
* choose to use the site's logo as ``og:image``
* enable support for content images, this mean that content types with image field will be able to
  provide that image instead of a global ones.
  Also supported `collective.contentleadimage`__
  
  __ http://plone.org/products/content-lead-image/

Dependencies
============

Tested on:

* Plone 3.3
* Plone 4.2
* Plone 4.3

On Plone 3.3 you need to configure properly `plone.app.registry`__ dependencies and upgrade
the default version used of `plone.z3cform`__.

__ http://pypi.python.org/pypi/plone.app.registry
__ http://pypi.python.org/pypi/plone.z3cform

Similar product
===============

There's another Plone package: that will give you Open Graph support: `collective.opengraph`__

__ http://plone.org/products/collective.opengraph

Credits
=======

Developed with the support of `S. Anna Hospital, Ferrara`__;
S. Anna Hospital supports the `PloneGov initiative`__.

.. image:: http://www.ospfe.it/ospfe-logo.jpg 
   :alt: S. Anna Hospital logo

__ http://www.ospfe.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/

