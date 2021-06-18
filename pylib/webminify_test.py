from .webminify import minify_css_blocks
import unittest
import sys
import io


class Test_Minify(unittest.TestCase):

    ############################################################################
    # Test that a simple html block can be parsed and compressed
    ############################################################################
    def test_minify(self) -> None:
        output = minify_css_blocks("<html><style>body:{ background: #CCC; }</style></html>")
        self.assertEqual(output, "<html><style>body:{background:#CCC}</style></html>")

    ############################################################################
    # Test that a warning is printed when the end </style> tag cannot be found
    ############################################################################
    def test_minify_closing_style_tag_missing(self) -> None:
        input_html = "<html><style>body:{ background: #CCC; }</html>"

        captured_output = io.StringIO()
        sys.stdout = captured_output
        output = minify_css_blocks(input_html)
        sys.stdout = sys.__stdout__

        self.assertEqual(output, input_html)
        self.assertEqual(captured_output.getvalue(), "ERROR IN CALCULATOR TEMPLATE: No Closing </style> tag found\n")
