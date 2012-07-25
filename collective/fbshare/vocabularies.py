# -*- coding: utf-8 -*-

from zope.interface import implements

try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    # Plone 4.1
    from zope.schema.interfaces import IVocabularyFactory

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from collective.fbshare import messageFactory as _

class ImageChoiceVocabulary(object):
    """Vocabulary factory for mode to use of a cloud.
    """
    implements( IVocabularyFactory )

    def __call__(self, context):
        
        terms = [SimpleTerm(u'custom_image',_(u'Custom image (select one below)')),
                 SimpleTerm(u'site_logo',_(u'Use site logo')),
                 ]
        return SimpleVocabulary(terms)

imageChoiceVocabularyFactory = ImageChoiceVocabulary()