# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.plugins.facebook.browser import PluginView as BasePluginView


class PluginView(BasePluginView):
    """
    Simply need to register a poor-man versione of the original meta set
    """    
    metadata = ViewPageTemplateFile("metadata.pt")
