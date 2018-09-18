import os
from nikola.plugin_categories import ShortcodePlugin
from mako.template import Template
from nikola.utils import LOGGER

plugin_path = os.path.dirname(os.path.realpath(__file__))
base_path = plugin_path.split("plugins")[0]


def get_entries(path):
    for dirName, _, fileList in os.walk(path, topdown=False):
        for fname in fileList:
            if fname.endswith(".py"):
                yield(os.path.join(dirName, fname))


class Plugin(ShortcodePlugin):

    name = "my_gallery"

    def read_files(self):
        self.rows = []
        cnt = 0
        for fname in get_entries(os.path.join(base_path, "../examples")):
            LOGGER.info("processing " + fname)
            try:
                # data = load_json(fname)
                data = {}
                data["path"] = fname
                data["path_image"] = fname[:-3] + ".png"
                data["name"] = os.path.basename(os.path.dirname(fname))
                data["url"] = "https://github.com/undertherain/pycontextfree/blob/master/examples/" + data["name"] + "/" + os.path.basename(fname)
                data["id"] = cnt
                name_image = os.path.basename(fname)[:-3] + ".png"

                data["image"] = "/gallery/" + name_image
                cnt += 1
                self.rows.append(data)
            except Exception as e:
                LOGGER.warning("error processing " + fname + str(e))

    def handler(self, filename=None, site=None, data=None, lang=None, post=None):
        # self.output_folder = os.path.join(base_path, site.config['OUTPUT_FOLDER'], "gallery")
        # os.makedirs(self.output_folder, exist_ok=True)
        self.read_files()
        mytemplate = Template(filename=os.path.join(plugin_path, 'gallery.tmpl'))
        result = mytemplate.render(rows=self.rows)
        # result = "hi!"
        return result, []
