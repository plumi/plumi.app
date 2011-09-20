## Script (Python) "notifyMemberAreaCreated"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Modify new member area
##

from plumi.app.member_area import notifyMemberAreaCreated

notifyMemberAreaCreated(container,context)
