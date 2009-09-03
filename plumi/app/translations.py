from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.i18n import ITranslationDomain

def createTranslations(portal,canon,domain='plumi'):
    """Creates translations of 'canon' into all available languages in 'domain'"""
    parent = canon.getParentNode()
    wftool = getToolByName(portal,'portal_workflow')
    transDomain = getUtility(ITranslationDomain, domain)
    availLanguages = transDomain.getCatalogsInfo()
    langs = []
    for lang in availLanguages.keys():
        if str(lang) != 'test':
            langs.append(str(lang))
    for lang in langs:
        transId = '%s-%s' % (canon.id, lang)
        transTitle = transDomain.translate(canon.title,
                                           target_language=lang)
        transDesc = transDomain.translate(canon.description,
                                          target_language=lang)
        if not hasattr(parent, transId):
            if parent != portal and parent.hasTranslation(lang):
                #if parent folder has a translation, put the clone in that
                translation = parent.getTranslation(lang).manage_clone(canon,
                                                    transId)
            else:
                translation = parent.manage_clone(canon, transId)
            translation.setTitle(transTitle)
            translation.setDescription(transDesc)
            translation.setLanguage(lang)
            translation.addTranslationReference(canon)
            wftool.doActionFor(translation,action='publish')

def createTranslationsRecursive(portal,canon,domain='plumi'):
    """Recursively creates translations into all available languages."""
    createTranslations(portal,canon,domain)
    if canon.isPrincipiaFolderish:
        for child in canon.getChildNodes():
            createTranslationsRecursive(portal,child,domain)

def deleteTranslations(canon):
    """Deletes all the translations of 'canon'"""
    for translation in canon.getBRefs():
        canon.getParentNode().manage_delObjects(translation.id)

#probably don't need a deleteTranslationsR, since once we delete the parent(s),
#the children should be unreferenced, and get garbage-collected later on.
