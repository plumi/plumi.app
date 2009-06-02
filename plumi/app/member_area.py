import logging
from Products.CMFCore.utils import getToolByName

exclude_filter = [ 'syndication_information' ]
def updateCreatorAndOwnership(container, member_id,object):
    plone_utils = getToolByName(container,'plone_utils') 
    ids_to_update = [ o for o in object.objectIds() if o not in exclude_filter ]
    for o in ids_to_update:
        logging.info('updateCreatorAndOwnership : object is %s ' % o)
        obj = getattr(object, o)
        logging.info('object type is %s, creators %s ' %  (obj.getTypeInfo().getId(),obj.Creators()))
        obj.setCreators([member_id])
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

    memb = portal_membership.getAuthenticatedMember()
    member_id = memb.getId()
    logger.info('found member, is %s ' % member_id)

    # here we do the copying
    copy_ids = default_member_content.objectIds()
    #exclude
    id_filter = ['.personal']
    copy_ids = [id for id in copy_ids if id not in id_filter]
    objects = default_member_content.manage_copyObjects(copy_ids)
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
 
    logger.info('ending notifyMemberAreaCreated')
