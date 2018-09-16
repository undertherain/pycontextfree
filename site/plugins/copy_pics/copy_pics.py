"""Copy pics"""


import os
from nikola.plugin_categories import Task
from nikola import utils
from nikola.utils import LOGGER

plugin_path = os.path.dirname(os.path.realpath(__file__))
base_path = plugin_path.split("plugins")[0]


def get_entries(path):
    for dirName, subdirList, fileList in os.walk(path, topdown=False):
        for fname in fileList:
            if fname.endswith(".png"):
                yield(os.path.join(dirName, fname))


class CopyPics(Task):
    """Render code listings."""

    name = "copy_pics"

    def register_output_name(self, input_folder, rel_name, rel_output_name):
        """Register proper and improper file mappings."""
        self.improper_input_file_mapping[rel_name].add(rel_output_name)
        self.proper_input_file_mapping[os.path.join(input_folder, rel_name)] = rel_output_name
        self.proper_input_file_mapping[rel_output_name] = rel_output_name

    def set_site(self, site):
        """Set Nikola site."""

    def gen_tasks(self):
        for in_name in get_entries(os.path.join(base_path, "../examples")):
            name_image = os.path.basename(in_name)
            out_name = "output/gallery/" + name_image

        # in_name = "/home/blackbird/Projects_heavy/pycontextfree/examples/paper/paper.png"
        # out_name = "output/gallery/paper.png"
        # out_name = "gallery/paper.png"
            LOGGER.info(f"emiting copyi task {in_name} to {out_name}")
            yield utils.apply_filters({
                'basename': self.name,
                'name': out_name,
                'file_dep': [in_name],
                'targets': [out_name],
                'actions': [(utils.copy_file, [in_name, out_name])],
                'clean': True,
                }, {})
