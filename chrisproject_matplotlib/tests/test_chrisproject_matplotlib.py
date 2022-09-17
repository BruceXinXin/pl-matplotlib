import os
from unittest import TestCase
from unittest import mock
from chrisproject_matplotlib.chrisproject_matplotlib import ChrisprojectMatplotlib


class ChrisprojectMatplotlibTests(TestCase):
    """
    Test ChrisprojectMatplotlib.
    """
    def setUp(self):
        self.app = ChrisprojectMatplotlib()
        self.test_directory = os.path.abspath(os.path.dirname(__file__))
        self.output_directory = self.test_directory + "/test_data/outputdata"
        os.makedirs(self.output_directory, exist_ok=True)

    def test_run(self):
        """
        Test the run code.
        """
        args = []
        if self.app.TYPE == 'ds':
            args.append(self.test_directory + "/test_data/inputdata") # you may want to change this inputdir mock
        args.append(self.output_directory)  # you may want to change this outputdir mock

        # you may want to add more of your custom defined optional arguments to test
        # your app with
        # eg.
        # args.append('--custom-int')
        # args.append(10)

        options = self.app.parse_args(args)
        self.app.run(options)

        # write your own assertions
        self.assertIn('SAG-anon.png', os.listdir(os.path.join(self.output_directory)))

    def tearDown(self):
        os.rmdir(self.output_directory)
