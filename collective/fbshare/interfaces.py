# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope import schema

from collective.fbshare import messageFactory as _
from collective.fbshare import logger

# We customize some of the sc.social.like behavior in this way
try:
    from sc.social.like.interfaces import ISocialLikeLayer as BaseLayerInterface
    logger.info('sc.social.like found. collective.fbshare will override Facebook OpenGraph meta')
except ImportError:
    from zope.interface import Interface as BaseLayerInterface


class IFbShareBrowserLayer(BaseLayerInterface):
    """Marker interface for collective.fbshare products layer"""


class IFbShareSettings(Interface):
    """
    Settings used in the control panel for Facebook (opengraph) share
    """
    
    image_to_share = schema.Choice(
        title=_(u"Default site image to share"),
        description=_('help_image_to_share',
                      default=u"You can choose to provide a custom image or use the site logo.\n"
                              u"If you choose a custom image without providing it, it will not provide any og:image meta content."),
        required=True,
        default=u'custom_image',
        vocabulary='collective.fbshare.imageChoiceVocabulary',
    )
    
    default_image = schema.Bytes(
            title=_(u"Custom image for Open Graph sharing"),
            description=_('help_default_image',
                          default=u"Images for Facebook must be at least 50px by 50px (though minimum 200px by 200px is preferred) "
                                  u"and have a maximum aspect ratio of 3:1. Supported format are PNG, JPEG and GIF formats."),
            default=None,
            required=False,
    )

    content_use_own_image = schema.Bool(
            title=_(u"Contents use own image"),
            description=_('help_content_use_own_image',
                          default=u"If checked, content types that behave an image field will provide the image in the og:image attribute.\n"
                                  u"The product contentleadimage is also supported."),
            default=True,
            required=False,
    )

    content_image_size = schema.Choice(
        title=_(u"Content image size to be used"),
        description=_('help_content_image_size',
                      default=u"Resized version of contents images to be used."),
        required=True,
        default=u'mini',
        vocabulary='collective.fbshare.imageSizeVocabulary',
    )
