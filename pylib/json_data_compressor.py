import json
from jinja2 import Environment
from typing import Dict, Optional, Any, Tuple, Generator

from pylib.uglifyjs import uglify_js_string


################################################################################
# Resource Calculator has a lot of stringy representation of mappings between
# different attributes. From the name of a resource being defined to the names
# of the resources required in a recipe there are a lot of duplicated strings
# in our data structure. This library creates a javascript string that
# represents the same data but in a much smaller footprint by extracting all of
# the keys and values in an an object and replacing them with indecies.
#
# This is also dramatically reduces the size when having constantly named keys.
#
# A downside to this simple compression model is that even small integers need
# to be swapped out for indecies. So it is possible some keys will become larger
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


    packed_json2 = mini_js_data2(data, variable_name+"packed")
    uglified_packed_json2 = uglify_js_string(packed_json2)


    # Do a simple sanity check to make sure our compression is not increasing the size
    raw_json = "var raw_recipe_json = " + json.dumps(data)
    uglified_raw_json = uglify_js_string(raw_json)


    print(len(packed_json), len(uglified_packed_json))
    print(len(packed_json2), len(uglified_packed_json2))
    print(len(raw_json), len(uglified_raw_json))


    with open("speed_profiling/packed_json2.js", 'w') as f:
        f.write(packed_json2)

    with open("speed_profiling/packed_json2.min.js", 'w') as f:
        f.write(uglified_packed_json2)


    with open("speed_profiling/packed_json.js", 'w') as f:
        f.write(packed_json)

    with open("speed_profiling/packed_json.min.js", 'w') as f:
        f.write(uglified_packed_json)


    with open("speed_profiling/raw_json.js", 'w') as f:
        f.write(raw_json)

    with open("speed_profiling/raw_json.min.js", 'w') as f:
        f.write(raw_json)

    exit(42)

    # print("PACKED JSON")
    # print(packed_json)
    # print("UGLIFIED_PACKED JSON")
    # print(uglified_packed_json)

    # print("RAW JSON")
    # print(raw_json)
    # print("UGLIFIED JSON")
    # print(uglified_raw_json)

    # exit(1)

    if len(uglified_raw_json) > len(uglified_packed_json):
        return uglified_packed_json
    else:
        return uglified_raw_json


################################################################################
# This function counts up all the token instances and assigned a lower index
# to the most used tokens. This is so we can have the most used tokens use the
# indecies with the smallest character counts. Eg: If "null" is present 100
# times in the datastructure, if we give it an index of 1 it will only take up
# 100 characters, but if we give it an index of 12 it will take up 200
# characters.
#
# From basic testing this showed to give ~8% further decrease in size from
# using basically random indecies
################################################################################
def _mini_js_data(data: Any) -> Tuple[Any, Any]:
    token_counts = get_token_counts(data)
    sorted_tokens = [k for k, v in sorted(token_counts.items(), key=lambda item: item[1], reverse=True)]
    token_map = {token: index for (index, token) in enumerate(sorted_tokens)}

    new_data = replace_data(data, token_map)

    return new_data, sorted_tokens


################################################################################
# This function goes through the datastructure and replaces all the tokens with
# their index as desribed in the token_map
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


# [key count, value count]
def get_token_counts2(data: Any, tokens: Dict[Any, Tuple[int, int]]) -> Dict[Any, Tuple[int, int]]:
    
    if isinstance(data, dict):
        for i in data:
            # Process the key as a key token
            if i not in tokens:
                tokens[i] = (0, 0)
            tokens[i] = (tokens[i][0]+1, tokens[i][1])

            # Process value tokens
            tokens = get_token_counts2(data[i], tokens)

    elif isinstance(data, list):
        for i in data:
            tokens = get_token_counts2(i, tokens)
    else:
        if data not in tokens:
            tokens[data] = (0, 0)
        tokens[data]     =(tokens[data][0], tokens[data][1]+ 1)
    return tokens


################################################################################
# converts an integer into an alphanumeric string where the first character is
# always a letter while the subequent characters can be numbers
################################################################################
symbols = ["$", "_"]
lowercase = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
uppercase = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
digits = ["0","1","2","3","4","5","6","7","8","9"]
characters = lowercase + uppercase + symbols + digits
start_characters = lowercase + uppercase + symbols
restricted_words = set(["do", "if", "in", "for", "int", "let", "new", "try", "var", "byte", "case", "char", "else",
                        "enum", "eval", "goto", "long", "null", "this", "true", "void", "with", "await", "break",
                        "catch", "class", "const", "false", "final", "float", "short", "super", "throw", "while",
                        "yield", "delete", "double", "export", "import", "native", "public", "return", "static",
                        "switch", "throws", "typeof", "boolean", "default", "extends", "finally", "package", "private",
                        "abstract", "continue", "debugger", "function", "volatile", "arguments", "interface",
                        "protected", "transient", "implements", "instanceof", "synchronized"])

def token_generator() -> Generator[str, None, None]:
    token_value = [0]
    yield 'a'
    while(True):
        token_value[-1] += 1

        # Propagate all digits
        for i in reversed(range(len(token_value))):
            if token_value[i] >= len(characters):
                token_value[i-1] += 1
                token_value[i] = 0

        # Propagate most significant digit, limit to only letters
        if token_value[0] >= len(start_characters):
            token_value[0] = 0
            token_value.insert(0, 0)

        value_to_yield = ''.join([characters[c] for c in token_value])

        if value_to_yield in restricted_words:
            continue

        yield value_to_yield



def javascript_key(value: Any) -> str:
    if type(value) == str:
        if len(value) == 0:
            return '""'
        if value[0] not in start_characters:
            return json.dumps(value)
        for i in value:
            if i not in characters:
                return json.dumps(value)

        return value

    if type(value) == int:
        return str(value)

    return json.dumps(value)



################################################################################
# A second attempt to create a minimizer that is smaller and more perfomant
# when being decoded.
################################################################################
def mini_js_data2(data: Any, variable_name: str) -> str:
    print("Mini JS 2")
    token_counts = get_token_counts2(data, {})
    sorted_tokens = [(k,v) for k, v in sorted(token_counts.items(), key=lambda item: item[1][0] + item[1][1], reverse=True)]
    # token_map = {token: index for (index, token) in enumerate(sorted_tokens)}
    token_map: Dict[Any, Tuple[str, str]] = {}

    # print(token_counts)

    variable_definitions = []

    token_gen = token_generator()
    next_token = next(token_gen)

    for token in sorted_tokens:
        raw_value = token[0]
        json_value = json.dumps(raw_value)
        json_key = javascript_key(raw_value)

        key_instance_count = token[1][0]
        value_instance_count = token[1][1]

        uncompressed_length = key_instance_count * len(json_key) + value_instance_count * len(json_value)


        compressed_definition = next_token+"="+json_value

        compressed_key = "[" + next_token + "]"
        compressed_value = next_token

        keys_length = len(compressed_key) * key_instance_count
        values_length = len(compressed_value) * value_instance_count

        compress_length = keys_length + values_length + len(compressed_definition) + 1


        # print()

        # print(json_value, instance_count, base_length, compress_length, base_length > compress_length)

        if compress_length < uncompressed_length:
            token_map[raw_value] = (compressed_key, compressed_value)
            variable_definitions.append(compressed_definition)
            next_token = next(token_gen)

        else:
            token_map[raw_value] = (json_key, json_value)


    # print("token map", token_map)
    # print("definitions", variable_definitions)

    # json_out = "let " + variable_name + "=" + dump_tokened_json(data, token_map)
    json_out =  dump_tokened_json(data, token_map)


    inline_variables = "let " + ",".join(variable_definitions) + ";"

    return "let " + variable_name + "=function(){" + inline_variables + "return" + json_out + "}()"


def dump_tokened_json(data: Any, token_map: Dict[Any, Tuple[str, str]]) -> str:
    # If this node is a dictionary process each key of it and recurse the values
    if isinstance(data, dict):
        new_dict = []
        for i in data:
            # Key Replacement
            key_token = token_map[i][0]

            # Value replacement
            element = dump_tokened_json(data[i], token_map)
            new_dict.append(key_token + ":" + element)
        return "{" + ",".join(new_dict) + "}"
    # If this node is a list recuse each element of it
    elif isinstance(data, list):
        new_list = []
        for i in data:
            element = dump_tokened_json(i, token_map)
            new_list.append(element)
            # new_list.append(",")
        # new_list.append("]")
        return "[" + ",".join(new_list) + "]"
    else:
        return token_map[data][1]
