# -*- coding: utf-8 -*-

import os

from scrapy.pipelines.images import ImagesPipeline


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class FolderStructureImagePipeline(ImagesPipeline):
    """Store Images using a folder tree structure. DEPTH attribute can be used to specify the depth of the tree."""

    DEPTH = 2

    def tree_path(self, path: str) -> str:
        """Generate a folder tree based on given path. I.e: path/to/image.jpg -> path/to/i/m/a/image.jpg

        :param path: original image filepath.
        :return: image filepath with extra folder tree.
        """
        filename = os.path.basename(path)
        dirname = os.path.dirname(path)
        return os.path.join(dirname, *[_ for _ in filename[: self.DEPTH]], filename)

    def file_path(self, request, response=None, info=None):
        return self.tree_path(super().file_path(request, response, info))

    def thumb_path(self, request, thumb_id, response=None, info=None):
        return self.tree_path(
            super().thumb_path(request, thumb_id, response=response, info=info)
        )
