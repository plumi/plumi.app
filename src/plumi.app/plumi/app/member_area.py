import logging
from Products.CMFCore.utils import getToolByName

#i18n
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("plumi")

exclude_filter = [ 'syndication_information' ]
def updateCreatorAndOwnership(container, member_id,object):
    plone_utils = getToolByName(container,'plone_utils') 
    ids_to_update = [ o for o in object.objectIds() if o not in exclude_filter ]
    for o in ids_to_update:
        obj = getattr(object, o)
        obj.setCreators([member_id])

        logging.info('updateCreatorAndOwnership : object is %s object type is %s, creators %s ' %  (o,obj.getTypeInfo().getId(),obj.Creators()))
        try:
            plone_utils.changeOwnershipOf (obj, member_id, 1)
        except KeyError:
            #special case, we must be using a user outside of this plone site, 
            #eg an admin user defined in a higher level
            pass
        #call recursively on sub-objects
        updateCreatorAndOwnership(container,member_id,obj)


def notifyMemberAreaCreated(container,context):
    ''' Called when a user logins in for the first time, and enable user folders is enabled'''
    logger=logging.getLogger('plumi.app.member_area')
    logger.info('starting notifyMemberAreaCreated , container is %s , context is %s' % (container,context))

    # this is the plone folder that holds the default member content
    default_member_content = getattr(container, 'default_member_content', None)
    portal_membership = getToolByName(container,'portal_membership') 
    workflow = getToolByName(container,'portal_workflow')

    #XXX this assumption is broken on importing members from CSV file.
    memb = portal_membership.getAuthenticatedMember()
    member_id = memb.getId()
    #hack around above bug. It manifests itself as everyone owned by 'admin' usually.
    if member_id == 'admin':
        #get name from folder context name
            member_id = context.getId()

    logger.info('found member, is %s ' % member_id) 
    # here we do the copying
#    copy_ids = default_member_content.objectIds()
    copy_ids = ['callouts', 'videos', 'news', 'events']
    #exclude
    id_filter = ['.personal']
    copy_ids = [id for id in copy_ids if id not in id_filter]
#    objects = default_member_content.manage_copyObjects(copy_ids)
    objects = 'x%DA%D3%60b%60%60%C8%04b%86h%16%20%A1%01%22J%40%DCbV%20%11%90%93%9F%97Z%2C%06d%A5%A4%A6%25%96%E6%94%C4%E7%A6%E6%26%A5%16%C5%27%E7%E7%95%A4%E6%95%14s%00%A5%92%13sr%F2KK%8A%C1z%83%88%D7%CB%06%94%2A%CBLI%CD%27Y%27Hy%5Ej9Y6%A6%96%81X%00%20%7B%3F%88'

    context.manage_pasteObjects(objects)
    logger.info('copied objects from default member content')
 
    context.manage_fixupOwnershipAfterAdd()

    #publish the members folder, and whatever got copied into it.
    workflow.doActionFor(context,'publish')
    for pubobj in context.objectIds():
        logging.info('publishing %s ' % pubobj)
        obj2 = getattr(context, pubobj)
        workflow.doActionFor(obj2, 'publish')

    #finally, acquire ownership for the new member
    #run the recursive update creator and ownership
    updateCreatorAndOwnership(container,member_id,context)

    #register users to mailchimp, for engagemedia.org
    try:
        logger.info('calling inviteToList, that registers engagemedia.org users to the relevant mailing list')
        from em.skin.mailchimp import inviteToList
        inviteToList(container,context)
    except:
        pass
 
    logger.info('ending notifyMemberAreaCreated')
