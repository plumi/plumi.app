"""This package adds extensions to portal_catalog.
"""

from zope.interface import providedBy, Interface
from Acquisition import aq_inner
from Products.CMFPlone.CatalogTool import registerIndexableAttribute
from Products.CMFCore.utils import getToolByName
from plumi.content.interfaces import IPlumiVideo
import logging

def hasImageAndCaption(object,portal, **kw):
    logger=logging.getLogger('plumi.app.policy.catalog_extension')
    if not IPlumiVideo.providedBy(object):
        return None
   
    logger.debug('hasImageAndCaption - have %s ' % object )
    img = object.getThumbnailImage()
    #check that the image is set
    if img is not None and img is not '':
	caption = object.getThumbnailImageDescription() or u''
        md = {'image': True, 'caption': caption }
    else:     
	md = {'image': False, 'caption': u''}

    logger.debug(' hasImageAndCaption returning %s  . thumbnail object is %s' % (md, object.getThumbnailImage()))
    return md

def isTranscodedPlumiVideoObj(object, portal, **kw):
    logger=logging.getLogger('plumi.app.policy.catalog_extension')

    if not IPlumiVideo.providedBy(object):
        return None

    logger.debug(' isTranscodedPlumiVideoObj - have %s ' % object )
    # XXX reimplement this.
    # using the PMH Grok web app 

    #statuses = TRANSCODING_STATUSES
    #status = str(object.getIndyTubeStatus())
    #if status in statuses:
    #    video_status = statuses.get(status, (False, u""))
    #    if video_status[0]:
    #            indytube_html = object.getIndyTubeHTML()
    #    else:
    #            indytube_html = ""
    #else:
    video_status = (False, u"")
    indytube_html = ""

    return { 'transcoding_status':video_status[0], 'indytube_html':indytube_html }

def isPublishablePlumiVideoObj(object, portal, **kw):
    logger=logging.getLogger('plumi.app.policy.catalog_extension')

    if not IPlumiVideo.providedBy(object):
        return None

    logger.debug(' isPublishablePlumiVideoObj - have %s ' % object )

    portal_workflow = getToolByName(portal,'portal_workflow')
    portal_membership = getToolByName(portal,'portal_membership')
    portal_contentlicensing = getToolByName(portal,'portal_contentlicensing')

    #wf state
    item_state = portal_workflow.getInfoFor(object, 'review_state', '')
    #name of creator 
    member_name = object.Creator()
    #get the actual user object
    user = portal_membership.getMemberById(member_name)
    portal.plone_log("Item %s by %s is in state %s. user is %s " % (object.absolute_url(), member_name, item_state,user))
    if user is None:
        portal.plone_log("No matching members??")

    if user is not None and item_state == 'published':
        (url,length,type) = object.getFileAttribs()
        cclicense = portal_contentlicensing.getLicenseAndHolderFromObject(object)
        cclicense_text = portal_contentlicensing.DefaultSiteLicense[0]
        cclicense_url  = None
        if cclicense[1][1] != 'None':
                cclicense_text = cclicense[1][1]
        if cclicense[1][2] != 'None':
                cclicense_url  = cclicense[1][2]


        d = { 'published':True,
              'item_title': object.Title(),
              'item_creator_email': user.getProperty('email',''),
              'item_creator_fullname':user.getProperty('fullname',''),
              'subject': object.Subject(),
              'item_rfc822_datetime': DateTime(object.Date()).rfc822(),
              'item_rfc3339_datetime': DateTime(object.Date()).HTML4(),
              'file_url': url,
              'file_length':length,
              'file_type':type,
              'item_url':object.absolute_url(),
              'license_text':cclicense_text,
              'license_url':cclicense_url
            }

    else:
        d = {'published': False }

    return d

#
# Register these indexable attributes
registerIndexableAttribute('hasImageAndCaption', hasImageAndCaption)
registerIndexableAttribute('isTranscodedPlumiVideoObj', isTranscodedPlumiVideoObj)
registerIndexableAttribute('isPublishablePlumiVideoObj', isPublishablePlumiVideoObj)
