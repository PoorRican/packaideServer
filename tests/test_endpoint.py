import unittest
from xml.etree import ElementTree

from fastapi.testclient import TestClient
from main import app
from utils import NO_SHAPE_FITS, ONE_SHAPE_TOO_BIG


class TestPackEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_basic_operation(self):
        """ Test that two SVGs are combined into one sheet """
        total_number_of_shapes = 3

        shape1 = """
        <svg>
        <rect height="100" width="100" />
        </svg>
        """

        shape2 = """
        <svg>
        <rect height="100" width="100" />
        <rect height="100" width="100" />
        </svg>
        """

        # Define a request body and make request
        request_data = {
            "height": 40,
            "width": 60,
            "shapes": [shape1, shape2]
        }

        response = self.client.post("/pack", json=request_data)

        # Assert that the response is successful
        self.assertEqual(response.status_code, 200)

        # Assert the correct number of output sheets
        outputs = response.json()

        self.assertEqual(1, len(outputs))

        # Assert the correct number of shapes
        output_as_xml = ElementTree.fromstring(outputs[0])

        self.assertEqual(total_number_of_shapes, len(output_as_xml))

    def test_multiple_sheets(self):
        """ Test that two SVGs are combined into one sheet """
        total_number_of_shapes = 4

        shape1 = """
        <svg>
        <rect height="100" width="100" />
        </svg>
        """

        shape2 = """
        <svg>
        <rect height="100" width="100" />
        <rect height="100" width="100" />
        <rect height="50" width="50" />
        </svg>
        """

        # Define a request body and make request
        request_data = {
            "height": 2,
            "width": 2,
            "shapes": [shape1, shape2]
        }

        response = self.client.post("/pack", json=request_data)

        # Assert that the response is successful
        self.assertEqual(response.status_code, 200)

        # Assert the correct number of output sheets
        outputs = response.json()

        self.assertEqual(3, len(outputs))

        # Assert the correct number of shapes
        shape_counter = 0
        for output in outputs:
            output_as_xml = ElementTree.fromstring(output)
            shape_counter += len(output_as_xml)

        self.assertEqual(total_number_of_shapes, shape_counter)

    def test_no_shapes_fit(self):
        """ Test when no given shapes fit onto the sheet """
        shape1 = """
        <svg>
        <rect height="100" width="100" />
        </svg>
        """

        shape2 = """
        <svg>
        <rect height="100" width="100" />
        <rect height="100" width="100" />
        </svg>
        """

        # Define a request body and make request
        request_data = {
            "height": 1,
            "width": 1,
            "shapes": [shape1, shape2]
        }

        response = self.client.post("/pack", json=request_data)

        # Assert that the response is successful
        self.assertEqual(response.status_code, 400)

        # Assert that the correct error code is returned
        parsed = response.json()
        detail = parsed['detail']

        self.assertEqual(NO_SHAPE_FITS, detail)

    def test_one_shape_too_large(self):
        """ Test when one shape is too large to fit onto a sheet """
        shape1 = """
        <svg>
        <rect height="100" width="100" />
        </svg>
        """

        shape2 = """
        <svg>
        <rect height="100" width="100" />
        <rect height="100" width="1000" />
        </svg>
        """

        # Define a request body and make request
        request_data = {
            "height": 2,
            "width": 2,
            "shapes": [shape1, shape2]
        }

        response = self.client.post("/pack", json=request_data)

        # Assert that the response is successful
        self.assertEqual(response.status_code, 400)

        # Assert that the correct error code is returned
        parsed = response.json()
        detail = parsed['detail']

        self.assertEqual(ONE_SHAPE_TOO_BIG, detail)


if __name__ == '__main__':
    unittest.main()