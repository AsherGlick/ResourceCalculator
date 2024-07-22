declare var recipe_json: {[key: string]: {output: number, recipe_type: string, requirements: {[key:string]:number}}[]};

////////////////////////////////////////////////////////////////////////
/////////////////////// Selection and modification of raw resources/////
////////////////////////////////////////////////////////////////////////

var alternate_recipe_selections: { [key: string]: number}  = {};

export function set_recipe_index(node_name: string, recipe_index: number) {
	alternate_recipe_selections[node_name] = recipe_index;
	if (recipe_index === 0) {
		delete alternate_recipe_selections[node_name];
	}
}

function get_recipe_index(node_name: string) {
	if (!(node_name in alternate_recipe_selections)) {
		return 0;
	}
	else {
		return alternate_recipe_selections[node_name];
	}
}
function set_recipe_to_raw(node_name: string) {

	for (let i = 0; i < recipe_json[node_name].length; i++){
		if (recipe_json[node_name][i].recipe_type === "Raw Resource"){
			set_recipe_index(node_name, i);
			return;
		}
	}
	alert("ERROR: Failed to set raw resource for " + node_name);
}



export function get_recipe(node_name: string) {
	return recipe_json[node_name][get_recipe_index(node_name)];
}

export function find_loop_from_node(start_node: string) {
	// Generate Light Node Mapping
	var nodes: {[key: string]: string[]} = {};
	for (let node in recipe_json)  {
		// Add all the edges
		nodes[node] = [];
		for (let edge in get_recipe(node).requirements) {
			if (-get_recipe(node).requirements[edge] > 0) {
				nodes[node].push(edge);
			}
		}
	}

	//Depth First search
	var recipe_changes = depth_first_search(nodes, start_node, start_node);


	for (let i in recipe_changes){
		console.warn("Changing", recipe_changes[i], "to raw resource to avoid infinite loop");
	}
}


/******************************************************************************\
| depth_first_search                                                           |
|                                                                              |
| Arguments
| nodes - a list of nodes each with a list of directed edges representing their requirements
| {
| 	node1: [node2, node3, node4],
| 	node2: []
| 	node3: [node3, node4]
| 	node4: [node1]
| }
| node - which node to search from (used for recursion)
| match - which node, if found, would indicate a loop
\******************************************************************************/
function depth_first_search(nodes:{[key: string]: string[]} , node: string, match: string): string[] {
	let changes: string[] = [];

	// loop through recipe requirements
	for (let i in nodes[node]) {
		// if a requirement is the original node then change this item to a source and report back
		if (nodes[node][i] === match) {
			// Convert to source recipe
			set_recipe_to_raw(node);
			// Return this node name as changed
			return [node];
		}
		else {
			// Run the depth first search on the requirement and add any changes to the list of changes
			changes = changes.concat(depth_first_search(nodes, nodes[node][i], match));
		}
	}
	return changes;
}
