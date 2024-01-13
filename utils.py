import xml.etree.ElementTree as et


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
