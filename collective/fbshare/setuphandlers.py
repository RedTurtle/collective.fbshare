# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from collective.fbshare import logger


PROFILE_ID = 'profile-collective.fbshare:default'

def migrateTo1100(context):
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')
    logger.info('Migrated to version 0.2')
