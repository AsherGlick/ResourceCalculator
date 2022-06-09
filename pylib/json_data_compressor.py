import json
from jinja2 import Environment
from typing import Dict, Optional, Any, Tuple

from pylib.uglifyjs import uglify_js_string


################################################################################
# Resource Calculator has a lot of stringy representation of mappings between
# different attributes. From the name of a resource being defined to the names
# of the resources required in a recipe there are a lot of duplicated strings
# in our data structure. This library creates a javascript string that
# represents the same data but in a much smaller footprint by extracting all of
# the keys and values in an an object and replacing them with indices.
#
# This is also dramatically reduces the size when having constantly named keys.
#
# A downside to this simple compression model is that even small integers need
# to be swapped out for indices. So it is possible some keys will become larger
# as they might change from "5" to "52" as the integer 5 will be in the 52nd
# index of the tokens. To combat this in the general case there is an escape
# for when we have minified to a larger binary then the original.
#
# We do not compress the tokens further then this deduplication because the
# final file will likely be gzipped and doing more compression here would be
# redundant and only server to make things more complex.
################################################################################
def mini_js_data(data: Any, variable_name: str) -> str:
    # This is a javascript function that gets prepended to the data so that it
    # can be decompressed on-load.
    javascript_reverser = """
    var {{variable_name}} = function () {
        var data = {{data}};
        var tokens = {{tokens}};
        return _uncompress(data, tokens);
    }();
    function _uncompress(data, tokens){
        if (typeof data === "object"){
            // Unpacking Array
            if (Array.isArray(data)) {
                for (var i in data) {
                    data[i] = _uncompress(data[i], tokens)
                }
                return data
            }
            // Unpacking Dictonary
            else {
                var new_data = {};
                for (var i in data) {
                    new_data[_uncompress(i, tokens)] = _uncompress(data[i], tokens)
                }
                return new_data
            }
        }
        // Unpacking Scalar
        else {
            return tokens[data]
        }
    }
    """

    (packed_data, tokens) = _mini_js_data(data)
    packed_json = Environment().from_string(javascript_reverser).render(
        variable_name=variable_name,
        data=json.dumps(packed_data),
        tokens=json.dumps(tokens),
    )
    uglified_packed_json = uglify_js_string(packed_json)

    # Do a simple sanity check to make sure our compression is not increasing the size
    uglified_raw_json = uglify_js_string("var " + variable_name + " = " + json.dumps(data))
    if len(uglified_raw_json) > len(uglified_packed_json):
        return uglified_packed_json
    else:
        return uglified_raw_json


################################################################################
# This function counts up all the token instances and assigned a lower index
# to the most used tokens. This is so we can have the most used tokens use the
# indices with the smallest character counts. Eg: If "null" is present 100
# times in the datastructure, if we give it an index of 1 it will only take up
# 100 characters, but if we give it an index of 12 it will take up 200
# characters.
#
# From basic testing this showed to give ~8% further decrease in size from
# using basically random indices
################################################################################
def _mini_js_data(data: Any) -> Tuple[Any, Any]:
    token_counts = get_token_counts(data)
    sorted_tokens = [k for k, v in sorted(token_counts.items(), key=lambda item: item[1], reverse=True)]
    token_map = {token: index for (index, token) in enumerate(sorted_tokens)}

    new_data = replace_data(data, token_map)

    return new_data, sorted_tokens


################################################################################
# This function goes through the datastructure and replaces all the tokens with
# their index as described in the token_map
################################################################################
def replace_data(data: Any, token_map: Dict[Any, int]) -> Any:
    # If this node is a dictionary process each key of it and recurse the values
    if isinstance(data, dict):
        new_dict = {}
        for i in data:
            # Key Replacement
            key_token_index = token_map[i]

            # Value replacement
            element = replace_data(data[i], token_map)
            new_dict[key_token_index] = element
        return new_dict
    # If this node is a list recuse each element of it
    elif isinstance(data, list):
        new_list = []
        for i in data:
            element = replace_data(i, token_map)
            new_list.append(element)
        return new_list
    else:
        new_data = token_map[data]
        return new_data

    # return (new_data)


################################################################################
# This function goes through the datastructure and counts up all the instances
# of a particular token so that we can know which ones are the most used and
# which ones are the least used.
################################################################################
def get_token_counts(data: Any, tokens: Optional[Dict[Any, int]] = None) -> Dict[Any, int]:
    if tokens is None:
        tokens = {}
    # If this node is a dictionary process each key of it and recurse the values
    if isinstance(data, dict):
        for i in data:
            # Process the Key as a token
            if i not in tokens:
                tokens[i] = 0
            tokens[i] += 1

            # Process the value tokens
            tokens = get_token_counts(data[i], tokens)

    # If this node is a list recuse each element of it
    elif isinstance(data, list):
        for i in data:
            tokens = get_token_counts(i, tokens)
    else:
        if data not in tokens:
            tokens[data] = 0
        tokens[data] += 1
    return tokens
