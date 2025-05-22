declare var recipe_json: {[key: string]: {output: number, recipe_type: string, requirements: {[key:string]:number}}[]};

////////////////////////////////////////////////////////////////////////////////
///////////////// Selection and modification of raw resources //////////////////
////////////////////////////////////////////////////////////////////////////////

let alternate_recipe_selections: { [key: string]: number} = {};

////////////////////////////////////////////////////////////////////////////////
// set_recipe_index
//
// Sets which recipe should be used by a resource using the resource name and
// the index of the recipe in the list of all recipes for that resource.
////////////////////////////////////////////////////////////////////////////////
export function set_recipe_index(node_name: string, recipe_index: number) {
	alternate_recipe_selections[node_name] = recipe_index;
	if (recipe_index === 0) {
		delete alternate_recipe_selections[node_name];
	}
}

////////////////////////////////////////////////////////////////////////////////
// get_recipe_index
//
// Gets which recipe index is current supposed to be used for a given resource
////////////////////////////////////////////////////////////////////////////////
function get_recipe_index(node_name: string) {
	if (!(node_name in alternate_recipe_selections)) {
		return 0;
	}
	else {
		return alternate_recipe_selections[node_name];
	}
}

////////////////////////////////////////////////////////////////////////////////
// set_recipe_to_raw
//
// Sets the recipe for the given resource to be whatever index the default
// "Raw Resource" recipe is set to.
////////////////////////////////////////////////////////////////////////////////
function set_recipe_to_raw(resource_name: string) {
	for (let i = 0; i < recipe_json[resource_name].length; i++){
		if (recipe_json[resource_name][i].recipe_type === "Raw Resource"){
			set_recipe_index(resource_name, i);
			return;
		}
	}
	alert("ERROR: Failed to set raw resource for " + resource_name);
}

////////////////////////////////////////////////////////////////////////////////
// get_recipe
//
// Get the recipe data that the given resource is supposed to use.
////////////////////////////////////////////////////////////////////////////////
export function get_recipe(resource_name: string) {
	return recipe_json[resource_name][get_recipe_index(resource_name)];
}

////////////////////////////////////////////////////////////////////////////////
// find_loop_from_node
//
// Find every loop in the recipe list that has this item in it.
////////////////////////////////////////////////////////////////////////////////
export function find_loop_from_node(start_node: string) {
	// Build simple directed graph of nodes and edges
	var directed_graph: {[key: string]: string[]} = {};
	for (let node in recipe_json) {
		directed_graph[node] = [];
		for (let edge in get_recipe(node).requirements) {
			if (-get_recipe(node).requirements[edge] > 0) {
				directed_graph[node].push(edge);
			}
		}
	}

	//Depth First search
	var recipe_changes = depth_first_search(directed_graph, start_node, start_node);

	for (let i in recipe_changes){
		// Convert to source recipe
		set_recipe_to_raw(recipe_changes[i]);
		console.warn("Changing", recipe_changes[i], "to raw resource to avoid infinite loop");
	}
}

////////////////////////////////////////////////////////////////////////////////
// depth_first_search
//
// Searches through the directed_graph starting at the start_node until it
// finds the end_node and returns all of the nodes that point to the end_node.
////////////////////////////////////////////////////////////////////////////////
function depth_first_search(
	directed_graph:{[key: string]: string[]},
	start_node: string,
	end_node: string
): string[] {
	let changes: string[] = [];

	// Loop through each of the recipe requirements
	for (let i in directed_graph[start_node]) {
		// if a requirement is the original node then change this item to a source and report back
		if (directed_graph[start_node][i] === end_node) {
			// Return this node name as changed
			return [start_node];
		}
		else {
			// Run the depth first search on the requirement and add any changes to the list of changes
			changes = changes.concat(depth_first_search(
				directed_graph,
				directed_graph[start_node][i],
				end_node
			));
		}
	}
	return changes;
}

// Javascript modules lack any method for tests to bypass the module's
// encapsulation so internal only functions have to have this big hack to make
// them accessible to the test scripts.
export const __internal__ = {
	depth_first_search,
	set_recipe_to_raw,
	get_recipe_index,
};
