from typing import Dict, List, TypedDict
import zipfile
import json
from io import BytesIO
import os


MINECRAFT_BLOCK_TAG_DIRECTORY = "data/minecraft/tags/block"
MINECRAFT_ITEM_TAG_DIRECTORY = "data/minecraft/tags/item"

class ResourceGroup(TypedDict):
    machine_name: str # MCTag
    human_name: str # Display Name
    resources: List[str] # Resource MCTags


class ResourceGroups():
    resource_groups: List[ResourceGroup]
    automatic_resource_groups: Dict[str, List[str]]

    def __init__(self, jarfile: zipfile.ZipFile, id_to_name_map: Dict[str, str]):

        self.load_automatic_resource_groups(jarfile)

        self.resource_groups = [
            # Auto resource groups, groups that are parsed automatically from minecraft data
            self.auto_resource_group("minecraft:planks", "Any Planks"),
            self.auto_resource_group("minecraft:wooden_slabs", "Any Slab"),
            self.auto_resource_group("minecraft:logs", "Any Log"),
            self.auto_resource_group("minecraft:stone_crafting_materials", "Any Stone"),
            self.auto_resource_group("minecraft:sand", "Any Sand"),
            self.auto_resource_group("minecraft:logs_that_burn", "Any Log That Burns"),
            self.auto_resource_group("minecraft:acacia_logs", "Any Acacia Log"),
            self.auto_resource_group("minecraft:birch_logs", "Any Birch Log"),
            self.auto_resource_group("minecraft:crimson_stems", "Any Crimson Stem"),
            self.auto_resource_group("minecraft:dark_oak_logs", "Any Dark Oak Log"),
            self.auto_resource_group("minecraft:oak_logs", "Any Oak Log"),
            self.auto_resource_group("minecraft:jungle_logs", "Any Jungle Log"),
            self.auto_resource_group("minecraft:mangrove_logs", "Any Mangrove Log"),
            self.auto_resource_group("minecraft:spruce_logs", "Any Spruce Log"),
            self.auto_resource_group("minecraft:warped_stems", "Any Warped Stem"),
            self.auto_resource_group("minecraft:coals", "Any Coal"),
            self.auto_resource_group("minecraft:wool", "Any Wool"),
            self.auto_resource_group("minecraft:soul_fire_base_blocks", "Any Soul Fire Base Block"),
            self.auto_resource_group("minecraft:stone_tool_materials", "Any Stone Tool Material"),
            self.auto_resource_group("minecraft:shulker_boxes", "Any Shulker Box"),
            self.auto_resource_group("minecraft:bamboo_blocks", "Any Bamboo Block"),
            self.auto_resource_group("minecraft:cherry_logs", "Any Cherry Log"),
            self.auto_resource_group("minecraft:beds", "Any Bed"),
            self.auto_resource_group("minecraft:wool_carpets", "Any Carpet"),
            self.auto_resource_group("minecraft:smelts_to_glass", "Any Sand"),

            # Non-Auto, these are groups that are defined inside the resource recipes but have no formal grouping
            {
                "machine_name": "resourcecalculator:yellow_sandstone",
                "human_name": "Any Yellow Sandstone",
                "resources": [
                    'minecraft:chiseled_sandstone',
                    'minecraft:cut_sandstone',
                    'minecraft:sandstone',
                ],
            }, {
                "machine_name": "resourcecalculator:uncut_yellow_sandstone",
                "human_name": "Any Uncut Yellow Sandstone",
                "resources": [
                    'minecraft:chiseled_sandstone',
                    'minecraft:sandstone',
                ],
            }, {
                "machine_name": "resourcecalculator:red_sandstone",
                "human_name": "Any Red Sandstone",
                "resources": [
                    'minecraft:chiseled_red_sandstone',
                    'minecraft:cut_red_sandstone',
                    'minecraft:red_sandstone',
                ],
            }, {
                "machine_name": "resourcecalculator:uncut_red_sandstone",
                "human_name": "Any Uncut Red Sandstone",
                "resources": [
                    'minecraft:chiseled_red_sandstone',
                    'minecraft:red_sandstone',
                ],
            }, {
                "machine_name": "resourcecalculator:unsmooth_quartz_block",
                "human_name": "Any Unsmooth Quartz Block",
                "resources": [
                    'minecraft:chiseled_quartz_block',
                    'minecraft:quartz_block',
                    'minecraft:quartz_pillar',
                ],
            }, {
                "machine_name": "resourcecalculator:purpur_block",
                "human_name": "Any Purpur Block",
                "resources": [
                    'minecraft:purpur_block',
                    'minecraft:purpur_pillar',
                ],
            },
        ]

        self.resource_groups += self.derive_resource_group_except_one("minecraft:beds", id_to_name_map)
        self.resource_groups += self.derive_resource_group_except_one("minecraft:wool", id_to_name_map)
        self.resource_groups += self.derive_resource_group_except_one("minecraft:wool_carpets", id_to_name_map)



    ############################################################################
    # load_automatic_resource_groups
    ############################################################################
    def load_automatic_resource_groups(self, jarfile: zipfile.ZipFile):
        all_tags: Dict[str, List[str]] = {}

        file_list = jarfile.infolist()
        for file in file_list:
            filename = file.filename

            if filename.startswith(MINECRAFT_BLOCK_TAG_DIRECTORY) or filename.startswith(MINECRAFT_ITEM_TAG_DIRECTORY):
                key = os.path.splitext(os.path.basename(filename))[0]
                all_tags["minecraft:"+key] = sorted(list(set(parse_tagfile(jarfile, filename))))

        self.automatic_resource_groups = all_tags


    def auto_resource_group(self, machine_name: str, human_name: str) -> ResourceGroup:

        if machine_name not in self.automatic_resource_groups:
            raise ValueError("{} not found, only auto resources available are {}".format(machine_name, str(self.automatic_resource_groups.keys())))

        return {
            "machine_name": machine_name,
            "human_name": human_name,
            "resources": self.automatic_resource_groups[machine_name]
        }


    def derive_resource_group_except_one(
        self,
        original_machine_name: str,
        id_to_name_map: Dict[str, str],
    ) -> List[ResourceGroup]:
        original_resources = self.get_resouces_from_group(original_machine_name)
        original_display_name = self.get_display_name_from_group(original_machine_name)

        new_resource_groups = []

        for removed_resource in original_resources:
            new_resource_groups.append({
                "machine_name": "resourcecalculator:" + original_machine_name + "_except_" + removed_resource,
                "human_name": original_display_name + " Except " + id_to_name_map[removed_resource],
                "resources": [x for x in original_resources if x != removed_resource]
            })

        return new_resource_groups







    # From a group name get the list of resources
    def get_resouces_from_group(self, group: str) -> List[str]:
        for resource_group in self.resource_groups:
            if resource_group["machine_name"] == group:
                return resource_group["resources"]

        raise ValueError("\n".join([
            "No resource group with the name {} found.",
            "If this is a new resource group you may need to add it to `ResourceGroups.resource_groups` manually",
        ]).format(group))

    # From a list of resources figure out what group it is a part of
    def get_group_from_resources(self, resources: List[str]) -> str:
        for resource_group in self.resource_groups:
            if resource_group["resources"] == resources:
                return resource_group["machine_name"]
        raise ValueError("\n".join([
            "No resource group with the resources {} was found.",
            "If this is a new resource group you may need to add it to `ResourceGroups.resource_groups` manually",
        ]).format(resources))


    def get_display_name_from_group(self, group: str) -> str:
        for resource_group in self.resource_groups:
            if resource_group["machine_name"] == group:
                return resource_group["human_name"]

        raise ValueError("\n".join([
            "No resource group with the name {} found.",
            "If this is a new resource group you may need to add it to `ResourceGroups.resource_groups` manually",
        ]).format(group))

    def is_display_name_a_group(self, display_name: str) -> bool:
        for resource_group in self.resource_groups:
            if resource_group["human_name"] == display_name:
                return True
        return False

    def get_group_from_display_name(self, display_name: str) -> str:
        for resource_group in self.resource_groups:
            if resource_group["human_name"] == display_name:
                return resource_group["machine_name"]

        raise ValueError("\n".join([
            "No resource group with the name {} found.",
            "If this is a new resource group you may need to add it to `ResourceGroups.resource_groups` manually",
        ]).format(display_name))




################################################################################
# Parse a given tag file. Tag files contain the equivlent of requirement groups
# and may be nested to contain other tagfiles. If a file contains another nested
# file then recursively open that file and add its contents to this tag.
################################################################################
def parse_tagfile(jarfile: zipfile.ZipFile, tag_filename: str) -> List[str]:
    tags: List[str] = []

    files = set([x.filename for x in jarfile.infolist()])

    tagfile_data = json.load(BytesIO(jarfile.read(tag_filename)))

    assert(len(tagfile_data) == 1)
    assert("values" in tagfile_data)
    assert(type(tagfile_data["values"] == list))

    for tag in tagfile_data["values"]:
        assert(type(tag) == str)

        if tag.startswith("#"):
            blocksfile = os.path.join(MINECRAFT_BLOCK_TAG_DIRECTORY, tag[11:] + ".json")
            itemsfile = os.path.join(MINECRAFT_ITEM_TAG_DIRECTORY, tag[11:] + ".json")

            if blocksfile in files:
                tags += parse_tagfile(jarfile, blocksfile)
            elif itemsfile in files:
                tags += parse_tagfile(jarfile, itemsfile)

        else:
            tags.append(tag)

    return tags

