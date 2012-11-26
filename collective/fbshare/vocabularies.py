# -*- coding: utf-8 -*-

from zope.interface import implements

try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    # Plone 4.1
    from zope.schema.interfaces import IVocabularyFactory

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from Products.CMFCore.utils import getToolByName

from collective.fbshare import messageFactory as _

class ImageChoiceVocabulary(object):
    """Vocabulary factory choosing og:image policy.
    """
    implements( IVocabularyFactory )

    def __call__(self, context):
        
        terms = [SimpleTerm(u'custom_image', title=_(u'Custom image (select one below)')),
                 SimpleTerm(u'site_logo', title=_(u'Use site logo')),
                 ]
        return SimpleVocabulary(terms)


class ImageSizeVocabulary(object):
    """Vocabulary factory for chhosing a content image format.
    """
    implements( IVocabularyFactory )

    def __call__(self, context):
        
        terms = [SimpleTerm(u'', title=_(u"Dont' resize images")),]
        
        imaging_properties = getattr (getToolByName(context, 'portal_properties'), 'imaging_properties', None)
        if imaging_properties:
            allowed_sizes = imaging_properties.allowed_sizes
            terms.extend([SimpleTerm(x.split(' ')[0], title=x) for x in allowed_sizes])
        
        return SimpleVocabulary(terms)


imageChoiceVocabularyFactory = ImageChoiceVocabulary()
imageSizeVocabularyFactory = ImageSizeVocabulary()