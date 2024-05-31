import xml.etree.ElementTree as et
from typing import LiteralString

NO_SHAPE_FITS: LiteralString = "Sheet size is too small for shapes"
ONE_SHAPE_TOO_BIG: LiteralString = "One shape is too large for sheet"


def _aggregate_svg_elements(svg_list: list[str]) -> et.Element:
    """ Combine a list of SVG strings into a single SVG XML element

    Example:
        >>> svg1 = '<svg><circle cx="50" cy="50" r="40" fill="red" /></svg>'
        >>> svg2 = '<svg><rect width="80" height="80" fill="blue" /></svg>'
        >>> len(_aggregate_svg_elements([svg1, svg2]))
        2

    """
    # Create the root element of the combined SVG
    combined_svg = et.Element('svg', {'xmlns': 'http://www.w3.org/2000/svg'})

    for svg_string in svg_list:
        root = et.fromstring(svg_string)

        # Append each child element of the SVG to the combined SVG
        for child in root:
            combined_svg.append(child)

    return combined_svg


def _set_viewbox(svg: et.Element) -> et.Element:
    """ Set the viewBox of an SVG element to a fixed size.

    The viewBox does not affect the output SVG. For some reason, it is necessary within the `packaide` code.
    There have been tests that confirm that the viewBox has no effect the output SVG. See `test_packaide.py` for more
    information. Therefore, when multiple elements are combined into a single SVG, the resulting SVG will be given
    a viewBox of a fixed size.
    """
    svg.attrib['viewBox'] = '0 0 100 100'

    return svg


def combine_svg(svg_list: list[str]) -> str:
    """ Combine multiple SVG files and return a string.

    All inner children of the SVG elements are combined into a single SVG element. The viewBox of the resulting SVG
    is set to a fixed size. The resulting SVG is returned as a string.

    Example:
        >>> svg1 = '<svg><circle cx="50" cy="50" r="40" fill="red" /></svg>'
        >>> svg2 = '<svg><rect width="80" height="80" fill="blue" /></svg>'
        >>> _combined: str = combine_svg([svg1, svg2])
    """
    combined = _aggregate_svg_elements(svg_list)
    combined = _set_viewbox(combined)

    return et.tostring(combined).decode('utf8')


def generate_sheet(width: float, height: float, dpi: int = 96) -> str:
    """ Generate an SVG sheet with a given height and width.

    The sheet is returned as a string.

    Parameters:
        width (float): The width of the sheet in inches.
        height (float): The height of the sheet in inches.
        dpi (int): The DPI of the sheet. Defaults to 96.

    Example:
        >>> _: str = generate_sheet(100, 100)
    """
    pixel_width = width * dpi
    pixel_height = height * dpi

    sheet = """<svg
       viewBox="0 0 {width} {height}"
       version="1.1"
       xmlns="http://www.w3.org/2000/svg"
       xmlns:svg="http://www.w3.org/2000/svg" ></svg>""".format(width=pixel_width, height=pixel_height)

    return sheet


def perform_pack(shapes: str, sheet: str,
                 tolerance: float,
                 offset: float,
                 rotations: int
                 ) -> list[str]:
    """ Perform the packing operation.

    The `packaide.pack` function is called with the given shapes and sheet. The resulting SVGs are returned as a list
    of strings.

    Parameters:
        shapes (str): A single SVG string, or a list of SVG strings, to pack onto the sheet.
        sheet (str): An SVG string representing the sheet to pack onto.
        tolerance (float): The tolerance of the packing algorithm.
        offset (float): The offset of the packing algorithm.
        rotations (int): The number of rotations to use.

    Raises:
        `ValueError` when:
            - Sheet size is too small to fit any shape
            - One shape is too large to fit onto sheet

    Example:
        >>> _shapes = '<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="red" /></svg>'
        >>> _sheet = '<svg viewBox="0 0 1 1"></svg>'
        >>> _ = perform_pack(_shapes, _sheet)
    """
    import packaide

    # get the number of shapes
    shapes_as_xml = et.fromstring(shapes)
    total_number_of_shapes = len(shapes_as_xml)

    sheet_count = 1     # number of sheets to use

    # this continues to run until there are no failed placed sheets
    while True:
        results, _, failed = packaide.pack(
            [sheet] * sheet_count,
            shapes,
            tolerance=tolerance,
            offset=offset,
            partial_solution=True,
            rotations=rotations,
            persist=False
        )

        if failed == 0:
            break
        elif failed == total_number_of_shapes:
            raise ValueError(NO_SHAPE_FITS)
        elif sheet_count > total_number_of_shapes:
            raise ValueError(ONE_SHAPE_TOO_BIG)
        else:
            sheet_count += 1

    sheets: list[str] = []
    for _, out in results:
        sheets.append(out)

    return sheets
