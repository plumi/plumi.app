"""This package adds extensions to portal_catalog.
"""
from Acquisition import aq_inner
from Products.CMFPlone.CatalogTool import registerIndexableAttribute
from Products.ATContentTypes.interface.image import IImageContent
from zope.interface import providedBy

def hasImageAndCaption(object, portal, **kw):
    if not IImageContent.providedBy(object):
        return None
    
    if object.getImage():
        caption = getattr(aq_inner(object), "getImageCaption", None)
        return {'image': True,
                'caption': caption and caption() or u''}
        
    return {'image': False, 'caption': u''}

print "registering new index for plumi.app"
registerIndexableAttribute('hasImageAndCaption', hasImageAndCaption)

