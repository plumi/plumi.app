"""This package adds extensions to portal_catalog.
"""
from Acquisition import aq_inner
from Products.ATContentTypes.interface.image import IImageContent
from zope.interface import providedBy, Interface
from plone.indexer.decorator import indexer

from plumi.content.interfaces import IPlumiVideo

@indexer(Interface)
def hasImageAndCaption(object):
    if not IImageContent.providedBy(object):
        return None
    
    if object.getImage():
        caption = getattr(aq_inner(object), "getImageCaption", None)
        return {'image': True,
                'caption': caption and caption() or u''}
        
    return {'image': False, 'caption': u''}

@indexer(Interface)
def isTranscodedPlumiVideoObj(object, portal, **kw):
    if not IPlumiVideo.providedBy(object):
        return None
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

@indexer(Interface)
def isPublishablePlumiVideoObj(object, portal, **kw):
    if not IPlumiVideo.providedBy(object):
        return None

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

    portal.plone_log("Returning metadata %s " % d)
    return d

