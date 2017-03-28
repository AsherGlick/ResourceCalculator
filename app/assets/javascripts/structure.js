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


	////////////////////////////////////////////////////////////////////////////
	// The function parses the palette builds a list of item counts based on the pallet indexes
	////////////////////////////////////////////////////////////////////////////
	function build_block_count(parsed_structure_file) {
		// console.log(parsed_structure_file.blocks)
		// console.log(parsed_structure_file.palette)
		// console.log(parsed_structure_file.palette.value)
		// console.log()

		blocks = parsed_structure_file.blocks.value.value;
		palette = parsed_structure_file.palette.value.value

		block_list = {};

		// A palette list to use for the resource block
		palette_map = [];

		// A list of all the property keys any block may have
		properties = [];

		air_block_index = -1;

		for (var i = 0; i < palette.length; i++) {

			// Grab the base item name
			base_name = palette[i].Name.value

			// Special case of air, don't include this but save the id to ignore later
			if (base_name === "minecraft:air"){
				if (air_block_index === -1) {
					air_block_index = i;
					continue
				}
				else {
					console.log("TWO AIR BLOCKS DETECTED IN PALETTE!")
				}
			}

			// For anything that has properties (like color) add the properties to the name
			// MODIFIES base_name
			if (palette[i].Properties !== undefined) {
				var keys = Object.keys(palette[i].Properties.value)
				for (var j = 0; j < keys.length; j++) {
					var key = keys[j]

					properties.push(key)

					if (properties_map[key]) {
						base_name += ":" +  palette[i].Properties.value[key].value
					}
				}
			}

			// If a global name mapping for the item cannot be found then ignore it and throw a warning
			if (name_mappings[base_name] === undefined) {
				console.log(base_name + " not found in global name mappings, Ignoring. If this item should be mapped to a resource calculator recipe add it to the global mapping list")
			}

			palette_map[i] = name_mappings[base_name]
		}

		function onlyUnique(value, index, self) { 
		    return self.indexOf(value) === index;
		}

		// A unique list of all the properties any block may have
		var unique_properties = properties.filter( onlyUnique ); // returns ['a', 1, 2, '1']





		// Read the blocks and add to the block list based off their pallet index
		for (var i = 0; i < blocks.length; i++) {
			palette_block_index = blocks[i].state.value
			// palette_count[palette_block_index] += 1

			// Skip air blocks
			if (palette_block_index === air_block_index) continue;

			// Grab the block name
			var block_name = undefined;
			if (blocks[i].nbt !== undefined) {

				// If this is a skull block do special logic to handle skulls which store their data solely in NBT data, grr
				if (blocks[i].nbt.value.id.value === "minecraft:skull") {
					var skull_values = {
						0: "SkeletonSkull",
						1: "WitherSkeletonSkull",
						2: "ZombieSkull",
						3: "PlayerSkull",
						4: "CreeperSkull",
						5: "EnderDragonSkull"
					}

					// If the skull type is not one of the above types throw an error
					if (!(blocks[i].nbt.value.SkullType.value in skull_values)) {
						console.log("Error loading skull type, not a known value!");
						continue;
					}

					// Try to grab the name from the name mapping but if it does not exist throw an error
					var base_name = "minecraft:skull:" + skull_values[blocks[i].nbt.value.SkullType.value];
					block_name = name_mappings[base_name];
					if (block_name === undefined) {
						console.log("Error finding skull type mapping for", base_name)
					}
				}
				// If this is a banner then do special logic to handle banners which also store their data solely in NBT data, also grr
				else if (blocks[i].nbt.value.id.value === "minecraft:banner") {
					// The color values for banners
					var color_values = {
						0: "black",
						1: "red",
						2: "green",
						3: "brown",
						4: "blue",
						5: "purple",
						6: "cyan",
						7: "silver",
						8: "gray",
						9: "pink",
						10: "lime",
						11: "yellow",
						12: "light_blue",
						13: "magenta",
						14: "orange",
						15: "white"
					}

					// If the color is not one of the above throw an error
					if (!(blocks[i].nbt.value.Base.value in color_values)) {
						console.log("Error loading color, not a known value:", blocks[i].nbt.value.Base.value)
						continue;
					}

					// Try to grab the name from the name mapping but if it does not exist throw an error
					var base_name = "minecraft:banner:" + color_values[blocks[i].nbt.value.Base.value];
					block_name = name_mappings[base_name];
					if (block_name === undefined) {
						console.log("Error finding banner type mapping for", base_name);
					}
				}
				// We are just dealing with a regular run of the mill block that happens to have NBT data
				else {
					block_name = palette_map[palette_block_index]
				}
			}
			else {
				block_name = palette_map[palette_block_index]
			}

			if (block_name === undefined) {
				console.log("BLOCK NAME '", block_name,"' IS UNDEFINED, SKIPPING");
				continue;
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

	////////////////////////////////////////////////////////////////////////////
	// Take the block_list and create a resource calculator url from that url
	////////////////////////////////////////////////////////////////////////////
	function display_url(block_list) {
		var outputbox = $("#outputbox");
		item_list = {}


		var block_keys = Object.keys(block_list);
		for (var i = 0; i < block_keys.length; i++) {
			// outputbox.text(outputbox.text() + block_keys[i] + ":" + block_list[block_keys[i]] + "\n")
			// outputbox.innerHTML += block_keys[i] + ":" + block_list[block_keys[i]] + "<br>";

			var block_url_name = block_keys[i].toLowerCase().replace(/[^a-z]/g,'');
			item_list[block_url_name] = block_list[block_keys[i]]
		}

		// outputbox.text();
		outputbox.empty();
		var calculator_link = $('<a/>')
			// .addClass('desired_item_count')
			.attr('href',"/#"+$.param(item_list))
			// .attr('href', '/')
			// .text("Click Here for calculation")
			.addClass('internal_link')
			.text("https://resourcecalculator.com/#" + $.param(item_list))
			// .attr('id', i.toLowerCase().replace(/[^a-z]/g,''))
			// .bind("propertychange change click keyup input paste", function(event){
				// save();
			// })
			.appendTo(outputbox)
	}




	$(window).load(function(){


		// Monitor the file input box and check if it changes, if it does load the new file
		document.getElementById('fileinput').addEventListener('change', parse_nbt_file, false);



		// Add button functionality
		$("#upload_structure").click(function(e){
			e.preventDefault();
			$("#fileinput").trigger('click');
		});

	});




})(jQuery);



