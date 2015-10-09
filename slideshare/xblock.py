from __future__ import absolute_import
"""

XBlock for SlideShare

Allows for the easy selection and embedding of an SlideShare within an XBlock.
Makes use of the SlideShare oEmbed entry points to look up the embed code and then
inserts it within the XBlock.

"""

import cgi
import pkg_resources
import requests

from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment

from xblockutils.publish_event import PublishEventMixin
from xblockutils.studio_editable import StudioEditableXBlockMixin


class SlideshareXBlock(XBlock, StudioEditableXBlockMixin, PublishEventMixin):
    """
    An XBlock providing SlideShare embedding capabilities
    """

    # Stored values for the XBlock
    href = String(
        display_name="SlideShare Embed URL",
        help="URL of the SlideShare you want to embed",
        scope=Scope.content,
        default='http://slideshare.net/slideshow/embed_code/key/mcQl0fTfEcQ7WI')

    display_name = String(
        display_name="Display Name",
        help="This name appears in the horizontal navigation at the top of the page.",
        scope=Scope.settings,
        default="SlideShare")

    editable_fields = ('href', 'display_name')

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        """
        Create a fragment used to display the XBlock to a student
        `context` is a dictionary used to configure the display (unused).

        Returns a `Fragment` object specifying the HTML, CSS and JavaScript to display
        """
        href = self.href or ''
        display_name = self.display_name or ''

        # Make the oEmbed call to get the embed code
        try:
            embed_code, width, height = self.get_embed_code(href)
            html_str = self.resource_string("static/html/slideshare.html")
        except Exception as ex:
            html_str = self.resource_string("static/html/embed_error.html")
            frag = Fragment(html_str.format(self=self, exception=cgi.escape(str(ex))))

            # Construct the JavaScript
            frag.add_javascript(self.resource_string("/static/js/src/slideshare_error.js"))
            frag.initialize_js('SlideshareXBlock')

            return frag

        # Construct the HTML
        frag = Fragment(html_str.format(self=self, embed_code=embed_code, display_name=cgi.escape(display_name)))

        # Construct the JavaScript
        frag.add_javascript(self.resource_string("/static/js/src/slideshare_view.js"))
        frag.initialize_js('SlideshareXBlock')

        return frag

    def get_embed_code(self, url):
        """
        Makes an oEmbed call out to Slideshare to retrieve the embed code and width and height of the mix
        for the given url.
        """

        parameters = {'url': url}

        oEmbedRequest = requests.get("http://www.slideshare.net/api/oembed/2/", params=parameters)
        oEmbedRequest.raise_for_status()
        responseJson = oEmbedRequest.json()

        return responseJson['html'], responseJson['width'], responseJson['height']

    @staticmethod
    def workbench_scenarios():
        """ Returns a single element which is the SlideShare xblock """
        return [
            ("SlideShare",
             """
             <slideshare href="http://slideshare.net/slideshow/embed_code/key/mcQl0fTfEcQ7WI" />
             """),
        ]
