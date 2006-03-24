"""
This tool requires a translation service which supports
the utranslate method and the default parameter.
By time of writing this code, that is only valid for PTS.
"""

from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem
from Products.CMFCore.utils import UniqueObject
from Products.CMFPlone import ToolNames
from AccessControl import ClassSecurityInfo
from Products.CMFPlone.PloneBaseTool import PloneBaseTool
from Products.CMFPlone.utils import classImplements
from Products.CMFCore.utils import getToolByName
from i18nl10n import utranslate, ulocalized_time, \
                     monthname_msgid, monthname_msgid_abbr, \
                     weekdayname_msgid, weekdayname_msgid_abbr, \
                     weekdayname_msgid_short, \
                     monthname_english, weekdayname_english

class TranslationServiceTool(PloneBaseTool, UniqueObject, SimpleItem):
    """ Utility methods to access the translation machinery """

    id = 'translation_service'
    meta_type = ToolNames.TranslationServiceTool
    toolicon = 'skins/plone_images/site_icon.gif'
    security = ClassSecurityInfo()

    __implements__ = (PloneBaseTool.__implements__,
                      SimpleItem.__implements__, )

    security.declarePublic('utranslate')
    def utranslate(self, *args, **kw):
        # Translate method to access the translation service
        # from resticted code like skins.
        return utranslate(*args, **kw)

    security.declarePublic('encode')
    def encode(self, m, input_encoding=None, output_encoding=None, errors='strict'):
        # encode a give unicode type or string type to string type in encoding output_encoding

        # check if input is not type unicode
        if not isinstance(m, unicode):
            if input_encoding is None: input_encoding = 'utf-8'
            m = unicode(str(m), input_encoding, errors)

        if output_encoding is None:
            # get output encoding from portal
            plone_tool = getToolByName(self, 'plone_utils')
            output_encoding = plone_tool.getSiteEncoding()

        # return as type string
        return m.encode(output_encoding, errors)

    security.declarePublic('asunicodetype')
    def asunicodetype(self, m, input_encoding=None, errors='strict'):
        # create type unicode from type string

        if isinstance(m, unicode): return m

        if input_encoding is None:
            # get input encoding from portal
            plone_tool = getToolByName(self, 'plone_utils')
            input_encoding = plone_tool.getSiteEncoding()

        # return as type unicode
        return unicode(str(m), input_encoding, errors)

    security.declarePublic('ulocalized_time')
    def ulocalized_time(self, time, long_format = None, context = None, domain='plone'):
        # get some context if none is passed
        if context is None: context = self
        return ulocalized_time(time, long_format, context, domain)

    security.declarePublic('day_msgid')
    def day_msgid(self, number, format=''):
        """ Returns the msgid which can be passed to the translation service for
        l10n of weekday names. Format is either '', 'a' or 's'.

        >>> ttool = self.portal.translation_service

        >>> ttool.day_msgid(0)
        'weekday_sun'

        >>> ttool.day_msgid(6)
        'weekday_sat'

        >>> ttool.day_msgid(0, format='a')
        'weekday_sun_abbr'

        >>> ttool.day_msgid(3, format='s')
        'weekday_wed_short'
        """
        # 
        if format == 's':
            # short format
            method = weekdayname_msgid_short
        elif format == 'a':
            # abbreviation
            method = weekdayname_msgid_abbr
        else:
            # long format
            method = weekdayname_msgid
        return method(number)

    security.declarePublic('month_msgid')
    def month_msgid(self, number, format=''):
        """ Returns the msgid which can be passed to the translation service for
        l10n of month names. Format is either '' or 'a' (long or abbreviation).

        >>> ttool = self.portal.translation_service

        >>> ttool.month_msgid(1)
        'month_jan'

        >>> ttool.month_msgid(12)
        'month_dec'

        >>> ttool.month_msgid(6, format='a')
        'month_jun_abbr'
        """
        return 'a' == format and monthname_msgid_abbr(number) or monthname_msgid(number)

    security.declarePublic('monthname_english')
    def month_english(self, number, format=''):
        """ Returns the english name of month by number. Format is either '' or
        'a' (long or abbreviation).

        >>> ttool = self.portal.translation_service

        >>> ttool.month_english(1)
        'January'

        >>> ttool.month_english(1, 'a')
        'Jan'
        """
        return monthname_english(number, format=format)

    security.declarePublic('weekdayname_english')
    def weekday_english(self, number, format=''):
        """ Returns the english name of a week by number. Format is either '',
        'a' or 'p'.

        >>> ttool = self.portal.translation_service

        >>> ttool.weekday_english(0)
        'Sunday'

        >>> ttool.weekday_english(6)
        'Saturday'

        >>> ttool.weekday_english(0, format='a')
        'Sun'

        >>> ttool.weekday_english(3, format='p')
        'Wed.'
        """
        return weekdayname_english(number, format=format)

classImplements(TranslationServiceTool,
                TranslationServiceTool.__implements__)
InitializeClass(TranslationServiceTool)
