import os
import xml.etree.ElementTree as ET

def convert_coordinates(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    # Calculate box center coordinates (x, y) and width/height (w, h)
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    # Normalize coordinates
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(xml_file, classes):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    objects = []
    for obj in root.findall('object'):
        obj_class = obj.find('name').text
        if obj_class not in classes:
            continue
        obj_id = classes.index(obj_class)
        bbox = obj.find('bndbox')
        xmin = float(bbox.find('xmin').text)
        xmax = float(bbox.find('xmax').text)
        ymin = float(bbox.find('ymin').text)
        ymax = float(bbox.find('ymax').text)
        bbox = (xmin, xmax, ymin, ymax)
        converted_bbox = convert_coordinates((w, h), bbox)
        objects.append((obj_id,) + converted_bbox)
    return objects

def main():
    # Define classes
    classes = ['With Helmet', 'Without Helmet']  # Update with your class labels
    # Path to directory containing XML annotations
    xml_dir = r'C:\Users\abhis\Downloads\Bike Helmet dataset\annotations'
    # Output directory for YOLO format annotations
    output_dir = r'C:\Users\abhis\OneDrive\Documents\Helmet_Detection_yolo_annotation'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for xml_file in os.listdir(xml_dir):
        if not xml_file.endswith('.xml'):
            continue
        image_id = os.path.splitext(xml_file)[0]
        yolo_file = os.path.join(output_dir, image_id + '.txt')
        objects = convert_annotation(os.path.join(xml_dir, xml_file), classes)
        with open(yolo_file, 'w') as f:
            for obj in objects:
                obj_line = ' '.join(str(x) for x in obj)
                f.write(obj_line + '\n')

if __name__ == '__main__':
    main()
