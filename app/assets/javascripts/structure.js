//= require nbt.js
//= require pako.js

(function($) {



	function display_error(error) {

	}

	function parse_nbt_file(evt) {
		// Retrieve the first (and only!) File from the FileList object
		var f = evt.target.files[0]; 


		if (f) {
			var r = new FileReader();
			r.onload = function(e) { 
				var contents = e.target.result;

				function hasGzipHeader(data) {
					var head = new Uint8Array(data.slice(0, 2));
					return head.length === 2 && head[0] === 0x1f && head[1] === 0x8b;
				}

				if (hasGzipHeader(contents)) {
					contents = pako.inflate(contents)
				}

				nbt.parse(contents	, function(error, data) {
					if (error) { throw error; }

					// console.log(data.value.stringTest.value);
					// console.log(data.value);
					build_block_count(data.value)
					// console.log(data.value['nested compound test'].value);
				});

			}
			r.readAsArrayBuffer(f);
		} else { 
			alert("Failed to load file");
			return;
		}


		// var data = fs.readFileSync('fixtures/bigtest.nbt.gz');
	}


	function build_block_count(parsed_structure_file) {
		// console.log(parsed_structure_file.blocks)
		// console.log(parsed_structure_file.palette)
		// console.log(parsed_structure_file.palette.value)
		// console.log()

		blocks = parsed_structure_file.blocks.value.value;
		palette = parsed_structure_file.palette.value.value

		block_list = {};

		palette_map = [];

		properties = [];

		air_block_index = -1;

		for (var i = 0; i < palette.length; i++) {
			// map between the index count and the palette blocks to produce a block count list
			// console.log(palette[i].Name.value)

			base_name = palette[i].Name.value

			// Special case of air, dont include this but save the id to ignore later
			if (base_name === "minecraft:air"){
				if (air_block_index === -1) {
					air_block_index = i;
					continue
				}
				else {
					console.log("TWO AIR BLOCKS DETECTED IN PALETTE!")
				}
			}


			if (palette[i].Properties !== undefined) {
				// console.log(palette[i].Properties.value)
				var keys = Object.keys(palette[i].Properties.value)
				for (var j = 0; j < keys.length; j++) {
					var key = keys[j]

					properties.push(key)

					if (properties_map[key]) {
						base_name += ":" +  palette[i].Properties.value[key].value
					}

					// console.log(properties_map)


					// console.log(palette[i].Properties.value[key].value)
				}
			}

			if (name_mappings[base_name] === undefined) {
				console.log(base_name + " not found in name mappings, ignoring")
			}

			palette_map[i] = name_mappings[base_name]

			// console.log(base_name)

		}

		function onlyUnique(value, index, self) { 
		    return self.indexOf(value) === index;
		}

		// usage example:
		var unique_properties = properties.filter( onlyUnique ); // returns ['a', 1, 2, '1']









		// Read the blocks and add to the block list





		// palette_count = Array.apply(null, Array(palette.length)).map(Number.prototype.valueOf,0);


		for (var i = 0; i < blocks.length; i++) {
			palette_block_index = blocks[i].state.value
			// palette_count[palette_block_index] += 1

			// Skip air blocks
			if (palette_block_index === air_block_index) continue;

			if (blocks[i].nbt !== undefined) {
				// console.log(blocks[i].nbt.value.id.value)
				if (blocks[i].nbt.value.id.value === "minecraft:skull") {
					// do something special
					continue
				}
				else if (blocks[i].nbt.value.id.value === "minecraft:banner") {
					// do something special
					continue
				}
			}

			block_name = palette_map[palette_block_index]

			if (block_name === undefined) {
				console.log("BLOCK NAME IS UNDEFINED, SKIPPING")
			}

			// If the block does not exist initilize it
			if (block_list[block_name] === undefined) {
				block_list[block_name] = 0
			}
			// add one to the block
			block_list[block_name] += 1

		}

		console.log(block_list)

		display_url(block_list)





	}


	function display_url(block_list) {
		var outputbox = $("#outputbox");
		item_list = {}


		var block_keys = Object.keys(block_list);
		for (var i = 0; i < block_keys.length; i++) {
			// outputbox.text(outputbox.text() + block_keys[i] + ":" + block_list[block_keys[i]] + "\n")
			// outputbox.innerHTML += block_keys[i] + ":" + block_list[block_keys[i]] + "<br>";

			var block_url_name = block_keys[i];
			item_list[block_url_name] = block_list[block_keys[i]]
		}

		outputbox.text($.param(item_list));
	}



	$(window).load(function(){


		// Monitor the file input box and check if it changes, if it does load the new file
		document.getElementById('fileinput').addEventListener('change', parse_nbt_file, false);
	});
})(jQuery);



