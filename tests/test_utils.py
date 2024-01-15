import unittest
from xml.etree import ElementTree

from utils import _aggregate_svg_elements, _set_viewbox, combine_svg, generate_sheet, perform_pack


def _generate_shapes():
    return """
    <svg>
      <rect width="100" height="50" />
      <rect width="50" height="100" />
      <ellipse rx="20" ry="20" />
    </svg>
    """


def _generate_shapes_with_viewbox():
    return """
    <svg viewBox="0 0 1 1">
      <rect width="100" height="50" />
      <rect width="50" height="100" />
      <ellipse rx="20" ry="20" />
    </svg>
    """


class TestCombineSVG(unittest.TestCase):
    def test_aggregate_svg(self):
        """ Test the `_aggregate_svg()` function """
        shape1 = _generate_shapes()
        shape2 = _generate_shapes()

        combined = _aggregate_svg_elements([shape1, shape2])

        self.assertEqual(6, len(combined))

    def test_set_viewbox(self):
        """ Test the `_set_viewbox()` function """
        _shape_str = _generate_shapes()
        shape = ElementTree.fromstring(_shape_str)

        with_viewbox = _set_viewbox(shape)

        self.assertEqual('0 0 100 100', with_viewbox.attrib['viewBox'])

    def test_combine_svg(self):
        """ Test the top level `combine_svg()` function. """

        shape1 = _generate_shapes()
        shape2 = _generate_shapes()

        combined_as_str = combine_svg([shape1, shape2])
        combined = ElementTree.fromstring(combined_as_str)

        # check that there are 6 internal shapes
        self.assertEqual(6, len(combined))

        # check that viewBox is set
        self.assertEqual('0 0 100 100', combined.attrib['viewBox'])


class TestGenerateSheet(unittest.TestCase):
    """ Test the `generate_sheet()` function. """

    def test_empty(self):
        """ Test that there are no elements inside of the sheet """
        sheet_as_str = generate_sheet(1, 1)
        sheet = ElementTree.fromstring(sheet_as_str)

        self.assertEqual(0, len(sheet))

    def test_default_dpi(self):
        """ Test the default API """
        height = 1
        expected_height = 96

        width = 2
        expected_width = 96 * 2

        sheet_as_str = generate_sheet(width=width, height=height)
        sheet = ElementTree.fromstring(sheet_as_str)

        expected_viewbox = f"0 0 {expected_width} {expected_height}"
        self.assertEqual(expected_viewbox, sheet.attrib['viewBox'])

    def test_with_dpi(self):
        dpi = 1000

        width = 2
        expected_width = dpi * width

        height = 1
        expected_height = dpi * height

        sheet_as_str = generate_sheet(width=width, height=height, dpi=dpi)
        sheet = ElementTree.fromstring(sheet_as_str)

        expected_viewbox = f"0 0 {expected_width} {expected_height}"
        self.assertEqual(expected_viewbox, sheet.attrib['viewBox'])


class TestPerformPacking(unittest.TestCase):
    """ Test the functionality of the `packaide.pack()` wrapper """

    def test_correct_number_of_resulting_shapes(self):
        """ Test that the correct number of resulting shapes """
        sheet = generate_sheet(200, 200, 1)
        shapes = _generate_shapes_with_viewbox()

        # manually get the number of shapes
        _shapes_as_xml = ElementTree.fromstring(shapes)
        number_of_shapes = len(_shapes_as_xml)

        # perform pack and count the number of internal shapes
        outputs = perform_pack(shapes, sheet)
        output_as_str = outputs[0]
        output = ElementTree.fromstring(output_as_str)

        self.assertEqual(number_of_shapes, len(output))

    def test_correct_output_size(self):
        """ Test that the output sheet size matches the original sheet """
        expected_width = 200
        expected_height = 100
        sheet = generate_sheet(expected_width, expected_height, dpi=1)

        shapes = _generate_shapes_with_viewbox()

        outputs = perform_pack(shapes, sheet)

        output_as_str = outputs[0]
        output = ElementTree.fromstring(output_as_str)

        expected_viewbox = f"0 0 {expected_width} {expected_height}"
        self.assertEqual(expected_viewbox, output.attrib['viewBox'])

    def test_sheet_too_small(self):
        """ Test that no shapes are placed when the sheet is too small """
        sheet = generate_sheet(1, 1, 1)
        shapes = _generate_shapes_with_viewbox()

        outputs = perform_pack(shapes, sheet)
        output_as_str = outputs[0]
        output = ElementTree.fromstring(output_as_str)

        self.assertEqual(0, len(output))

    @unittest.expectedFailure
    def test_correct_multiple_sheets(self):
        """ Test that multiple sheets are returned when shapes do not fit onto a single sheet """
        # shapes cannot fit onto a 100 x 100 sheet
        shapes = _generate_shapes_with_viewbox()

        sheet = generate_sheet(100, 100, 1)

        outputs = perform_pack(shapes, sheet)

        # expect 2 output sheets
        self.assertEqual(2, len(outputs))

        # manually get the number of shapes
        _shapes_as_xml = ElementTree.fromstring(shapes)
        number_of_shapes = len(_shapes_as_xml)

        # get the number of shapes on each sheet
        shape_counter = 0
        for output_sheet_as_str in outputs:
            output = ElementTree.fromstring(output_sheet_as_str)
            shape_counter += len(output)

        self.assertEqual(number_of_shapes, shape_counter)





if __name__ == '__main__':
    unittest.main()
