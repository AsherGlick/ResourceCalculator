import { ResourceEdge } from "./resource_edge";

// This function groups the list of nodes into ones that should share
// the same column within the generated graph
export function get_node_columns(edges: { [key: string]: ResourceEdge }) {
	let nodes: string[] = [];

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
	var child_counts: { [key: string]: number } = {};
	var parent_counts: { [key: string]: number } = {};

	function populate_child_count(node: string){
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
	function populate_parent_count(node: string){
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