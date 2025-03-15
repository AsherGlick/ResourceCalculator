import { ResourceEdge } from "./resource_edge";
import { get_node_columns } from "./node_columns";
import { get_recipe, set_recipe_index, find_loop_from_node } from "./recipe_info";
import { inventory_label_suffix } from "./strings";
import { generate_instructions } from "./text_instructions";

declare var resource_simple_names: {[key: string]: string};
declare var recipe_json: {[key: string]: {output: number, recipe_type: string, requirements: {[key:string]:number}}[]};


////////////////////////////////////////////////////////////////////////////////
// calculator.js handles all of the javascript for the calculator page
////////////////////////////////////////////////////////////////////////////////

/// DOM Gathering ///
const inventory_import_text_elem = <HTMLInputElement>document.getElementById("inventory_import_text");
const hover_name_elem: HTMLElement = document.getElementById("hover_name")!;
const reset_item_count_elem: HTMLElement = document.getElementById("reset_item_count")!;
const hide_unused_checkbox_elem: HTMLInputElement = <HTMLInputElement>document.getElementById("unused_hide_checkbox");
const hide_unused_checkbox_label_elem: HTMLElement = document.getElementById("unused_hide_checkbox_label")!;
const recipe_selector_list_elem = document.getElementById("recipe_selector_list")!;
const recipe_select_elem = document.getElementById("recipe_select")!;
const inventory_amount_input_elem = <HTMLInputElement>document.getElementById("inventory_amount_input");

////////////////////////////////////////////////////////////////////////////////
////////////////////////////// Header Bar Logics ///////////////////////////////
////////////////////////////////////////////////////////////////////////////////

/******************************************************************************\
| "Reset Item Counts" Button Logic                                             |
\******************************************************************************/
function clear_item_counts() {
	if (!confirm("Are you sure you want to clear all items?")) {
		return;
	}

	document.querySelectorAll(".desired_item").forEach((desired_item) => {
		const field = <HTMLInputElement>desired_item.querySelector(".desired_item_count");
		field.value = "";
		set_textbox_background(field);
	});

	// uncheck the hide unused checkbox element
	if (hide_unused_checkbox_elem.checked) {
		hide_unused_checkbox_elem.click();
	}

	generatelist();
}

reset_item_count_elem.addEventListener("click", clear_item_counts);
inventory_import_text_elem.addEventListener("change", clear_item_counts);

/******************************************************************************\
| "About Us" Button Logic                                                      |
\******************************************************************************/
// $(".inventory_import_export_toggle").click(function() {
// 	$("#inventory_import_export").slideToggle();
// }); // TODO: Re enable when desired

// $("#about_button").click(function() {
// 	$("#about_us").slideToggle();
// }); // TODO: Re enable when desired

// TODO: We should not need to regenerate the calculator every time a stack size
// button is clicked. This is especially visible if the calculator has not yet
// been generated.
document.querySelectorAll("input[name=unit_name]").forEach(function(stack_size_button) {
	stack_size_button.addEventListener("click", function() {
		generatelist();
	});
});

// Bind events to the item list elements // TODO THIS FUNCTION NEEDS A BETTER COMMENT
function initilize_all_items() {
	document.querySelectorAll(".desired_item").forEach((item) => {
		let item_input_box = <HTMLInputElement>item.querySelector(".desired_item_count");
		let item_label = item_input_box.getAttribute("aria-label")!;

		// When clicking on the box focus the text box
		item.addEventListener("click", function() {
			item_input_box.style.display = "block";
			console.log("showing item");
			item_input_box.focus();
		});

		// Make the item counts save when modified
		item_input_box.addEventListener("propertychange", save);
		item_input_box.addEventListener("change", save);
		item_input_box.addEventListener("click", save);
		item_input_box.addEventListener("keyup", save);
		item_input_box.addEventListener("input", save);
		item_input_box.addEventListener("paste", save);

		// Put an orange border around the item when the text box is focused
		// This makes it more noticeable when an item is selected
		item_input_box.addEventListener("focus", function() {
			item.classList.add("desired_item_input_focused");
			item_input_box.style.backgroundColor = "rgba(0,0,0,.5)";
			item_input_box.select();
		});
		item_input_box.addEventListener("blur", function() {
			item.classList.remove("desired_item_input_focused");
			set_textbox_background(item_input_box);

		});

		// When doubleclicking open the recipe select menu
		item.addEventListener("dblclick", function (event) {
			switch_recipe(item_label, <MouseEvent>event);
			switch_inventory_amount_input(item_label);
		});

		// Enable item name hover text
		item.addEventListener("mouseover", function() {
			hover_name_elem.textContent = item_label;
			hover_name_elem.style.opacity = "1";
		});
		item.addEventListener("mouseout", function() {
			hover_name_elem.style.opacity = "0";
		});
	});
}
initilize_all_items();


/******************************************************************************\
| Search Bar filter logic
\******************************************************************************/
function filter_items() {
	let search_string = item_filter_elem.value.toLowerCase();;
	let hide_unused = hide_unused_checkbox_elem.checked;

	// Loop through each item
	document.querySelectorAll(".desired_item").forEach(function(item) {
		let item_name = item.querySelector("input")!.getAttribute("aria-label")!.toLowerCase();
		let item_count: number = parseInt((<HTMLInputElement>item.querySelector(".desired_item_count")).value);

		// If the search string does not match hide the item
		// If the item count is not greater than 0 and hide unused is true hide
		if (item_name.indexOf(search_string) === -1 || !(item_count > 0 || !hide_unused)) {
			(<HTMLInputElement>item).style.display = "none";
		}
		else {
			(<HTMLInputElement>item).style.display = "block";
		}
	});
}



let item_filter_elem: HTMLInputElement = <HTMLInputElement>document.getElementById("item_filter");
item_filter_elem.addEventListener("change", filter_items);
item_filter_elem.addEventListener("click", filter_items);
item_filter_elem.addEventListener("keyup", filter_items);
item_filter_elem.addEventListener("input", filter_items);
item_filter_elem.addEventListener("paste", filter_items);


/******************************************************************************\
| "Hide Unused" "Show Unused" Button Logic                                     |
\******************************************************************************/
hide_unused_checkbox_elem.addEventListener("change", function() {
	if (this.checked) {
		hide_unused_checkbox_label_elem.textContent = "Show Unused";
	}
	else {
		hide_unused_checkbox_label_elem.textContent = "Hide Unused";
	}
	filter_items();
});


////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////// // TODO THIS FUNCTION NEEDS A BETTER PLACE TO LIVE
////////////////////////////////////////////////////////////////////////////////
function filenameify(rawname: string): string {
	if (rawname === null) {
		return "";
	}
	return rawname.toLowerCase().replace(/[^a-z0=9]/g, "");
}


////////////////////////////////////////////////////////////////////////////////
//////////////////////////////// Save and Load /////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

/******************************************************************************\
| save()                                                                       |
|                                                                              |
| This function saves the current state of the resource requirement list to    |
| the URI hash so that it can be shared with other users or so the page can be |
| refreshed without losing current information.                                |
\******************************************************************************/
function save() {
	let selected_items: {[key: string]: number} = {};

	document.querySelectorAll(".desired_item").forEach(function(item) {
		let key: string = item.querySelector(".desired_item_count")!.id;
		let value: string = (<HTMLInputElement>item.querySelector(".desired_item_count")).value;

		let int_value: number = parseInt(value);
		if (!isNaN(int_value)) {
			selected_items[key] = int_value;
		}
	});
	// TODO: We probably want to do something here with replace state instead of
	// push state if possible.
	if(history.pushState) {
		history.pushState(null, "", "#" + to_url_params(selected_items));
	}
	else {
		window.location.hash = to_url_params(selected_items);
	}

	export_inventory_to_localstorage();
}

function to_url_params(source: {[key: string]: number}): string {
	let array = [];

	for (let key in source) {
		array.push(encodeURIComponent(key) + "=" + encodeURIComponent(source[key]));
	}

	return array.join("&");
}



let inventory: { [key: string]: number} = {};
function export_inventory_to_localstorage() {
	let input = inventory;

	input = remove_null_entries(input);

	input = input ? input : {};
	let calculatorName = window.location.pathname.replace(/\//g, "");

	localStorage.setItem("[" + calculatorName + " Inventory]", JSON.stringify(input));
}

function export_inventory_to_textbox() {
	inventory = remove_null_entries(inventory);
	(<HTMLInputElement>document.getElementById("inventory_import_text")).value = JSON.stringify(inventory ? inventory : {}, null, 1);
}


/******************************************************************************\
| load()                                                                       |
|                                                                              |
| This function is an inverse to save() and reads the state of the resource    |
| requirement list from the URI hash. In addition it will automatically call   |
| generatelist() to save the user from having to click the button for a saved  |
| list.                                                                        |
\******************************************************************************/
function load() {
	import_inventory_from_localstorage();
	export_inventory_to_textbox();

	var uri_arguments = decodeURIComponent(window.location.hash.substr(1));
	if (uri_arguments !== "") {
		var pairs = uri_arguments.split("&");
		for(let i in pairs){
			var split = pairs[i].split("=");
			var id = decodeURIComponent(split[0]);
			var value = decodeURIComponent(split[1]);
			let desired_item = <HTMLInputElement>document.getElementById(id);
			desired_item.value = value;
			desired_item.style.display = "block";
			set_textbox_background(desired_item);
		}
		// check the hide unused checkbox
		if (!hide_unused_checkbox_elem.checked) {
			hide_unused_checkbox_elem.click();
		}
		generatelist();
	}
}

function import_inventory_from_localstorage() {
	let calculatorName = window.location.pathname.replace(/\//g, "");
	let inventoryContent = JSON.parse(localStorage.getItem("[" + calculatorName + " Inventory]") || "{}");
	inventory = remove_null_entries(inventory);
	export_inventory_to_textbox();
	return inventory;
}


const inventory_import_error_elem = document.getElementById("inventory_import_error")!;

function import_inventory_from_textbox(){
	let text: string = inventory_import_text_elem.value;
	if (text.trim().length > 0){
		try {
			inventory = JSON.parse(text);
			inventory_import_error_elem.classList.add("hidden");
		}
		catch (exception) {
			inventory_import_error_elem.classList.remove("hidden");
		}
	}
	else {
		inventory = {};
		inventory_import_error_elem.classList.add("hidden");
	}

	inventory = remove_null_entries(inventory);
	export_inventory_to_localstorage();
}



function remove_null_entries<T>(item_collection: {[key: string]:T}): {[key: string]:T}{
	for (let item_name in item_collection) {
		if (!item_collection[item_name]){
			delete item_collection[item_name];
		}
	}
	return item_collection;
}

////////////////////////////////////////////////////////////////////////////////
///////////////////////// Requirements Calculation Logic ///////////////////////
////////////////////////////////////////////////////////////////////////////////
const generate_list_button_elem = document.getElementById("generatelist")!;
generate_list_button_elem.addEventListener("click", generatelist);




function negative_requirements_exist(requirements: { [key: string]: number }): boolean {
	for (let requirement in requirements){
		if (requirements[requirement] < 0) {
			return true;
		}
	}
	return false;
}



function generatelist() {
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
						output_requirements[item] += recipe_requirements[item] * produce_count;

						// Add the recipe's conversion
						let tracker_key = requirement+item;
						if (!(tracker_key in resource_tracker)) {
							resource_tracker[tracker_key] = new ResourceEdge(
								item,
								requirement,
								0,
							);
						}
						resource_tracker[tracker_key].value += recipe_requirements[item] * -produce_count;
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

/******************************************************************************\
|
\******************************************************************************/
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


function get_columns(edges: { [key: string]: ResourceEdge }): string[][] {
	let node_columns: { [key: string]: number } = get_node_columns(edges);

	// determine how many columns there should be
	let column_count = 0;
	for (let node in node_columns) {
		if (node_columns[node] + 1 > column_count) {
			column_count = node_columns[node] + 1;
		}
	}

	// Create an array of those columns
	let columns: string[][] = Array(column_count);
	for (let i = 0; i < column_count; i++){
		columns[i] = [];
	}

	for (let node in node_columns) {
		columns[node_columns[node]].push(node);
	}

	return columns;
}


////////////////////////////////////////////////////////////////////////////////
//////////////////////////////// Chart Creation ////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

class ResourceNode {
	public input: number = 0;
	public output: number = 0;
	public size: number = 0;
	public column: number = 0;
	public passthrough: boolean = false;
	public passthrough_node_index: number | null = null; // TODO: Confirm this is correct
	public incoming_edges: string[] = []; // List of edge key ids
	public outgoing_edges: string[] = []; // List of edge key ids

	public passthrough_edge_id: string = ""; // todo: figure out how this should be used

	// Size and positions
	public height: number = 0;
	public y: number = 0;

	node(input: number, output: number, size: number, column: number): ResourceNode {
		this.input = input;
		this.output = output;
		this.size = size;
		this.column = column;
		return this
	}

	passthrough_node(
		size: number,
		column: number,
		passthrough_node_index: number,
		passthrough_edge_id: string,
	): ResourceNode{
		this.size = size;
		this.column = column
		this.passthrough_node_index = passthrough_node_index;
		this.passthrough_edge_id = passthrough_edge_id;
		this.passthrough = true;
		return this;
	}
}

interface RectangleMargin {
	top: number,
	right: number,
	bottom: number,
	left: number,
}

/******************************************************************************\
| generate_chart                                                               |
|                                                                              |
| This function is in charge of drawing the sankey chart onto the canvas       |
|
| Arguments
|   generation_events -
\******************************************************************************/
function generate_chart(
	edges: { [key: string]: ResourceEdge },
	node_quantities: { [key: string]: number },
	used_from_inventory: { [key: string]: number },
) {

	if(Object.keys(node_quantities).length === 0) {
		console.log("Nothing to render");

		// clear cache
		cached_chart_data = undefined;
		relayout_chart();
		return;
	}

	// Set the margins for the area that the nodes and edges can take up
	var margin: RectangleMargin = {
		top: 10,
		right: 1,
		bottom: 10,
		left: 1,
	};

	// Reset the colors that have already been selected so we can get repeatable graphs
	color_lookup_cache = {};

	// Set the space between the bottom of one node and the top of the one below it to 10px
	var node_padding = 10;

	// Calculate the width and the height of the area that the nodes and edges can take up
	var height = 800 - margin.top - margin.bottom;

	// Get the matrix of nodes, sorted into an array of columns
	let columns: string[][] = get_columns(edges);

	// Create a representation of node objects
	var nodes: { [key: string]: ResourceNode} = {};
	for (let column_id in columns) {
		for (let node_id in columns[column_id]) {
			let node_name = columns[column_id][node_id];

			let input = get_input_size(edges, node_name);
			let output;
			if (node_quantities[node_name] !== undefined) {
				output = node_quantities[node_name];
			}
			else {
				output = 0;
			}

			if (used_from_inventory[node_name] !== undefined) {
				output += used_from_inventory[node_name];
			}

			let size = Math.max(output, input);

			nodes[node_name] = new ResourceNode().node(
				input,
				output,
				size,
				Number(column_id),
			);
		}
	}

	// Assign all edges to the nodes depending if the edge connects as a source
	// or as a target for the given node. Also cache which column the node is
	// in for the next step of finding edges that span multiple columns
	for (let edge_id in edges) {
		let edge = edges[edge_id];

		nodes[edge.target].incoming_edges.push(edge_id);
		nodes[edge.source].outgoing_edges.push(edge_id);
	}

	// Find edges that span multiple columns and create fake nodes for them in
	// the columns they pass over. This allows us to weight the edges so they
	// wont be overlapped by a node in that column
	for (let edge_id in edges){
		let edge = edges[edge_id];
		edge.passthrough_nodes = [];

		let source_column_index = nodes[edge.source].column;
		let target_column_index = nodes[edge.target].column;

		for (let passthrough_column_index = source_column_index+1; passthrough_column_index<target_column_index; passthrough_column_index+=1) {
			var passthrough_node_id: string = edge_id + "_" + passthrough_column_index;

			nodes[passthrough_node_id] = new ResourceNode().passthrough_node(
				edge.value,
				passthrough_column_index,
				edge.passthrough_nodes.length,
				edge_id,
			);

			edge.passthrough_nodes.push(passthrough_node_id);
			columns[passthrough_column_index].push(passthrough_node_id);
		}
	}

	// Calculate the scale of a single item based on the tallest column of items
	// such that that column fits within the allotted height of the chart
	var value_scale = 9999;
	for (let column in columns) {
		var height_for_values = height + node_padding;
		var values = 0;
		for (let node_index in columns[column]) {
			var node = nodes[columns[column][node_index]];
			height_for_values -= node_padding;
			values += node.size;
		}

		var column_scale = height_for_values / values;
		if (value_scale > column_scale) {
			value_scale = column_scale;
		}
	}

	// Calculate the positions of the nodes in each column based on the nodes
	// in other columns. We do 32 iterations of the internal process to achieve
	// very good positions
	set_node_positions(32, columns, nodes, edges, value_scale, node_padding, height);

	// Make the call to draw the chart itself now that numbers have been calculated
	layout_chart(columns, nodes, edges, height, value_scale, margin);
}


function set_node_positions(
	iterations: number,
	columns: string[][],
	nodes: {[key: string]: ResourceNode},
	edges: {[key: string]: ResourceEdge},
	value_scale: number,
	node_padding: number,
	svg_height: number,
) {
	// Calculate Node Heights and Positions
	for (let column_index in columns) {
		var running_y = 0;
		for (let node_index in columns[column_index]) {
			var node = nodes[columns[column_index][node_index]];
			node.height = node.size * value_scale;
			node.y = running_y;
			running_y += node.height + node_padding;
		}
	}

	// Run the relaxation algorithms forwards and backwards
	for (let alpha = 1; iterations > 0; --iterations) {
		relax_columns_right_to_left(alpha *= .99, columns, nodes, edges);
		relax_columns_left_to_right(alpha, columns, nodes, edges);
		resolve_node_collisions(columns, nodes, node_padding, svg_height);
	}
}

function relax_columns_left_to_right(
	alpha:number,
	columns: string[][],
	nodes: {[key: string]: ResourceNode},
	edges: {[key: string]: ResourceEdge},
) {
	function weighted_source_sum(node: ResourceNode): number {
		var sum = 0;
		if (node.passthrough_node_index === null) {
			for (let source_id in node.incoming_edges) {
				var edge = edges[node.incoming_edges[source_id]];

				var source_node = nodes[edge.source];
				if (edge.passthrough_nodes.length) {
					source_node = nodes[edge.passthrough_nodes[edge.passthrough_nodes.length-1]];
				}
				sum += y_midpoint(source_node) * edge.value;
			}
		}
		else {
			var passthrough_edge = edges[node.passthrough_edge_id];
			if (node.passthrough_node_index === 0) {
				sum = y_midpoint(nodes[passthrough_edge.source]) * passthrough_edge.value;
			}
			else {
				sum = y_midpoint(nodes[passthrough_edge.passthrough_nodes[node.passthrough_node_index-1]]) * passthrough_edge.value;
			}
		}
		return sum;
	}
	function raw_source_sum(node: ResourceNode): number {
		// If the node is not a passthrough then return the sum of all of
		// the source edges
		if (node.passthrough === false) {
			var sum = 0;
			for (let source_id in node.incoming_edges) {
				sum += edges[node.incoming_edges[source_id]].value;
			}
			return sum;
		}
		// If this is a passthrough node then both the target and source
		// edges will be the same size as the node
		else {
			return node.size;
		}
	}

	for (let column_index in columns) {
		if (Number(column_index) === 0) {
			continue;
		}
		for (let node_index in columns[column_index]) {
			var node = nodes[columns[column_index][node_index]];
			var y = weighted_source_sum(node) / raw_source_sum(node);
			node.y += (y - y_midpoint(node)) * alpha;
		}
	}

}
function relax_columns_right_to_left(
	alpha:number,
	columns: string[][],
	nodes: {[key: string]: ResourceNode},
	edges: {[key: string]: ResourceEdge},
) {
	function weighted_target_sum(node: ResourceNode): number {
		var sum = 0;
		if (node.passthrough_node_index === null) {
			for (let target_id in node.outgoing_edges) {
				var edge = edges[node.outgoing_edges[target_id]];

				var target_node = nodes[edge.target];
				if (edge.passthrough_nodes.length) {
					target_node = nodes[edge.passthrough_nodes[0]];
				}
				sum += y_midpoint(target_node) * edge.value;
			}
		}
		else {
			var passthrough_edge = edges[node.passthrough_edge_id];
			if (node.passthrough_node_index === passthrough_edge.passthrough_nodes.length-1) {
				sum = y_midpoint(nodes[passthrough_edge.target]) * passthrough_edge.value;
			}
			else {
				sum = y_midpoint(nodes[passthrough_edge.passthrough_nodes[node.passthrough_node_index+1]]) * passthrough_edge.value;
			}
		}
		return sum;
	}
	function raw_target_sum(node: ResourceNode): number {
		// If the node is not a passthrough then return the sum of all of
		// the source edges
		if (node.passthrough === false) {
			var sum = 0;
			for (let target_id in node.outgoing_edges) {
				sum += edges[node.outgoing_edges[target_id]].value;
			}
			return sum;
		}
		// If this is a passthrough node then both the target and source
		// edges will be the same size as the node
		else {
			return node.size;
		}
	}

	columns = columns.slice().reverse();
	for (let column_index in columns) {
		if (Number(column_index) === 0) {
			continue;
		}
		for (let node_index in columns[column_index]) {
			var node = nodes[columns[column_index][node_index]];
			var y = weighted_target_sum(node) / raw_target_sum(node);
			node.y += (y - y_midpoint(node)) * alpha;
		}
	}

}

function y_midpoint(node: ResourceNode): number {
	return node.y + node.height / 2;
}

function resolve_node_collisions(
	columns: string[][],
	nodes: {[key: string]: ResourceNode},
	node_padding: number,
	svg_height: number,
) {
	function y_comp(a: string, b: string) {
		return nodes[a].y - nodes[b].y;
	}

	// Sort all the nodes in the array based on their visual order
	for (let column_index in columns) {
		var column = columns[column_index];
		column.sort(y_comp);

		// If any node is overlapping the previous node push it downwards
		var bottom_of_previous_node = 0;
		for (let i = 0; i < column.length; i++) {
			let node = nodes[column[i]];

			// Check to see if there is an overlap and fix it if so
			let delta_y = bottom_of_previous_node - node.y;
			if (delta_y > 0) {
				node.y += delta_y;
			}

			// Set the bottom of this node to be the bottom of the previous node for the next cycle
			bottom_of_previous_node = node.y + node.height + node_padding;
		}

		// If any node is overlapping push it upwards
		// maybe this can include node padding as we dont need a padding on the bottom
		var top_of_previous_node = svg_height;
		for (let i = column.length-1; i >= 0; i--) {
			let node = nodes[column[i]];

			let delta_y = top_of_previous_node - (node.y + node.height);
			if (delta_y < 0) {
				node.y += delta_y;
			}

			top_of_previous_node = node.y - node_padding;
		}
	}
}


interface Color {
	r: number;
	b: number;
	g: number;
}

function hexToRgb(hex: string): Color {
	var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
	return result ? {
		r: parseInt(result[1], 16),
		g: parseInt(result[2], 16),
		b: parseInt(result[3], 16),
	} : {r: 0, b: 0, g:0};
}

function color_darken(color: Color): Color {
	var k = 0.49;

	return {
		r: Math.round(color.r * k),
		g: Math.round(color.g * k),
		b: Math.round(color.b * k),
	};
}

function color_string(color: Color): string{
	return "rgb("+color.r+","+color.g+","+color.b+")";
}


/******************************************************************************\
| get_color
|
| This function supplies a color for a node to use as it's fill color. The
| color is determined by the first word in the string, excluding a [Extra] or
| [Final] prefix. The first time that key is presented to the function a new
| color is chosen for that key, each subsequent call after the first  with the
| same key will return the same color but this is not necessarily the case for
| a new chart generation.
\******************************************************************************/
const all_colors = [
	hexToRgb("1f77b4"),
	hexToRgb("aec7e8"),
	hexToRgb("ff7f0e"),
	hexToRgb("ffbb78"),
	hexToRgb("2ca02c"),
	hexToRgb("98df8a"),
	hexToRgb("d62728"),
	hexToRgb("ff9896"),
	hexToRgb("9467bd"),
	hexToRgb("c5b0d5"),
	hexToRgb("8c564b"),
	hexToRgb("c49c94"),
	hexToRgb("e377c2"),
	hexToRgb("f7b6d2"),
	hexToRgb("bcbd22"),
	hexToRgb("dbdb8d"),
	hexToRgb("17becf"),
	hexToRgb("9edae5"),
	hexToRgb("7f7f7f"),
	hexToRgb("c7c7c7"),
];
let color_lookup_cache: { [key: string]:number } = {};
function get_color(key: string) {
	// Strip out Extra and Final prefixes
	key = key.replace(/^\[Extra\] /, "");
	key = key.replace(/^\[Final\] /, "");

	// Strip out everything past the first word
	key = key.replace(/ .*/, "");

	// Lookup or set the color that is attached to this key
	var index = color_lookup_cache[key];
	if (index === undefined) {
		index = Object.keys(color_lookup_cache).length % all_colors.length;
		color_lookup_cache[key] = index;
	}

	return all_colors[index];
}



/******************************************************************************\
| layout_chart
|
| draw the chart itself
\******************************************************************************/
class CachedChartData {
	columns: string[][] = [];
	nodes: { [key: string]: ResourceNode } = {};
	edges: { [key: string]: ResourceEdge } = {};
	height: number = 0;
	value_scale: number = 0;
	margin: RectangleMargin = {top: 0, right: 0, bottom: 0, left: 0};
}
let cached_chart_data: CachedChartData|undefined;
function layout_chart(
	columns: string[][],
	nodes: { [key: string]: ResourceNode },
	edges: { [key: string]: ResourceEdge } ,
	height: number,
	value_scale: number,
	margin: RectangleMargin
) {
	cached_chart_data = {
		columns: columns,
		nodes: nodes,
		edges: edges,
		height: height,
		value_scale: value_scale,
		margin: margin,
	};
	relayout_chart();
}
window.onresize = function() {
	relayout_chart();
};

const chart_elem: HTMLElement = document.getElementById("chart")!;
const content_elem: HTMLElement = document.getElementById("content")!;


function relayout_chart(){
	// Empty the chart immediately.
	while (chart_elem.lastChild) {
		chart_elem.removeChild(chart_elem.lastChild);
	}

	// If there is no chart to render, then stop early.
	if (cached_chart_data === undefined) {
		return;
	}

	let columns = cached_chart_data.columns;
	var nodes = cached_chart_data.nodes;
	var edges = cached_chart_data.edges;
	var height = cached_chart_data.height;
	var value_scale = cached_chart_data.value_scale;
	var margin = cached_chart_data.margin;


	var width = content_elem.offsetWidth - margin.left - margin.right;

	var node_width = 20;

	// Determine the space between the left hand side of each node column
	var node_spacing: number = (width-node_width) / (columns.length - 1);



	// Create the new SVG object that will represent our chart
	var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
	var padding_g = document.createElementNS("http://www.w3.org/2000/svg", "g")
	padding_g.setAttribute("transform", "translate(" + margin.left + "," + margin.top + ")");
	svg.appendChild(padding_g);

	// Create the group that will hold all of the edges to make sure they show up below nodes
	var edges_g = document.createElementNS("http://www.w3.org/2000/svg", "g");
	padding_g.appendChild(edges_g);

	// Create the group that will hold all the nodes after edges to make sure nodes show up on top
	var nodes_g = document.createElementNS("http://www.w3.org/2000/svg", "g");
	padding_g.appendChild(nodes_g);


	// Draw all of the node lines
	for (let column_index_string in columns) {
		let column_index = parseInt(column_index_string);
		var x = node_spacing * column_index;
		for (let node_index in columns[column_index]) {
			var node_id = columns[column_index][node_index];
			let node = nodes[node_id];

			// Build the node
			if (!node.passthrough) {
				var left_height = node.input * value_scale;
				var full_height = node.size * value_scale;
				var right_height = node.output * value_scale;
				if (Number(column_index) === 0) {
					left_height = full_height;
				}


				let d = "M 0,0 L 0,"+left_height+" "+node_width/3+","+left_height+" "+node_width/3+","+full_height+" "+node_width*2/3+","+full_height+" "+node_width*2/3+","+right_height+" "+node_width+","+right_height+" "+node_width+",0 Z";

				let node_g = document.createElementNS("http://www.w3.org/2000/svg", "g");
				node_g.setAttribute("transform", "translate(" + x + "," + node.y + ")");
				node_g.setAttribute("class", "node");


				var fill_color = get_color(node_id);
				var edge_color = color_darken(fill_color);


				let node_shape_elem = document.createElementNS("http://www.w3.org/2000/svg", "path")
				node_shape_elem.setAttribute("d", d)
				node_shape_elem.setAttribute("style", "fill: "+color_string(fill_color)+"; stroke: "+color_string(edge_color)+";")
				node_g.appendChild(node_shape_elem);

				var text_offset = node_width + 6;
				var text_anchor = "start";
				if (column_index >= columns.length/2){
					text_offset = -6;
					text_anchor = "end";
				}

				let node_name_text: SVGTextElement = document.createElementNS("http://www.w3.org/2000/svg", "text")
				node_name_text.setAttribute("x", text_offset.toString());
				node_name_text.setAttribute("y", (full_height/2).toString());
				node_name_text.setAttribute("dy", ".35em");
				node_name_text.setAttribute("text-anchor", text_anchor);
				node_name_text.textContent = node_id;
				node_g.appendChild(node_name_text);

				nodes_g.appendChild(node_g);
			}
		}
	}

	// Determine offset of all the edge connections
	function source_y(edge_id: string) {
		var edge = edges[edge_id];
		// if this is a passthrough edge get the last passthrough node instead of the source
		if (edge.passthrough_nodes.length > 0) {
			return nodes[edge.passthrough_nodes[edge.passthrough_nodes.length-1]].y;
		}
		else {
			return nodes[edge.source].y;
		}
	}
	function source_y_comp(a: string, b: string) {
		return source_y(a) - source_y(b);
	}

	function target_y(edge_id: string) {
		var edge = edges[edge_id];
		// if this is a passthrough edge get the first passthrough node instead of the target
		if (edge.passthrough_nodes.length > 0) {
			return nodes[edge.passthrough_nodes[0]].y;
		}
		else {
			return nodes[edge.target].y;
		}
	}
	function target_y_comp(a: string, b: string) {
		return target_y(a) - target_y(b);
	}
	for (let node_id in nodes) {
		let node = nodes[node_id];
		if (node.passthrough === false) {
			node.incoming_edges.sort(source_y_comp);
			node.outgoing_edges.sort(target_y_comp);

			var running_edge_height = 0;
			for (let edge_id in node.incoming_edges) {
				let edge = edges[node.incoming_edges[edge_id]];
				edge.target_y_offset = running_edge_height;
				running_edge_height += edge.value * value_scale;
			}
			running_edge_height = 0;
			for (let edge_id in node.outgoing_edges) {
				let edge = edges[node.outgoing_edges[edge_id]];
				edge.source_y_offset = running_edge_height;
				running_edge_height += edge.value * value_scale;
			}
		}
	}


	// Draw all of the edge Lines
	for (let edge_index in edges) {
		var edge = edges[edge_index];
		var line_thickness = edge.value * value_scale;

		let node_g = document.createElementNS("http://www.w3.org/2000/svg", "g")
		node_g.setAttribute("transform", "translate(" + 0 + "," + 0 + ")");

		var start_node = nodes[edges[edge_index].source];
		var end_node = nodes[edges[edge_index].target];

		var mid_x_mod = (node_spacing-node_width)/2;

		var start_x = start_node.column*node_spacing +node_width;
		var start_y = start_node.y + edge.source_y_offset + line_thickness/2;

		let d = "M" + start_x + "," + start_y + "C" + (start_x + mid_x_mod) + "," + start_y + " ";

		for (let passthrough_node_index in edges[edge_index].passthrough_nodes) {
			var passthrough_node = nodes[edges[edge_index].passthrough_nodes[passthrough_node_index]];
			var passthrough_x = passthrough_node.column*node_spacing;
			var passthrough_y = passthrough_node.y + line_thickness/2	;

			d += (passthrough_x - mid_x_mod) + "," + passthrough_y + " " + passthrough_x + "," + passthrough_y + "C" + (passthrough_x + mid_x_mod) + "," + passthrough_y + " ";
		}

		var end_x = end_node.column*node_spacing;
		var end_y = end_node.y + edge.target_y_offset + line_thickness/2;

		d += (end_x - mid_x_mod) + "," + end_y + " " + end_x + "," + end_y;

		let edge_shape_elem = document.createElementNS("http://www.w3.org/2000/svg", "path")
		edge_shape_elem.setAttribute("d", d)
		edge_shape_elem.setAttribute("style", "stroke-width: " + line_thickness + "px;")
		edge_shape_elem.setAttribute("class", "link")
		node_g.appendChild(edge_shape_elem);

		edges_g.appendChild(node_g);
	}

	var chart_width = width + margin.left + margin.right;
	var chart_height = height + margin.top + margin.bottom;


	svg.setAttribute("width", chart_width.toString());
	svg.setAttribute("height", chart_height.toString());
	chart_elem.appendChild(svg);
}




function get_input_size(edges: { [key: string]: ResourceEdge }, output: string): number{

	var inputs_size = 0;
	for (let edge in edges){
		if (edges[edge].target === output) {
			inputs_size += edges[edge].value;
		}
	}
	return inputs_size;
}


////////////////////////////////////////////////////////////////////////////////
/////////////////////////////// Hover Text Logic ///////////////////////////////
////////////////////////////////////////////////////////////////////////////////
// How far away from the mouse should the hoverbox be
let hover_x_offset: number = 10;
let hover_y_offset: number = -10;

document.addEventListener("mousemove", function(e: MouseEvent){
	// If the hoverbox is not hanging over the side of the screen when rendered, render normally
	if (window.innerWidth > hover_name_elem.offsetWidth + e.pageX + hover_x_offset) {
		hover_name_elem.style.left = (e.pageX + hover_x_offset).toString() + "px";
		hover_name_elem.style.top = (e.pageY + hover_y_offset).toString() + "px";
	}
	// If the hoverbox is hanging over the side of the screen then render on the other side of the mouse
	else {
		hover_name_elem.style.left = (e.pageX - hover_x_offset - hover_name_elem.offsetWidth).toString() + "px";
		hover_name_elem.style.top = (e.pageY + hover_y_offset).toString() + "px";
	}
});


////////////////////////////////////////////////////////////////////////////////
////////////////////////////// Hover Recipe Logic //////////////////////////////
////////////////////////////////////////////////////////////////////////////////
// function set_recipe (target, source, source_quantity) {
// 	var recipe = get_recipe(target);

// 	var source_item_count = -recipe.requirements[source];
// 	var item_multiplier = source_quantity / source_item_count;

// 	if (recipe.recipe_type === "crafting") {

// 		for (let i in recipe.recipe) {
// 			$("#crafting_slot_"+i).removeClass (function (index, className) {
// 				return (className.match (/\bitem_[a-z0-9_]*/) || []).join(" ");
// 			}).addClass("item_" + filenameify(recipe.recipe[i]));

// 			if (item_multiplier > 1 && recipe.recipe[i] !== null) {
// 				$("#crafting_slot_"+i).text(item_multiplier);
// 			}
// 			else {
// 				$("#crafting_slot_"+i).text("");
// 			}
// 		}
// 		$("#crafting_output_image").removeClass (function (index, className) {
// 			return (className.match (/\bitem_[a-z0-9_]*/) || []).join(" ");
// 		}).addClass("item_" + filenameify(target));

// 		if (recipe.output * item_multiplier > 1){
// 			$("#crafting_output_image").text(recipe.output * item_multiplier);
// 		}
// 		else {
// 			$("#crafting_output_image").text("");
// 		}
// 	}
// 	else {
// 		console.error("The recipe type for " + target + " has not been created yet");
// 	}
// }

// $(document).on("mousemove", function(e) {


// 	var left_offset = e.pageX + hover_x_offset;
// 	var top_offset = e.pageY + hover_y_offset;

// 	if ($(window).width() < $("#hover_recipe").outerWidth() + e.pageX + hover_x_offset ) {
// 		left_offset = e.pageX - hover_x_offset - $("#hover_recipe").outerWidth();
// 	}

// 	if ($(window).height() + $(document).scrollTop() < $("#hover_recipe").outerHeight() + e.pageY + hover_y_offset ) {
// 		top_offset = e.pageY - hover_y_offset - $("#hover_recipe").outerHeight();
// 	}

// 	$("#hover_recipe").offset ({
// 		left:  left_offset,
// 		top:   top_offset,
// 	});
// });



////////////////////////////////////////////////////////////////////////////////
/////////////////////////////// Recipe Switching ///////////////////////////////
////////////////////////////////////////////////////////////////////////////////


/******************************************************************************\
|
\******************************************************************************/
function switch_recipe(item_name: string, event: MouseEvent) {
	var recipe_selector = recipe_select_elem;

	// Clear the recipe selector list
	while (recipe_selector_list_elem.lastChild) {
		recipe_selector_list_elem.removeChild(recipe_selector_list_elem.lastChild);
	}

	for (let i = 0; i < recipe_json[item_name].length; i++) {
		var recipe_item = document.createElement("div");
		recipe_item.classList.add("recipe_select_item");

		recipe_item.addEventListener("click", (function(index: number) {
			return function() {
				set_recipe_index(item_name, index);
				find_loop_from_node(item_name);
				recipe_selector.style.opacity = "0";
				recipe_selector.style.pointerEvents = "none";
			};
		})(i));

		let recipe_category = document.createElement("div");
		recipe_category.classList.add("recipe_select_item_name");
		recipe_category.textContent = recipe_json[item_name][i].recipe_type;

		for (let j in recipe_json[item_name][i].requirements) {
			(function(j) {

				let quantity = -recipe_json[item_name][i].requirements[j];

				let item_elem = document.createElement("div");
				item_elem.classList.add("required_item");
				item_elem.classList.add("item");
				item_elem.classList.add("item_" + (resource_simple_names[j] ? resource_simple_names[j] : filenameify(j)));
				item_elem.textContent = quantity.toString();
				recipe_category.appendChild(item_elem);

				item_elem.addEventListener("mouseover", function() {
					hover_name_elem.textContent = quantity + "x " + j;
					hover_name_elem.style.opacity = "1";
				});
				item_elem.addEventListener("mouseout", function() {
					hover_name_elem.style.opacity = "0";
				});
			})(j);
		}
		recipe_item.appendChild(recipe_category);

		let clear_div = document.createElement("div");
		clear_div.classList.add("clear");
		recipe_item.appendChild(clear_div)

		recipe_selector_list_elem.appendChild(recipe_item);
	}

	recipe_selector.style.opacity = "1";
	recipe_selector.style.pointerEvents = "auto";



	var menu_x_offset = -10;
	var menu_y_offset = -10;

	var left_offset = event.pageX + menu_x_offset;
	var top_offset = event.pageY + menu_y_offset;

	if (window.innerWidth < recipe_selector.offsetWidth + event.pageX + menu_x_offset) {
		left_offset = event.pageX - menu_x_offset - recipe_selector.offsetWidth;
	}


	if (window.innerHeight + window.pageYOffset < recipe_selector.offsetHeight + event.pageY + menu_y_offset && event.pageY - menu_y_offset - recipe_selector.offsetHeight >= 0) {
		top_offset = event.pageY - menu_y_offset - recipe_selector.offsetHeight;
	}

	recipe_selector.style.top = top_offset.toString() + "px";
	recipe_selector.style.left = left_offset.toString() + "px";
}

function switch_inventory_amount_input(item_name: string) {
	inventory_amount_input_elem.setAttribute("item_name", item_name); //???
	if (inventory[item_name] === undefined) {
		inventory_amount_input_elem.value = "0";
	} else {
		inventory_amount_input_elem.value = inventory[item_name].toString();
	}
}

recipe_select_elem.addEventListener("mouseleave", function() {
	recipe_select_elem.style.opacity = "0";
	recipe_select_elem.style.pointerEvents = "none";
});


inventory_amount_input_elem.addEventListener("change", function(){
	let item_name = inventory_amount_input_elem.getAttribute("item_name");
	if (item_name === null) {
		// TODO: create a nicer method of identification where this can never
		// be true. Some sort of closure that has this value set already.
		console.error("No actively selected item name");
	}
	else {
		inventory[item_name] = parseInt(inventory_amount_input_elem.value);
		export_inventory_to_localstorage();
		export_inventory_to_textbox();
	}
});

inventory_amount_input_elem.addEventListener("focus", function() {
	this.select();
});

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

// TODO: This seems very related to the function loop at the top that is not
// well commented, see if we can combine these two things together in a
// reasonable way. Or split up the other loop to be like this one
/******************************************************************************\
| set_textbox_background                                                       |
|                                                                              |
| This function darkens the background of a textbox based on if the box has    |
| any text in it. It is paired with a focus and blur trigger that causes the   |
| background to go dark when clicked, and only go light again when the text    |
| box is blank.                                                                |
\******************************************************************************/
function set_textbox_background(textbox: HTMLInputElement){
	if (textbox.value === ""){
		textbox.style.backgroundColor = "rgba(0,0,0,0)";
	}
	else {
		textbox.style.backgroundColor = "rgba(0,0,0,.5)";
	}
}



// Run the load function to load arguments from the URL if they exist
load();
