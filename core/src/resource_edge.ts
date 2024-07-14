export class ResourceEdge {
	public source: string;
	public target: string;
	public value: number;

	public passthrough_nodes: string[] = []; // temporarily used later on

	public source_y_offset: number = 0; // temporarily used later for positioning
	public target_y_offset: number = 0; // temporarily used later for positioning


	constructor(source: string, target: string, value: number) {
		this.source = source;
		this.target = target;
		this.value = value;
	}
}
