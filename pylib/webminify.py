import csscompressor  # type: ignore
import re


def minify_css_blocks(html_code: str) -> str:
    remaining_code = html_code

    start_tag = re.compile(r"<\s*style[^>]*>")
    end_tag = re.compile(r"<\s*/\s*style[^>]*>")

    last_location = 0

    new_html_code = ""

    while True:
        # Find Open Bracket
        start_match = start_tag.search(remaining_code, last_location)

        # If there are no more start style tags exit loop
        if (start_match is None):
            break

        # Grab the character directly after the match
        start_location = start_match.span()[1]

        new_html_code += html_code[last_location:start_location]
        last_location = start_location

        # Find Close Tag
        end_match = end_tag.search(remaining_code, last_location)
        if end_match is None:
            print("ERROR IN CALCULATOR TEMPLATE: No Closing </style> tag found")
            break

        # Minify the CSS and add it to the html code
        css = html_code[start_location:end_match.span()[0]]
        min_css = csscompressor.compress(css)

        new_html_code += min_css

        # Add the ending tag to the new HTML
        new_html_code += html_code[end_match.span()[0]:end_match.span()[1]]

        # Start Searching for the next chunk after the ending tag
        last_location = end_match.span()[1]

    new_html_code += html_code[last_location:]

    return new_html_code
