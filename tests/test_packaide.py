# All of these tests are to explore and verify the functionality of the `packaide` module.
# There are two specific questions that needed to be answered:
#  1. What is the effect of the viewBox on the output SVG?
#  2. What effect does grouping of SVG elements have on the output SVG?
#
# These questions determine the functionality of the `combine_svg` function. The `combine_svg` function is the core
# functionality which allows multiple SVG files to be combined into a single SVG file.
#
# All of these functions have been visually verified. All results returned from `packaide.pack()` have been viewed
# to ensure that elements are both properly placed and maintain their original size, form, and features.
from typing import Tuple, List

import packaide
import unittest
from xml.etree import ElementTree


# Here is defined a sheet used for testing.

SHEET_HEIGHT = 2500
SHEET_WIDTH = 5000

SHEET = ("""<svg viewBox="0 0 {width} {height}"></svg>"""
         .format(width=SHEET_WIDTH, height=SHEET_HEIGHT))


def do_pack(shapes: str) -> Tuple[List[Tuple[int, str]], int, int]:
    """ This is a helper function to run the `packaide.pack` function. """
    return packaide.pack([SHEET], shapes,
                         tolerance=0.1,
                         offset=0.1,
                         partial_solution=True,
                         rotations=4,
                         persist=True)


def get_output_svg(results: List[Tuple[int, str]]) -> ElementTree.Element:
    """ This is a helper function to get the output SVG from the results of the `packaide.pack` function.

    This asserts that all shapes have been fit onto a single SVG element (that `results` is len of 1)

    Parameters:
        `results` - The first element returned by the `packaide.pack` function.

    Returns:
        The output SVG as an `ElementTree.Element` object.
    """
    assert len(results) == 1

    output = results[0][1]
    return ElementTree.fromstring(output)


class ViewBoxTests(unittest.TestCase):
    """ These tests are to see what affect the viewBox has on the output SVG.

    The conclusion is that the viewBox does not affect the output SVG. Therefore, when multiple SVGs are combined into
    a single SVG, the resulting SVG will be given a viewBox of a fixed size.

    The reason these tests were necessary is that `packaide.pack` throws an error if the viewBox is not set.
    """

    def test_fails_without_size(self):
        """ This test shows that nesting fails if no `viewBox` is defined. """
        shapes = """
        <svg>
          <rect width="100" height="50" />
          <rect width="50" height="100" />
          <ellipse rx="20" ry="20" />
        </svg>
        """
        with self.assertRaises(ValueError):
            do_pack(shapes)

    def test_output_size(self):
        """ This tests that the output SVG is the same size as the sheet given.

        Question: What happens when the viewBox of the input "shapes" is smaller than the `SHEET`?
        Conclusion: the output SVG keeps the dimensions defined by `SHEET`
        """
        # here we have an SVG where all shapes exist within the viewBox
        shapes = """
        <svg viewBox="0 0 432.13 593.04">
          <rect width="100" height="50" />
          <rect width="50" height="100" />
          <ellipse rx="20" ry="20" />
        </svg>
        """
        results, placed, failed = do_pack(shapes)

        self.assertEqual(placed, 3)
        self.assertEqual(failed, 0)
        self.assertEqual(len(results), 1)

        nested = get_output_svg(results)
        self.assertEqual(nested.attrib['viewBox'],
                         '0 0 {width} {height}'.format(width=SHEET_WIDTH, height=SHEET_HEIGHT))

    def test_shapes_escape_edges(self):
        """ This tests that shapes are still properly nested when one of the shapes extends beyond the edges of it's
        viewBox.

        Question: What happens when the input shapes SVG is too small to enclose all the shapes?
        Conclusion: Shape is still placed even when the viewBox is too small.
        """
        # 2 out of 3 of these shapes extend beyond the viewBox
        shapes = """
        <svg viewBox="0 0 30 90">
          <rect width="100" height="50" />
          <rect width="50" height="100" />
          <ellipse rx="20" ry="20" />
        </svg>"""

        results, placed, failed = do_pack(shapes)

        self.assertEqual(placed, 3)
        self.assertEqual(failed, 0)

        # viewBox still maintains the size of `SHEET`
        nested = get_output_svg(results)
        self.assertEqual(nested.attrib['viewBox'],
                         '0 0 {width} {height}'.format(width=SHEET_WIDTH, height=SHEET_HEIGHT))

    def test_shape_exists_outside_of_bounds(self):
        """ What happens when a shape entirely exists outside the viewBox?

        Question: What if a shape does not intersect with the viewBox at all?
        Conclusion: Shape is still placed correctly even when it is incorrectly placed.
        """

        # here, one of the `<rect>` objects exists entirely outside the viewBox
        shapes = """
        <svg viewBox="0 0 32.13 93.04">
          <rect width="100" height="50" />
          <rect width="50" height="100" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <ellipse rx="20" ry="20" />
        </svg>"""

        results, placed, failed = do_pack(shapes)

        self.assertEqual(placed, 4)
        self.assertEqual(failed, 0)

        # viewBox still maintains the size of `SHEET`
        nested = get_output_svg(results)
        self.assertEqual(nested.attrib['viewBox'],
                         '0 0 {width} {height}'.format(width=SHEET_WIDTH, height=SHEET_HEIGHT))

    def test_fixed_window(self):
        """ Does the viewBox matter at all?
        """

        # here is an SVG with a total view window of 1x1
        shapes = """
        <svg viewBox="0 0 1 1">
          <rect width="100" height="50" />
          <rect width="1000" height="1000" x="1000" y="1000" />
        </svg>"""

        results, placed, failed = do_pack(shapes)

        self.assertEqual(placed, 2)
        self.assertEqual(failed, 0)

        # viewBox still maintains the size of `SHEET`
        nested = get_output_svg(results)
        self.assertEqual(nested.attrib['viewBox'],
                         '0 0 {width} {height}'.format(width=SHEET_WIDTH, height=SHEET_HEIGHT))


class PlacementTests(unittest.TestCase):
    """ These tests are to see what affect the placement of shapes has on the output SVG.

    The conclusion is that the placement of shapes has no effect on the output SVG. Therefore, when multiple SVGs
    are overlapping, shapes will be nested regardless of their original placement.
    """

    def test_overlapping_shapes(self):
        """ This test shows that shapes may overlap. This has been visually verified.

        Question: What if all shapes are overlapping?
        Conclusion: Placement of shapes have no effect on resulting SVG.
        """

        # here is an SVG where all 8 shapes are overlapping. This shapes barely fit on `SHEET`
        shapes = """
        <svg viewBox="0 0 1 1">
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
        </svg>"""

        results, placed, failed = do_pack(shapes)

        self.assertEqual(8, placed)
        self.assertEqual(0, failed)

        # viewBox still maintains the size of `SHEET`
        nested = get_output_svg(results)
        self.assertEqual(nested.attrib['viewBox'],
                         '0 0 {width} {height}'.format(width=SHEET_WIDTH, height=SHEET_HEIGHT))

    def test_too_many_shapes(self):
        """ What happens when sheet is purposefully overloaded.
        """

        # here is an SVG where all 10 shapes are overlapping. 2 of these shapes cannot fit.
        shapes = """
        <svg viewBox="0 0 1 1">
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
        </svg>"""

        results, placed, failed = do_pack(shapes)

        self.assertEqual(8, placed)
        self.assertEqual(2, failed)

        # viewBox still maintains the size of `SHEET`
        nested = get_output_svg(results)
        self.assertEqual(nested.attrib['viewBox'],
                         '0 0 {width} {height}'.format(width=SHEET_WIDTH, height=SHEET_HEIGHT))

    def test_second_sheet(self):
        """ What happens when a second `SHEET` is passed. Will shapes be fit onto the new sheet?

        This test will be used to build functionality that ensures that all sheets are placed.
        """
        shapes = """
        <svg viewBox="0 0 1 1">
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
        </svg>"""

        results, placed, failed = packaide.pack([SHEET, SHEET], shapes)

        self.assertEqual(10, placed)
        self.assertEqual(0, failed)

        # a second SVG with the remaining shapes is returned.
        self.assertEqual(2, len(results))


class GroupingTests(unittest.TestCase):
    """ These tests are to see what affect grouping of SVG elements has on the output SVG.

    Since Inkscape and other SVG editors seem to output SVGs with a variety of grouping, it is important to ensure that
    the `packaide` module can handle these cases.
    """
    def test_some_grouped_shapes(self):
        """ What happens when multiple SVG elements are grouped together?

        Question: What when some objects are grouped together, and some are not, are all the shapes nested?
        Conclusion: All shapes are nested regardless of grouping.
        """
        shapes = """
        <svg viewBox="0 0 1 1">
          <g>
            <rect width="1000" height="1000" x="1000" y="1000" />
            <rect width="1000" height="1000" x="1000" y="1000" />
          </g>
          <rect width="1000" height="1000" x="1000" y="1000" />
          <rect width="1000" height="1000" x="1000" y="1000" />
        </svg>"""

        results, placed, failed = do_pack(shapes)

        self.assertEqual(4, placed)
        self.assertEqual(0, failed)

        # viewBox still maintains the size of `SHEET`
        nested = get_output_svg(results)
        self.assertEqual(nested.attrib['viewBox'],
                         '0 0 {width} {height}'.format(width=SHEET_WIDTH, height=SHEET_HEIGHT))

    def test_all_grouped_shapes(self):
        """ What happens when all SVG elements are grouped together?

        Question: What happens when all objects are grouped together?
        Conclusion: All shapes are nested regardless of grouping.
        """
        shapes = """
        <svg viewBox="0 0 1 1">
          <g>
            <rect width="1000" height="1000" x="1000" y="1000" />
            <rect width="1000" height="1000" x="1000" y="1000" />
            <rect width="1000" height="1000" x="1000" y="1000" />
          </g>
        </svg>
        """

        results, placed, failed = do_pack(shapes)

        self.assertEqual(3, placed)
        self.assertEqual(0, failed)

        # viewBox still maintains the size of `SHEET`
        nested = get_output_svg(results)
        self.assertEqual(nested.attrib['viewBox'],
                         '0 0 {width} {height}'.format(width=SHEET_WIDTH, height=SHEET_HEIGHT))

    def test_deep_grouping(self):
        """ What happens when SVG elements are grouped multiple levels deep? """
        shapes = """
        <svg viewBox="0 0 1 1">
            <g>
                <g>
                    <g><g>
                        <rect width="1000" height="1000" x="1000" y="1000" />
                        <rect width="1000" height="1000" x="1000" y="1000" />
                    </g></g>
                <rect width="1000" height="1000" x="1000" y="1000" />
                </g>
            </g>
            <rect width="1000" height="1000" x="1000" y="1000" />
        </svg>
        """

        results, placed, failed = do_pack(shapes)

        self.assertEqual(4, placed)
        self.assertEqual(0, failed)


if __name__ == '__main__':
    unittest.main()
