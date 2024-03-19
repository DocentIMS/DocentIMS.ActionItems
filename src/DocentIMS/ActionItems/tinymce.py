from Acquisition import aq_get
from plone.base.interfaces import IPatternsSettings
from plone.uuid.interfaces import IUUID
from Products.CMFPlone.patterns.settings import PatternSettingsAdapter
from Products.CMFPlone.utils import get_portal
from zope.interface import implementer

import json


@implementer(IPatternsSettings)
class CustomPatternSettingsAdapter(PatternSettingsAdapter):

    def tinymce(self):
        """Use a folder 'bilder' as initial target to upload and select images (and links)."""
        orig_config = super().tinymce()
        images_folder = aq_get(self.context, "images", None)
        if not images_folder or images_folder.portal_type != "Folder":
            return orig_config

        config = json.loads(orig_config["data-pat-tinymce"])
        images_path = "/".join(images_folder.getPhysicalPath())
        images_uuid = IUUID(images_folder)
        images_favorite = {"path": images_path, "title": "Images"}
        portal = get_portal()
        portal_url = portal.absolute_url()
        images_current_path = images_folder.absolute_url()[len(portal_url) :]

        # We need to set all three for upload to work properly.
        config["upload"]["currentPath"] = images_current_path
        config["relatedItems"]["basePath"] = images_path
        config["upload"]["initialFolder"] = images_uuid
        if "favorites" in config["relatedItems"]:
            config["relatedItems"]["favorites"].insert(0, images_favorite)
        return {"data-pat-tinymce": json.dumps(config)}