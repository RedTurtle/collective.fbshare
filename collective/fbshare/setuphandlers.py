# -*- coding: utf-8 -*-

from zope.component import queryUtility
from Products.CMFCore.utils import getToolByName

from plone.registry.interfaces import IRegistry
from Products.CMFPlone.utils import safe_unicode

from collective.fbshare import logger

PROFILE_ID = 'profile-collective.fbshare:default'

def migrateTo1100(context):
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')
    logger.info('Migrated to version 0.2')
