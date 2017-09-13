import os


class Reader(object):
    def __init__(self, xml_dir):
        self.xml_dir = xml_dir

    def get_xml_files(self):
        xml_filenames = []
        for xml_filename in os.listdir(self.xml_dir):
            if xml_filename.endswith(".xml"):
                xml_filenames.append(os.path.join(self.xml_dir, xml_filename))
        return xml_filenames

    @staticmethod
    def get_classes(filename="classes.txt"):
        with open(os.path.join(os.path.dirname(os.path.realpath('__file__')), filename), "r") as f:
            lines = f.readlines()
            return {value: key for (key, value) in enumerate(list(map(lambda x: x.strip(), lines)))}
