import unittest
from xml.etree import ElementTree

from fastapi.testclient import TestClient
from main import app


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


if __name__ == '__main__':
    unittest.main()