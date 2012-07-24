# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope import schema

from collective.fbshare import messageFactory as _


class IFbShareBrowserLayer(Interface):
    """Marker interface for collective.fbshare products layer"""


class IFbShareSettings(Interface):
    """
    Settings used in the control panel for Facebook (opengraph) share
    """
    
    default_image = schema. Bytes(
            title=_(u"Default image for Open Graph sharing"),
            description=_('help_default_image',
                          default=u"Images for Facebook must be at least 50px by 50px (though minimum 200px by 200px is preferred) "
                                  u"and have a maximum aspect ratio of 3:1. Supported format are PNG, JPEG and GIF formats."),
            default=None,
            required=False,
    )

