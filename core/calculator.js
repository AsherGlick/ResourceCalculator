////////////////////////////////////////////////////////////////////////////////
// calculator.js handles all of the javascript for the calculator page
////////////////////////////////////////////////////////////////////////////////

// Closure wrapper for the script file
(function($) {"use strict";$(window).on("load", function(){
// Closure wrapper for the script file

////////////////////////////////////////////////////////////////////////////////
////////////////////////////// Header Bar Logics ///////////////////////////////
////////////////////////////////////////////////////////////////////////////////

/******************************************************************************\
| "Reset Item Counts" Button Logic                                             |
\******************************************************************************/
function clear_item_counts() {
	$(".desired_item").each(function() {
		var field = $(this).find(".desired_item_count");
		field.val("");
		set_textbox_background(field);
	});

	$("#unused_hide_checkbox").prop("checked");

	$("#unused_hide_checkbox").prop("checked", false).change();
	generatelist();
}
$("#reset_item_count").click(clear_item_counts);


/******************************************************************************\
| "About Us" Button Logic                                                      |
\******************************************************************************/
$("#about_button").click(function() {
	$("#about_us").slideToggle();
});

$("input[name=unit_name]").click(function() {
	generatelist();
});

// Bind events to the item list elements // TODO THIS FUNCTION NEEDS A BETTER COMMENT
$(".desired_item").each(function() {
	var item = $(this);
	var item_input_box = item.find(".desired_item_count");

	// When clicking on the box focus the text box
	item.click(function() {
		item_input_box.focus();
	});

	// Make the item counts save when modified
	item_input_box.bind("propertychange change click keyup input paste", function() {
		save();
	});

	// Put an orage border around the item when the text box is focused
	// This makes it more noticeable when an item is selected
	item_input_box.focus(function() {
		item.addClass("desired_item_input_focused");
	});
	item_input_box.blur(function() {
		item.removeClass("desired_item_input_focused");
	});

	// When doubleclicking open the recipe select menu
	item.dblclick( function (event) {
		switch_recipe(item.attr("mc_value"), event);
	});

	// Enable item name hover text
	item.mouseover( function() {
		$("#hover_name").text(item.attr("mc_value"));
		$("#hover_name").css("opacity", 1);
	});
	item.mouseout( function() {
		$("#hover_name").css("opacity", 0);
	});
});

/******************************************************************************\
| Search Bar filter logic
\******************************************************************************/
function filter_items() {
	var search_string = $("#item_filter").val().toLowerCase();
	var hide_unused = $("#unused_hide_checkbox").prop("checked");

	// Loop through each item
	$("#content_field").find(".desired_item").each(function() {
		var item_name = $(this).attr("mc_value").toLowerCase();
		var item_count = $(this).find(".desired_item_count").val();

		// If the search string does not match hide the item
		// If the item count is not greated then 0 and hide unused is true hide
		if (item_name.indexOf(search_string) === -1 || !(item_count > 0 || !hide_unused)) {
			$(this).hide();
		}
		else {
			$(this).show();
		}
	});
}
$("#item_filter").bind("propertychange change click keyup input paste", function(){
	filter_items();
});


/******************************************************************************\
| "Hide Unused" "Show Unused" Button Logic                                     |
\******************************************************************************/
$("#unused_hide_checkbox").change(function() {
	if ($(this).prop("checked")) {
		$("label[for='"+$(this).attr("id")+"']")
			.text("Show Unused");
	}
	else {
		$("label[for='"+$(this).attr("id")+"']")
			.text("Hide Unused");
	}
	filter_items();
});


////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////// // TODO THIS FUNCTION NEEDS A BETTER PLACE TO LIVE
////////////////////////////////////////////////////////////////////////////////
function filenameify(rawname) {
	if (rawname === null) {
		return "";
	}
	return rawname.toLowerCase().replace(/[^a-z]/g, "");
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
	var selected_items = {};
	$(".desired_item").each(function() {
		var key = $(this).find(".desired_item_count").attr("id");
		// console.log(key);
		var value = $(this).find(".desired_item_count").val();

		if ($.isNumeric(value)) {
			// Set the value as negative to indicate they are needed
			selected_items[key] = value;
		}

	});
	if(history.pushState) {
		history.pushState(null, null, "#"+$.param(selected_items));
	}
	else {
		window.location.hash = $.param(selected_items);
	}

}


/******************************************************************************\
| load()                                                                       |
|                                                                              |
| This function is an inverse to save() and reads the state of the resource    |
| requirement list from the UIR hash. In addition it will automatically call   |
| generatelist() to save the user from having to click the button for a saved  |
| list.                                                                        |
\******************************************************************************/
function load() {
	var uri_arguments = decodeURIComponent(window.location.hash.substr(1));
	if (uri_arguments !== "") {
		var pairs = uri_arguments.split("&");
		for(let i in pairs){
			var split = pairs[i].split("=");
			var id = decodeURIComponent(split[0]);
			var value = decodeURIComponent(split[1]);
			$("#"+id).val(value);
			set_textbox_background($("#"+id));
		}
		$("#unused_hide_checkbox").prop("checked", true).change();
		generatelist();
	}
	$("#unused_hide_checkbox").change();
}


////////////////////////////////////////////////////////////////////////////////
///////////////////////// Requirements Calculation Logic ///////////////////////
////////////////////////////////////////////////////////////////////////////////
$("#generatelist").click(generatelist);



function negative_requirements_exist(requirements) {
	for (let requirement in requirements){
		if (requirements[requirement] < 0) {
			return true;
		}
	}
	return false;
}


function generatelist() {
	var original_requirements = gather_requirements();
	var requirements = JSON.parse(JSON.stringify(original_requirements));
	var resource_tracker = {};
	var generation_totals = {}; // the total number of each resource produce (ignoring any consumption)

	var raw_resources = {};

	// While we still have something that requires another resource to create
	while(negative_requirements_exist(requirements)) {

		// We create a copy of requirements so that the original can stay
		// unmodified while iterating over it in the for loop
		var output_requirements = JSON.parse(JSON.stringify(requirements));

		// For each negative requirement get it's base resources
		for (let requirement in requirements){
			if (requirements[requirement] < 0) {


				var recipe = get_recipe(requirement).requirements;
				var produces_count = get_recipe(requirement).output;
				var required_count = -requirements[requirement];

				// Figure out the minimum number of a given requirement can be produced
				// to fit the quantity of that requirement needed.
				// EG: if a recipe produces 4 of an item but you only need 3
				//     then you must produce 4 of that item with 1 left over
				var produce_count = Math.ceil(required_count/produces_count);
				output_requirements[requirement] += produce_count * produces_count;

				// Add the quantity of the item created to the generation_totals
				// This is used to keep track of how many of any item in the crafting process are produced
				if (!(requirement in generation_totals)) {
					generation_totals[requirement] = 0;
				}
				generation_totals[requirement] += produce_count * produces_count;

				// if this is a raw resource then add it to the raw resource list
				if (recipe[requirement] === 0 && Object.keys(recipe).length === 1) {
					if (raw_resources[requirement] === undefined) {
						raw_resources[requirement] = 0;
					}
					raw_resources[requirement] += produce_count * produces_count;
				}

				// If this is not a raw resource, track the change the  and modify the output requirements
				else {
					$.each(recipe, function(item) {
						// Set the recipe requirements as new output requirements
						if (output_requirements[item] === undefined) {
							output_requirements[item] = 0;
						}
						output_requirements[item] += recipe[item] * produce_count;

						// Add the recipe's conversion
						var tracker_key = requirement+item;
						if (!(tracker_key in resource_tracker)) {
							resource_tracker[tracker_key] = {
								"source":item,
								"target":requirement,
								"value":0,
							};
						}
						resource_tracker[tracker_key].value += recipe[item] * -produce_count;
					});
				}
			}
		}
		requirements = output_requirements;
	}

	for (let original_requirement in original_requirements) {
		// console.log(get_recipe(original_requirement));
		if (get_recipe(original_requirement).recipe_type === "Raw Resource") {
			resource_tracker[original_requirement + "final"] = {
				"source": original_requirement,
				"target": "[Final] " + original_requirement,
				"value": -original_requirements[original_requirement],
			};
		}
	}


	// This maps all extra items to an extra value
	// It is done in order to get the right heights for items that produce more then they take
	// TODO, it might be nice to have a special path instead of a node to represent "extra"
	for (let key in output_requirements) {
		if (output_requirements[key] > 0) {
			var tracker_key = key+"extra";
			resource_tracker[tracker_key] = {
				"source":key,
				"target":"[Extra] " + key,
				"value":output_requirements[key],
			};
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

			var final_trakcer = source+"final";
			resource_tracker[final_trakcer] = {
				"source": source,
				"target":"[Final] " + source,
				"value": -original_requirements[source],
			};

			// Add in value of the non-extra resource
			generation_totals["[Final] " + source] = -original_requirements[source];
		}
	}



	generate_chart(resource_tracker, generation_totals);
	generate_instructions(resource_tracker, generation_totals);
}


/******************************************************************************\
|
\******************************************************************************/
function gather_requirements() {
	var resources = {};
	$(".desired_item").each(function() {
		var key = $(this).attr("mc_value");
		var value = $(this).find(".desired_item_count").val();

		if ($.isNumeric(value)) {
			// Set the value as negative to indicate they are needed
			resources[key] = -value;
		}

	});
	return resources;
}

////////////////////////////////////////////////////////////////////////////////
////////////////////////// Text Instruction Creation ///////////////////////////
////////////////////////////////////////////////////////////////////////////////
function generate_instructions(edges, generation_totals) {
	var node_columns = get_node_columns(edges);

	var instructions = $("<div/>");
	var column_count = 0;

	$("<div/>").attr("id", "text_instructions_title").text("Base Ingredients").appendTo(instructions);
	// List out raw resource numbers
	for (let node in node_columns){
		if (node_columns[node] === 0) {


			var line_wrapper = $("<div/>");
			line_wrapper.addClass("instruction_wrapper");
			var base_ingredients = text_item_object(generation_totals[node], node);
			base_ingredients.appendTo(line_wrapper);
			line_wrapper.appendTo(instructions);

		}

		// Track the largest column as the max column count
		if (node_columns[node] >= column_count) {
			column_count = node_columns[node]+1;
		}
	}

	$("<div/>").attr("id", "text_instructions_title").text("Text Instructions [Beta]").appendTo(instructions);

	// Create the step by step instructions
	for (let i = 1; i < column_count; i++) {
		for (let node in node_columns) {
			if (node_columns[node] === i) {

				if (node.startsWith("[Final]") || node.startsWith("[Extra]")){
					continue;
				}

				build_instruction_line(edges, node, generation_totals).appendTo(instructions);
			}
		}
		var line_break = $("<div/>");
		line_break.addClass("instruction_line_break");
		line_break.appendTo(instructions);
	}

	// Delete any old instructions
	var text_instructions = document.getElementById("text_instructions");
	while (text_instructions.firstChild) {
		text_instructions.removeChild(text_instructions.firstChild);
	}

	// Add the new instruction list to the page
	instructions.appendTo($("#text_instructions"));

}

function build_instruction_line(edges, item_name, generation_totals) {
	// Build the input item sub string
	var inputs = {};
	for (let edge in edges){
		// If this is pointing into the resource we are currently trying to craft
		if (edges[edge].target === item_name) {
			inputs[edges[edge].source] = edges[edge].value;
		}
	}

	var recipe_type = get_recipe(item_name).recipe_type;

	return recipe_type_functions[recipe_type](inputs, item_name, generation_totals[item_name], text_item_object);
}


function build_unit_value_list(number, unit_name) {
	if (number === 0) {
		return [];
	}
	if (unit_name === null) {
		return [{"name":null, "count":number}];
	}

	var unit = stack_sizes[unit_name];
	var unit_size = unit.quantity_multiplier;
	var quotient = Math.floor(number/unit_size);
	var remainder = number % unit_size;

	var value_list = [];

	if (quotient > 0) {
		var value_list_element = {};
		if (quotient > 1) {
			value_list_element.name = unit.plural;
		}
		else {
			value_list_element.name = unit_name;
		}
		value_list_element.count = quotient;
		value_list = [value_list_element];

	}

	// recurse down all the other possible units until
	value_list = value_list.concat(build_unit_value_list(remainder, unit.extends_from));

	return value_list;
}

function text_item_object(count, name){
	var item_object = $("<div/>");
	item_object.addClass("instruction_item");


	var units = $("input[name=unit_name]:checked").val();
	if (units !== "" && units !== undefined) {
		var unit_value_list = build_unit_value_list(count, units);

		let count_object = $("<div/>");
		count_object.addClass("instruction_item_count");
		var join_plus_character = "";
		for (let i = 0; i < unit_value_list.length; i++){
			$("<span/>").text(join_plus_character + unit_value_list[i].count).appendTo(count_object);
			if (unit_value_list[i].name !== null) {
				$("<span/>").text("("+unit_value_list[i].name+")").addClass("small_unit_name").appendTo(count_object);
			}
			join_plus_character="+";
		}
		count_object.appendTo(item_object);
	}
	else {
		let count_object = $("<div/>");
		count_object.addClass("instruction_item_count");
		count_object.text(count);
		count_object.appendTo(item_object);
	}

	var space_object = $("<span/>");
	space_object.text(" ");
	space_object.appendTo(item_object);

	var name_object = $("<div/>");
	name_object.addClass("instruction_item_name");
	name_object.text(name);
	name_object.appendTo(item_object);

	return item_object;
}

// This function groups the list of nodes into ones that should share
// the same column within the generated graph
function get_node_columns(edges) {
	var nodes = [];

	// Start by getting a list of all the nodes
	for (let edge in edges){
		if (nodes.indexOf(edges[edge].source) === -1) {
			nodes.push(edges[edge].source);
		}
		if (nodes.indexOf(edges[edge].target) === -1) {
			nodes.push(edges[edge].target);
		}
	}

	// Recursively populate the child count and parent counts via javascript closure magic
	var child_counts = {};
	var parent_counts = {};

	function populate_child_count(node){
		if (!(node in child_counts)) {
			child_counts[node] = 0;
			for (let edge in edges){
				if (edges[edge].source === node) {
					// make sure that this child has the correct child count
					populate_child_count(edges[edge].target);
					// If this child's child count is larger then any other child's thus far save it as the longest
					if (child_counts[edges[edge].target]+1 > child_counts[node]){
						child_counts[node] = child_counts[edges[edge].target]+1;
					}
				}
			}
		}
	}
	function populate_parent_count(node){
		if (!(node in parent_counts)) {
			parent_counts[node] = 0;
			for (let edge in edges){
				if (edges[edge].target === node) {
					// make sure that this child has the correct child count
					populate_parent_count(edges[edge].source);
					// If this child's child count is larger then any other child's thus far save it as the longest
					if (parent_counts[edges[edge].source]+1 > parent_counts[node]){
						parent_counts[node] = parent_counts[edges[edge].source]+1;
					}
				}
			}
		}
	}

	for (let node in nodes)  {
		populate_child_count(nodes[node]);
		populate_parent_count(nodes[node]);
	}

	var max_column_index = 0;
	for (let node in parent_counts) {
		if (parent_counts[node] > max_column_index) {
			max_column_index = parent_counts[node];
		}
	}

	// Snap all final results to the rightmost column
	for (let node in child_counts) {
		if (child_counts[node] === 0) {
			parent_counts[node] = max_column_index;
		}
	}

	return parent_counts;
}

function get_columns(edges) {
	var node_columns = get_node_columns(edges);

	// deterimine how many columns there should be
	var column_count = 0;
	for (let node in node_columns) {
		if (node_columns[node]+1 > column_count) {
			column_count = node_columns[node]+1;
		}
	}

	// Create an array of those columns
	var columns = Array(column_count);
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

/******************************************************************************\
| generate_chart                                                               |
|                                                                              |
| This function is in charge of drawing the sankey chart onto the canvas       |
|
| Arguments
|   generation_events -
\******************************************************************************/
function generate_chart(edges, node_quantities) {

	// Set the margins for the area that the nodes and edges can take up
	var margin = {
		top: 10,
		right: 1,
		bottom: 10,
		left: 1,
	};

	// Reset the colors that have already been selected so we can get repeatable graphs
	selected_colors = {};

	// Set the space betwen the bottom of one node and the top of the one below it to 10px
	var node_padding = 10;

	// Calculate the widthe and the height of the area that the nodes and edges can take up
	var width = $("#content").width() - margin.left - margin.right;
	var height = 800 - margin.top - margin.bottom;

	// Get the matrix of nodes, sorted into an array of columns
	var columns = get_columns(edges);

	// Create a representation of node objects
	var nodes = {};
	for (let column_id in columns) {
		for (let node_id in columns[column_id]) {
			var node_name = columns[column_id][node_id];
			// console.log(node);
			nodes[node_name] = {
				"input": get_input_size(edges, node_name),
				"output": node_quantities[node_name],
				"size": Math.max(node_quantities[node_name], get_input_size(edges, node_name)),
				"column": Number(column_id),
				"passthrough": false,
				"incoming_edges":[],
				"outgoing_edges":[],
			};
		}
	}

	// Assign all edges to the nodes depending if the edge connects as a source
	// or as a target for the given node. Also cache which column the node is
	// in for the next step of finding edges that span multiple columns
	for (let edge_id in edges) {
		let edge = edges[edge_id];

		nodes[edge.target].incoming_edges.push(edge_id);
		nodes[edge.source].outgoing_edges.push(edge_id);
		edge.target_column = nodes[edge.target].column;
		edge.source_column = nodes[edge.source].column;
	}

	// Find edges that span multiple columns and create fake nodes for them in
	// the columns they pass over. This allows us to weight the edges so they
	// wont be overlapped by a node in that column
	for (let edge_id in edges){
		let edge = edges[edge_id];
		edge.passthrough_nodes = [];

		var source_column_index = edge.source_column;
		var target_column_index = edge.target_column;

		for (let passthrough_column_index=source_column_index+1; passthrough_column_index<target_column_index; passthrough_column_index+=1) {
			var passthrough_node_id = edge_id + "_" + passthrough_column_index;

			nodes[passthrough_node_id] = {
				"size": edge.value,
				"passthrough_node_index": edge.passthrough_nodes.length,
				"passthrough_edge_id": edge_id,
				"column":passthrough_column_index,
				"passthrough": true,
			};
			edge.passthrough_nodes.push(passthrough_node_id);
			columns[passthrough_column_index].push(passthrough_node_id);
		}
	}

	// Calculate the scale of a single item based on the tallest column of items
	// such that that column fits within the alloted height of the chart
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
	layout_chart(columns, nodes, edges, node_padding, width, height, value_scale, margin);
}


function set_node_positions(iterations, columns, nodes, edges, value_scale, node_padding, svg_height) {
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

function relax_columns_left_to_right(alpha, columns, nodes, edges) {
	function weighted_source_sum(node) {
		var sum = 0;
		if (node.passthrough === false) {
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
	function raw_source_sum(node) {
		// If the node is not a passthroguh then return the sum of all of
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
function relax_columns_right_to_left(alpha, columns, nodes, edges) {
	function weighted_target_sum(node) {
		var sum = 0;
		if (node.passthrough === false) {
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
	function raw_target_sum(node) {
		// If the node is not a passthroguh then return the sum of all of
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

function y_midpoint(node) {
	return node.y + node.height / 2;
}

function resolve_node_collisions(columns, nodes, node_padding, svg_height) {
	function y_comp(a, b) {
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
				// console.log("Pushing Up:", delta_y);
				node.y += delta_y;
			}

			top_of_previous_node = node.y - node_padding;
		}
	}
}




function hexToRgb(hex) {
	var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
	return result ? {
		r: parseInt(result[1], 16),
		g: parseInt(result[2], 16),
		b: parseInt(result[3], 16),
	} : null;
}

function color_darken(color) {
	var k = 0.49;

	return {
		r: Math.round(color.r * k),
		g: Math.round(color.g * k),
		b: Math.round(color.b * k),
	};
}

function color_string(color){
	return "rgb("+color.r+","+color.g+","+color.b+")";
}


/******************************************************************************\
| get_color
|
| This function supplies a color for a node to use as it's fill color. The
| color is determined by the first word in the string, excluding a [Extra] or
| [Final] prefix. The first time that key is presented to the function a new
| color is chosen for that key, each subsiquent call after the first  with the
| same key will return the same color but this is not necessarily the case for
| a new chart generation.
\******************************************************************************/
var all_colors = [
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
var selected_colors = {};
function get_color(key) {
	// Strip out Extra and Final prefixes
	key = key.replace(/^\[Extra\] /, "");
	key = key.replace(/^\[Final\] /, "");

	// Strip out everything past the first word
	key = key.replace(/ .*/, "");

	// Lookup or set the color that is attached to this key
	var index = selected_colors[key];
	if (index === undefined) {
		index = Object.keys(selected_colors).length % all_colors.length;
		selected_colors[key] = index;
	}

	return all_colors[index];
}



/******************************************************************************\
| layout_chart
|
| draw the chart itself
\******************************************************************************/
function layout_chart(columns, nodes, edges, node_padding, width, height, value_scale, margin) {
	var node_width = 20;

	// Determine the space between the left hand side of each node column
	var node_spacing = (width-node_width) / (columns.length-1);

	// Empty the chart immediately
	$("#chart").empty();

	// Create the new SVG object that will represent our chart
	var svg = $(document.createElementNS("http://www.w3.org/2000/svg", "svg"));
	var padding_g = $(document.createElementNS("http://www.w3.org/2000/svg", "g")).attr("transform", "translate("+margin.left+","+margin.top+")").appendTo(svg);
	// Create the group that will hold all of the edges to make sure they show up below nodes
	var edges_g = $(document.createElementNS("http://www.w3.org/2000/svg", "g")).appendTo(padding_g);
	// Create the group that will hold all the nodes after edges to make sure nodes show up on top
	var nodes_g = $(document.createElementNS("http://www.w3.org/2000/svg", "g")).appendTo(padding_g);

	// Draw all of the node lines
	for (let column_index in columns) {
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

				let node_g = $(document.createElementNS("http://www.w3.org/2000/svg", "g")).attr("transform", "translate("+x+","+node.y+")").attr("class", "node");


				var fill_color = get_color(node_id);
				var edge_color = color_darken(fill_color);


				$(document.createElementNS("http://www.w3.org/2000/svg", "path")).attr("d", d).attr("style", "fill: "+color_string(fill_color)+"; stroke: "+color_string(edge_color)+";").appendTo(node_g);

				var text_offset = node_width + 6;
				var text_anchor = "start";
				if (column_index >= columns.length/2){
					text_offset = -6;
					text_anchor = "end";
				}

				$(document.createElementNS("http://www.w3.org/2000/svg", "text")).attr("x", text_offset).attr("y", full_height/2).attr("dy", ".35em").attr("text-anchor", text_anchor).text(node_id).appendTo(node_g);
				node_g.appendTo(nodes_g);
			}
		}
	}

	// Determine offset of all the edge connections
	function source_y(edge_id) {
		var edge = edges[edge_id];
		// if this is a passthrough edge get the last passthrough node instead of the source
		if (edge.passthrough_nodes.length > 0) {
			return nodes[edge.passthrough_nodes[edge.passthrough_nodes.length-1]].y;
		}
		else {
			return nodes[edge.source].y;
		}
	}
	function source_y_comp(a, b) {
		return source_y(a) - source_y(b);
	}

	function target_y(edge_id) {
		var edge = edges[edge_id];
		// if this is a passthrough edge get the first passthrough node instead of the target
		if (edge.passthrough_nodes.length > 0) {
			return nodes[edge.passthrough_nodes[0]].y;
		}
		else {
			return nodes[edge.target].y;
		}
	}
	function target_y_comp(a, b) {
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

		let node_g = $(document.createElementNS("http://www.w3.org/2000/svg", "g")).attr("transform", "translate("+0+","+0+")");

		var start_node = nodes[edges[edge_index].source];
		var end_node = nodes[edges[edge_index].target];

		var mid_x_mod = (node_spacing-node_width)/2;

		var start_x = start_node.column*node_spacing +node_width;
		var start_y = start_node.y + edge.source_y_offset + line_thickness/2;

		let d="M"+start_x+","+start_y+"C"+(start_x+mid_x_mod)+","+start_y+" ";

		for (let passthrough_node_index in edges[edge_index].passthrough_nodes) {
			var passthrough_node = nodes[edges[edge_index].passthrough_nodes[passthrough_node_index]];
			var passthrough_x = passthrough_node.column*node_spacing;
			var passthrough_y = passthrough_node.y + line_thickness/2	;

			d += (passthrough_x-mid_x_mod)+","+passthrough_y+" "+passthrough_x+","+passthrough_y+"C"+(passthrough_x + mid_x_mod)+","+passthrough_y+" ";
		}

		var end_x = end_node.column*node_spacing;
		var end_y = end_node.y + edge.target_y_offset + line_thickness/2;

		d+=(end_x-mid_x_mod)+","+end_y+" "+end_x+","+end_y;

		$(document.createElementNS("http://www.w3.org/2000/svg", "path")).attr("d", d).attr("style", "stroke-width: "+line_thickness+ "px;").attr("class", "link").appendTo(node_g);
		node_g.appendTo(edges_g);
	}

	var chart_width = width + margin.left + margin.right;
	var chart_height = height + margin.top + margin.bottom;

	svg.appendTo($("#chart")).attr("width", chart_width).attr("height", chart_height);
}




function get_input_size(edges, output){

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
// How far away from the mouse should hte hoverbox be
var hover_x_offset = 10;
var hover_y_offset = -10;
$(document).on("mousemove", function(e){

	// If the hoverbox is not hanging over the side of the screen when rendered, render normally
	if ($(window).width() > $("#hover_name").outerWidth() + e.pageX + hover_x_offset) {

		$("#hover_name").offset	({
			left:  e.pageX + hover_x_offset,
			top:   e.pageY + hover_y_offset,
		});
	}
	// If the hoverbox is hanging over the side of the screen then render on the other side of the mouse
	else {

		$("#hover_name").offset	({
			left:  e.pageX - hover_x_offset - $("#hover_name").outerWidth(),
			top:   e.pageY + hover_y_offset,
		});
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
function switch_recipe(item_name, event) {
	var recipe_selector = $("#recipe_select");
	var recipe_selector_list = $("#recipe_selector_list");
	recipe_selector_list.empty();

	for (let i in recipe_json[item_name]) {
		var recipe_item = $("<div/>");
		recipe_item.addClass("recipe_select_item");

		recipe_item.click( (function(index) {
			return function() {
				set_recipe_index(item_name, index);
				find_loop_from_node(item_name);
				recipe_selector.css("opacity", 0);
				recipe_selector.css("pointer-events", "none");
			};
		})(i));

		var recipe_category = $("<div/>").addClass("recipe_select_item_name").text(recipe_json[item_name][i].recipe_type);

		for (let j in recipe_json[item_name][i].requirements) {
			(function(j) {

				var quantity = -recipe_json[item_name][i].requirements[j];

				var item = $("<div/>")
					.addClass("required_item")
					.addClass("item")
					.addClass("item_" + filenameify(j))
					.text(quantity)
					.appendTo(recipe_category);

				item.mouseover( function() {
					$("#hover_name").text(quantity +"x "+j);
					$("#hover_name").css("opacity", 1);
				});
				item.mouseout( function() {
					$("#hover_name").css("opacity", 0);
				});
			})(j);
		}
		recipe_category.appendTo(recipe_item);
		$("<div/>").addClass("clear").appendTo(recipe_item);
		recipe_item.appendTo(recipe_selector_list);
	}

	recipe_selector.css("opacity", 1);
	recipe_selector.css("pointer-events", "auto");



	var menu_x_offset = -10;
	var menu_y_offset = -10;

	var left_offset = event.pageX + menu_x_offset;
	var top_offset = event.pageY + menu_y_offset;

	if ($(window).width() < recipe_selector.outerWidth() + event.pageX + menu_x_offset ) {
		left_offset = event.pageX - menu_x_offset - recipe_selector.outerWidth();
	}
	if ($(window).height() + $(document).scrollTop() < recipe_selector.outerHeight() + event.pageY + menu_y_offset ) {
		top_offset = event.pageY - menu_y_offset - recipe_selector.outerHeight();
	}

	recipe_selector.offset ({
		left:  left_offset,
		top:   top_offset,
	});
}


$("#recipe_select").mouseleave(function() {
	$("#recipe_select").css("opacity", 0);
	$("#recipe_select").css("pointer-events", "none");
});


////////////////////////////////////////////////////////////////////////
/////////////////////// Selection and modification of raw resources/////
////////////////////////////////////////////////////////////////////////

var alternate_recipe_selections = {};

function set_recipe_index(node_name, recipe_index) {
	alternate_recipe_selections[node_name] = recipe_index;
	if (recipe_index === 0) {
		delete alternate_recipe_selections[node_name];
	}
}

function get_recipe_index(node_name) {
	if (!(node_name in alternate_recipe_selections)) {
		return 0;
	}
	else {
		return alternate_recipe_selections[node_name];
	}
}
function set_recipe_to_raw(node_name) {
	// console.log("Setting as raw resource");

	for (let i in recipe_json[node_name]){
		if (recipe_json[node_name][i].recipe_type === "Raw Resource"){
			set_recipe_index(node_name, i);
			return;
		}
	}
	alert("ERROR: Failed to set raw resource for " + node_name);
}



function get_recipe(node_name) {
	return recipe_json[node_name][get_recipe_index(node_name)];
}

function find_loop_from_node(start_node) {
	// Generate Light Node Mapping
	var nodes = {};
	for (let node in recipe_json)  {
		// Add all the edges
		nodes[node] = [];
		for (let edge in get_recipe(node).requirements) {
			// console.log(get_recipe(node).requirements[edge]);
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
function depth_first_search(nodes, node, match) {
	var changes = [];

	// loop through recipe requirements
	for (let i in nodes[node]) {
		// if a requirement is the original node then change this item to a soruce and report back
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
function set_textbox_background(textbox){
	if ($(textbox).val() === ""){
		$(textbox).css("background-color", "rgba(0,0,0,0)");
	}
	else {
		$(textbox).css("background-color", "rgba(0,0,0,.5)");
	}
}
$(".desired_item_count").focus(function() {
	$(this).css("background-color", "rgba(0,0,0,.5)");
	$(this).select();
});
$(".desired_item_count").blur(function() {
	set_textbox_background(this);
});

// Run the load function to load arguments from the URL if they exist
load();

// Closure wrapper for the script file
});})(jQuery);
// Closure wrapper for the script file
