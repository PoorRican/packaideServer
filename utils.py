import xml.etree.ElementTree as et


def _aggregate_svg_elements(svg_list: list[str]) -> et.Element:
    """ Combine a list of SVG strings into a single SVG XML element

    Example:
        >>> svg1 = '<svg><circle cx="50" cy="50" r="40" fill="red" /></svg>'
        >>> svg2 = '<svg><rect width="80" height="80" fill="blue" /></svg>'
        >>> combined = _aggregate_svg_elements([svg1, svg2])
        >>> assert len(combined) == 2

    """
    # Create the root element of the combined SVG
    combined_svg = et.Element('svg', {'xmlns': 'http://www.w3.org/2000/svg'})

    for svg_string in svg_list:
        root = et.fromstring(svg_string)

        # Append each child element of the SVG to the combined SVG
        for child in root:
            combined_svg.append(child)

    return combined_svg


def combine_svg(svg_list: list[str]) -> str:
    """ Combine multiple SVG files and return a string.

    Example:
        >>> svg1 = '<svg><circle cx="50" cy="50" r="40" fill="red" /></svg>'
        >>> svg2 = '<svg><rect width="80" height="80" fill="blue" /></svg>'
        >>> combine_svg([svg1, svg2])
    """
    combined = _aggregate_svg_elements(svg_list)

    return et.tostring(combined).decode('utf8')
