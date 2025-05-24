// This file contains the main brains of the calculator. It handles building
// all of the information about which items are needed to be crafted via their
// specified recipes.
import { ResourceEdge } from "./resource_edge";
import { inventory_label_suffix } from "./strings";
import { generate_instructions } from "./text_instructions";
import { generate_chart } from "./chart";
import { get_recipe } from "./recipe_info";

////////////////////////////////////////////////////////////////////////////////
// negative_requirements_exist
//
// A helper function to check all of the nodes that have been touched to see if
// any of them still have a negative quantity required. This means that we need
// to do more calculations still before the resource graph is complete.
////////////////////////////////////////////////////////////////////////////////
function negative_requirements_exist(requirements: { [key: string]: number }): boolean {
    for (let requirement in requirements){
        if (requirements[requirement] < 0) {
            return true;
        }
    }
    return false;
}


////////////////////////////////////////////////////////////////////////////////
// generatelist
//
// The primary function which handles all of the calculations needed to process
// the resource requirements and build the graph of conversion steps.
////////////////////////////////////////////////////////////////////////////////
export function generatelist(inventory: { [key: string]: number}) {
    var original_requirements: { [key: string]: number } = gather_requirements();
    var requirements: { [key: string]: number } = JSON.parse(JSON.stringify(original_requirements));
    var resource_tracker: { [key: string]: ResourceEdge } = {};
    var generation_totals: { [key: string]: number} = {}; // the total number of each resource produce (ignoring any consumption)

    var remaining_inventory_items = JSON.parse(JSON.stringify(inventory));
    var used_from_inventory: { [key: string]: number } = {};

    var raw_resources: { [key: string]: number } = {};

    // While we still have something that requires another resource to create
    while(negative_requirements_exist(requirements)) {

        // We create a copy of requirements so that the original can stay
        // unmodified while iterating over it in the for loop
        var output_requirements = JSON.parse(JSON.stringify(requirements));

        // For each negative requirement get it's base resources
        for (let requirement in requirements){
            if (requirements[requirement] < 0) {
                let recipe = get_recipe(requirement);
                let recipe_requirements = recipe.requirements;
                let recipe_output = recipe.output;

                if (remaining_inventory_items[requirement] > 0) {
                    let owned = remaining_inventory_items[requirement];
                    let needed = Math.abs(requirements[requirement]);
                    let recipes_from_owned = Math.floor(owned / recipe_output);
                    let overshot_from_owned = owned % recipe_output;
                    let extra_from_produce = needed % recipe_output;

                    if (overshot_from_owned < extra_from_produce) {
                        if (recipes_from_owned > 0) {
                            recipes_from_owned--;
                        }
                        else {
                            extra_from_produce = 0;
                        }
                    }

                    // Only take so much from inventory, that no [Extra] will be crafted.
                    let usable_count =  Math.min(needed, extra_from_produce + recipes_from_owned * recipe_output);

                    remaining_inventory_items[requirement] -= usable_count;
                    output_requirements[requirement] += usable_count;
                    requirements[requirement] += usable_count;

                    if (used_from_inventory[requirement] === undefined) {
                        used_from_inventory[requirement] = 0;
                    }

                    used_from_inventory[requirement] += usable_count;

                    let tracker_key: string = requirement + requirement + inventory_label_suffix;
                    if (!(tracker_key in resource_tracker)) {
                        resource_tracker[tracker_key] = new ResourceEdge(
                            requirement + inventory_label_suffix,
                            requirement,
                            0,
                        );
                    }

                    resource_tracker[tracker_key].value += usable_count;

                    let inventory_key = requirement + inventory_label_suffix;
                    if (!(inventory_key in generation_totals)) {
                        generation_totals[inventory_key] = 0;
                    }

                    generation_totals[inventory_key] += usable_count;

                    // console.log("using " + usable_count + " " + requirement + " from inventory.");
                }

                let required_count = -requirements[requirement];
                // Figure out the minimum number of a given requirement can be produced
                // to fit the quantity of that requirement needed.
                // EG: if a recipe produces 4 of an item but you only need 3
                //     then you must produce 4 of that item with 1 left over
                let produce_count = Math.ceil(required_count / recipe_output);
                output_requirements[requirement] += produce_count * recipe_output;

                // Add the quantity of the item created to the generation_totals
                // This is used to keep track of how many of any item in the crafting process are produced
                if (!(requirement in generation_totals)) {
                    generation_totals[requirement] = 0;
                }

                generation_totals[requirement] += produce_count * recipe_output;

                // if this is a raw resource then add it to the raw resource list
                if (recipe_requirements[requirement] === 0 && Object.keys(recipe_requirements).length === 1) {
                    if (raw_resources[requirement] === undefined) {
                        raw_resources[requirement] = 0;
                    }

                    raw_resources[requirement] += produce_count * recipe_output;
                }

                // If this is not a raw resource, track the change the and modify the output requirements
                else {
                    for (let item of Object.keys(recipe_requirements)) {

                        // Set the recipe requirements as new output requirements
                        if (output_requirements[item] === undefined) {
                            output_requirements[item] = 0;
                        }
                        output_requirements[item] -= recipe_requirements[item] * produce_count;

                        // Add the recipe's conversion
                        let tracker_key = requirement+item;
                        if (!(tracker_key in resource_tracker)) {
                            resource_tracker[tracker_key] = new ResourceEdge(
                                item,
                                requirement,
                                0,
                            );
                        }
                        resource_tracker[tracker_key].value += recipe_requirements[item] * produce_count;
                    };
                }
            }
        }
        requirements = output_requirements;
    }

    // console.log("Used from inventory:", used_from_inventory);

    for (let original_requirement in original_requirements) {
        // console.log(get_recipe(original_requirement));
        if (get_recipe(original_requirement).recipe_type === "Raw Resource") {
            resource_tracker[original_requirement + "final"] = new ResourceEdge(
                original_requirement,
                "[Final] " + original_requirement,
                -original_requirements[original_requirement],
            );
        }
    }

    // This maps all extra items to an extra value
    // It is done in order to get the right heights for items that produce more then they take
    // TODO, it might be nice to have a special path instead of a node to represent "extra"
    for (let key in output_requirements) {
        if (output_requirements[key] > 0) {
            var tracker_key = key+"extra";
            resource_tracker[tracker_key] = new ResourceEdge(
                key,
                "[Extra] " + key,
                output_requirements[key],
            );
            // Store the number of extra values for hover text on the chart
            generation_totals["[Extra] " + key] = output_requirements[key];
        }
    }

    // Make a copy of the resource_tracker to prevent updates while iterating
    var resource_tracker_copy = JSON.parse(JSON.stringify(resource_tracker));

    // Find any final resource that also feed into another resource and have it
    // feed into an extra node. This prevents final resource from not appearing
    // in the right hand column of the chart
    for (let tracked_resource in resource_tracker_copy) {
        var source = resource_tracker_copy[tracked_resource].source;
        if (source in original_requirements) {

            var final_tracker = source + "final";
            resource_tracker[final_tracker] = new ResourceEdge(
                source,
                "[Final] " + source,
                -original_requirements[source],
            );

            // Add in value of the non-extra resource
            generation_totals["[Final] " + source] = -original_requirements[source];
        }
    }

    for (let tracked_resource in resource_tracker) {
        if (resource_tracker[tracked_resource].value === 0) {
            delete resource_tracker[tracked_resource];
        }
    }

    generate_chart(resource_tracker, generation_totals, used_from_inventory);
    generate_instructions(resource_tracker, generation_totals);
}

////////////////////////////////////////////////////////////////////////////////
// gather_requirements
//
// A helper function that parses the DOM in order to identify which items the
// user has specified a desire for. Then returns those items as a mapping of
// item name to negative quantity.
////////////////////////////////////////////////////////////////////////////////
function gather_requirements(): { [key: string]: number } {
    var resources: { [key: string]:number } = {};

    document.querySelectorAll(".desired_item").forEach((elem) => {
        let key: string = elem.querySelector("input")!.getAttribute("aria-label")!;
        let value: string = (<HTMLInputElement>elem.querySelector(".desired_item_count")).value;

        let numeric_value = parseInt(value);
        if (!isNaN(numeric_value)) {
            // Set the value as negative to indicate they are needed
            resources[key] = -numeric_value;
        }
    });

    return resources;
}
