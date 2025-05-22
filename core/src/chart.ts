import { ResourceEdge } from "./resource_edge";
import { get_node_columns } from "./node_columns";


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
| generate_chart                                                               |
|                                                                              |
| This function is in charge of drawing the sankey chart onto the canvas       |
|
| Arguments
|   generation_events -
\******************************************************************************/
export function generate_chart(
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
