from collections import OrderedDict
from typing import Any, TextIO, Type
from typing import NamedTuple
import yaml


class TokenBundle(NamedTuple):
    value: Any
    token: yaml.nodes.ScalarNode


def tuple_string_constructor(loader: Any, node: yaml.nodes.ScalarNode) -> TokenBundle:
    return TokenBundle(loader.construct_yaml_str(node), node)


def tuple_null_constructor(loader: Any, node: yaml.nodes.ScalarNode) -> TokenBundle:
    return TokenBundle(loader.construct_yaml_null(node), node)


def tuple_int_constructor(loader: Any, node: yaml.nodes.ScalarNode) -> TokenBundle:
    return TokenBundle(loader.construct_yaml_int(node), node)


def tuple_bool_constructor(loader: Any, node: yaml.nodes.ScalarNode) -> TokenBundle:
    return TokenBundle(loader.construct_yaml_bool(node), node)


def placeholder_constructor(loader: Any, node: yaml.nodes.ScalarNode) -> None:
    raise(ValueError("ERROR: YAML Element Found For Placeholder Constructor {}".format(node)))


################################################################################
# ordered_load
#
# This function will load in the yaml recipe file but maintain the order of the
# items. This allows us to simplify the file definition making it easier for
# humans to use while also allowing us to set the order of the items for easy
# grouping
################################################################################
def ordered_load(stream: TextIO, object_pairs_hook: Type[object] = OrderedDict) -> Any:
    class OrderedLoader(yaml.SafeLoader):
        pass

    # Ordered Load
    def construct_mapping(loader, node):  # type: ignore
        loader.flatten_mapping(node)
        pairs = loader.construct_pairs(node)
        return object_pairs_hook(pairs)  # type: ignore

    OrderedLoader.add_constructor(  # type: ignore
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)

    # Tokenized Load
    OrderedLoader.add_constructor(  # type: ignore
        'tag:yaml.org,2002:null',
        tuple_null_constructor
    )

    OrderedLoader.add_constructor(  # type: ignore
        'tag:yaml.org,2002:bool',
        tuple_bool_constructor
    )

    OrderedLoader.add_constructor(  # type: ignore
        'tag:yaml.org,2002:int',
        tuple_int_constructor
    )

    OrderedLoader.add_constructor(  # type: ignore
        'tag:yaml.org,2002:float',
        placeholder_constructor  # TODO: Maybe Add TokenBundle Wrapper
        # SafeConstructor.construct_yaml_float)
    )

    OrderedLoader.add_constructor(  # type: ignore
        'tag:yaml.org,2002:binary',
        placeholder_constructor  # TODO: Maybe Add TokenBundle Wrapper
        # SafeConstructor.construct_yaml_binary)
    )

    OrderedLoader.add_constructor(  # type: ignore
        'tag:yaml.org,2002:timestamp',
        placeholder_constructor  # TODO: Maybe Add TokenBundle Wrapper
        # SafeConstructor.construct_yaml_timestamp)
    )

    OrderedLoader.add_constructor(  # type: ignore
        'tag:yaml.org,2002:omap',
        placeholder_constructor  # TODO: Maybe Add TokenBundle Wrapper
        # SafeConstructor.construct_yaml_omap)
    )

    OrderedLoader.add_constructor(  # type: ignore
        'tag:yaml.org,2002:pairs',
        placeholder_constructor  # TODO: Maybe Add TokenBundle Wrapper
        # SafeConstructor.construct_yaml_pairs)
    )

    OrderedLoader.add_constructor(  # type: ignore
        'tag:yaml.org,2002:set',
        placeholder_constructor  # TODO: Maybe Add TokenBundle Wrapper
        # SafeConstructor.construct_yaml_set)
    )

    OrderedLoader.add_constructor(  # type: ignore
        'tag:yaml.org,2002:str',
        tuple_string_constructor
    )

    # No need to overwrite the Array and Map nodes
    # OrderedLoader.add_constructor(  # type: ignore
    #         'tag:yaml.org,2002:seq',
    #         SafeConstructor.construct_yaml_seq)

    # OrderedLoader.add_constructor(  # type: ignore
    #         'tag:yaml.org,2002:map',
    #         SafeConstructor.construct_yaml_map)

    OrderedLoader.add_constructor(  # type: ignore
        None,
        placeholder_constructor  # TODO: Maybe Add TokenBundle Wrapper
        # SafeConstructor.construct_undefined)
    )

    return yaml.load(stream, OrderedLoader)
