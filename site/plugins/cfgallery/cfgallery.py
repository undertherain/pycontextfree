# -*- coding: utf-8 -*-

import os
import sys
import shutil
import html
from nikola.plugin_categories import RestExtension
#from nikola.utils import get_logger, STDERR_HANDLER
from nikola.utils import LOGGER, copy_file

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from mako.template import Template

plugin_path = os.path.dirname(os.path.realpath(__file__))
base_path = plugin_path.split("plugins")[0]
#LOGGER = get_logger('scan_posts', STDERR_HANDLER)


def filter_entry(metadata):
    if "description" not in metadata:
        metadata["description"] = ""
    filtered = {}
    for key in ["url", "project_page"]:
        if key in metadata:
            filtered[key] = metadata[key]
        else:
            filtered[key] = ""
    filtered["meta"] = metadata
    return filtered


def get_entries(path):
    for dirName, subdirList, fileList in os.walk(path, topdown=False):
        for fname in fileList:
            if fname.endswith(".py"):
                yield(os.path.join(dirName, fname))


class Plugin(RestExtension):

    name = "fgallery"

    def set_site(self, site):
        self.site = site
        CFGallery.site = self.site
        directives.register_directive('cfgallery', CFGallery)
        # PublicationList.output_folder = self.site.config['OUTPUT_FOLDER']
        return super(Plugin, self).set_site(site)


class CFGallery(Directive):
    has_content = False
    # required_arguments = 1
    optional_arguments = sys.maxsize
    option_spec = {}

    def read_files(self):
        self.rows = []
        cnt = 0
        for fname in get_entries(os.path.join(base_path, "../examples")):
            LOGGER.info("processing " + fname)
            try:
                # data = load_json(fname)
                data = {}
                data["path"] = fname
                data["name"] = os.path.basename(os.path.dirname(fname))
                data["url"] = "https://github.com/undertherain/pycontextfree/blob/master/examples/" + data["name"] + "/" + os.path.basename(fname)
                data["id"] = cnt
                output_folder = os.path.join(base_path, self.site.config['OUTPUT_FOLDER'], "gallery")
                os.makedirs(output_folder, exist_ok=True)
                # data["name"] = html.escape(output_folder)
                print("AAAAAAAAAAAAAAAAAAAAAAAAa")
                name_image = os.path.basename(fname)[:-3] + ".png"
                # copy_file(fname[:-3] + ".png", os.path.join(output_folder, name_image))
                shutil.copy(fname[:-3] + ".png", os.path.join(output_folder, name_image))
                data["image"] = "/gallery/" + name_image
                cnt += 1
                self.rows.append(data)
            except Exception as e:
                LOGGER.warning("error processing " + fname + str(e))

    def render(self):
        self.read_files()
        mytemplate = Template(filename=os.path.join(plugin_path, 'gallery.tmpl'))
        result = mytemplate.render(rows=self.rows)
        return result

    def run(self):
        html = self.render()
        return [nodes.raw('', html, format='html'), ]


def main():  # for developing
    print("hi")


if __name__ == "__main__":
    main()
    mp = SampleProcessor()
    print(mp.render())
