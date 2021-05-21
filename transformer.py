import os
from pprint import pprint

from objectmapper import ObjectMapper
from reader import Reader


class Transformer(object):
    def __init__(self, xml_dir, out_dir, class_file, isEnumerate):
        self.xml_dir = xml_dir
        self.out_dir = out_dir
        self.class_file = class_file
        self.isEnumerate = isEnumerate

    def transform(self):
        object_mapper = ObjectMapper()
        reader = Reader(xml_dir=self.xml_dir)
        xml_files = reader.get_xml_files()
        annotations = object_mapper.bind_files(xml_files, xml_dir=self.xml_dir)

        if self.isEnumerate:
            self.enumerate_and_write_classes(annotations)

        classes = reader.get_classes(self.class_file)

        self.write_to_txt(annotations, classes)

    def write_to_txt(self, annotations, classes):
        for annotation in annotations:
            output_path = os.path.join(self.out_dir, self.darknet_filename_format(annotation.filename))
            if not os.path.exists(os.path.dirname(output_path)):
                os.makedirs(os.path.dirname(output_path))
            with open(output_path, "w+") as f:
                f.write(self.to_darknet_format(annotation, classes))
    
    def enumerate_and_write_classes(self, annotations):
        labels = {}

        for annotation in annotations:
            for obj in annotation.objects:
                if obj.name in labels.keys():
                    labels[obj.name] += 1
                else:
                    labels[obj.name] = 0

        print('Classese : number')
        pprint(labels)

        f=open(self.class_file, 'w+')
        for key in labels.keys():
            f.write(f'{key}\n')
        
        print(f'Write down classes to: {self.class_file}')

    def to_darknet_format(self, annotation, classes):
        result = []
        for obj in annotation.objects:
            if obj.name not in classes:
                print("Please, add '%s' to classes.txt file." % obj.name)
                exit()


            x, y, width, height = self.get_object_params(obj, annotation.size)
            result.append("%d %.6f %.6f %.6f %.6f" % (classes[obj.name], x, y, width, height))
            # result.append("%d %.6f %.6f %.6f %.6f" % (0, x, y, width, height))

        return "\n".join(result)
    

    @staticmethod
    def get_object_params(obj, size):
        image_width = 1.0 * size.width
        image_height = 1.0 * size.height

        box = obj.box
        absolute_x = box.xmin + 0.5 * (box.xmax - box.xmin)
        absolute_y = box.ymin + 0.5 * (box.ymax - box.ymin)

        absolute_width = box.xmax - box.xmin
        absolute_height = box.ymax - box.ymin

        x = absolute_x / image_width
        y = absolute_y / image_height
        width = absolute_width / image_width
        height = absolute_height / image_height

        return x, y, width, height

    @staticmethod
    def darknet_filename_format(filename):
        pre, ext = os.path.splitext(filename)
        return "%s.txt" % pre
