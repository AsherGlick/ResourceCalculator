////////////////////////////////////////////////////////////////////////////////
// calculator.js handles all of the javascript for the calculator page
////////////////////////////////////////////////////////////////////////////////

(function($) {
	"use strict";
	$(window).on("load", function(){

		// Assign event handlers
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


		$("#about_button").click(function() {
			$("#about_us").slideToggle();
		});

		// Bind events to the item list elements
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


		function filenameify(rawname) {
			if (rawname === null) {
				return "";
			}
			return rawname.toLowerCase().replace(/[^a-z]/g, "");
		}

		// This function changes the url hash whenever an item is added or removed
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
		// This function should only be called once on pageload and after the item elements are created
		// loads the url into the item list then generates the results
		function load() {
			var uri_arguments = decodeURIComponent(window.location.hash.substr(1));
			if (uri_arguments !== "") {
				var pairs = uri_arguments.split("&");
				for(var i in pairs){
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
			for (var requirement in requirements){
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
				for (var requirement in requirements){
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

			for (var original_requirement in original_requirements) {
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
			for (var key in output_requirements) {
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
			for (var tracked_resource in resource_tracker_copy) {
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
			generate_instructions(resource_tracker);
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

		function generate_instructions(generation_events) {
			return generation_events;
		}

		/******************************************************************************\
		| generate_chart                                                               |
		|                                                                              |
		| This function is in charge of drawing the sankey chart onto the canvas       |
		|
		| Arguments
		|   generation_events -
		\******************************************************************************/
		function generate_chart(generation_events, resource_totals) {
			var margin = {
				top: 10,
				right: 1,
				bottom: 10,
				left: 1,
			};
			var width = $("#content").width() - margin.left - margin.right;
			var height = 800 - margin.top - margin.bottom;
			var color = d3.scaleOrdinal(d3.schemeCategory20);

			// Clear any old elements in the chart area
			$("#chart").empty();

			// Create the new SVG image that will contain the sankey graph
			var svg = d3.select("#chart").append("svg")
				.attr("width", width + margin.left + margin.right)
				.attr("height", height + margin.top + margin.bottom)
				.append("g")
				.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

			var sankey = d3.sankey()
				.nodeWidth(20)
				.nodePadding(10)
				.size([width, height]);

			var path = sankey.link();

			// d3.json("energy.json", function(energy) {

			// Need piston
			// 0: make sure this exists
			// 1: make sure all of the sources exist
			// 2: mapping

			// Add mapping to and from and the quantity for each element
			// "tofrom":{"source":"from","target":"to","value":1}



			var nodes = [];
			var inverted_nodes = {};
			var links = [];




			for (var key in generation_events) {
				var resource = generation_events[key];


				var source = resource.source;
				var target = resource.target;

				var value = resource.value;


				var source_index;
				if (source in inverted_nodes) {
					source_index = inverted_nodes[source];
				}
				else {
					source_index = nodes.length;
					nodes.push({"name":source});
					inverted_nodes[source] = source_index;
				}

				var target_index;
				if (target in inverted_nodes) {
					target_index = inverted_nodes[target];
				}
				else {
					target_index = nodes.length;
					nodes.push({"name":target});
					inverted_nodes[target] = target_index;
				}

				links.push({
					"source":source_index,
					"target":target_index,
					"value":value,
				});


			}


			var energy = {
				"nodes":nodes,
				"links":links,
			};

			sankey
				.nodes(energy.nodes)
				.links(energy.links)
				.layout(32);

			var link = svg.append("g").selectAll(".link")
				.data(energy.links)
				.enter().append("path")
				.attr("class", "link")
				.attr("d", path)
				.attr("rcalc:source", function(d) {
					return d.source.name;
				})
				.attr("rcalc:target", function(d) {
					return d.target.name;
				})
				.attr("rcalc:quantity", function(d) {
					return d.value;
				})
				.style("stroke-width", function(d) {
					return Math.max(1, d.dy);
				})
				.sort(function(a, b) {
					return b.dy - a.dy;
				})
				.on("mouseover", function() {
					$("#hover_recipe").show();
					set_recipe($(this).attr("target"), $(this).attr("source"), $(this).attr("quantity"));
				})
				.on("mouseout", function() {
					$("#hover_recipe").hide();
				});

			var node = svg.append("g").selectAll(".node")
				.data(energy.nodes)
				.enter().append("g")
				.attr("class", "node")
				.attr("transform", function(d) {
					return "translate(" + d.x + "," + d.y + ")";
				})
				.call(d3.drag()
					.subject(function(d) {
						return d;
					})
					.on("start", function() {
						this.parentNode.appendChild(this);
					})
					.on("drag", dragmove));



			node.append("path")
				.attr("d", function(d) {



					var left_count = 0; // sum target links
					for (var target_link in d.targetLinks) {
						left_count += d.targetLinks[target_link].value;
					}
					// If this is the first element make it the full height
					if (left_count === 0) {
						left_count = d.value;
					}

					var right_count = 0; // sum source links
					for (var source_link in d.sourceLinks) {
						right_count += d.sourceLinks[source_link].value;
					}
					// If this is the last element make it the full height
					if (right_count === 0) {
						right_count = d.value;
					}



					var left_height = d.dy * (left_count / d.value);
					var full_height = d.dy;
					var right_height = d.dy * (right_count / d.value);
					var width = d.dx;
					return "M 0,0 L 0,"+left_height+" "+width/3+","+left_height+" "+width/3+","+full_height+" "+width*2/3+","+full_height+" "+width*2/3+","+right_height+" "+width+","+right_height+" "+width+",0 Z";
				})
				.style("fill", function(d) {
					return d.color = color(d.name.replace(/ .*/, ""));
				})
				.style("stroke", function(d) {
					return d3.rgb(d.color).darker(2);
				})
				.append("title")
				.text(function(d) {
					// console.log(d);
					// return d.name + "\n" + format(d.value);
					return resource_totals[d.name] + " " + d.name;
				});


			node.append("text")
				.attr("x", -6)
				.attr("y", function(d) {
					return d.dy / 2;
				})
				.attr("dy", ".35em")
				.attr("text-anchor", "end")
				.attr("transform", null)
				.text(function(d) {
					if (d.name.startsWith("[Final]")){
						return d.name.substr(8);
					}
					else {
						return d.name;
					}
				})
				.filter(function(d) {
					return d.x < width / 2;
				})
				.attr("x", 6 + sankey.nodeWidth())
				.attr("text-anchor", "start");

			function dragmove(d) {
				d3.select(this).attr("transform", "translate(" + d.x + "," + (d.y = Math.max(0, Math.min(height - d.dy, d3.event.y))) + ")");
				sankey.relayout();
				link.attr("d", path);
			}
		}




		////////////////////////////////////////////////////////////////////////////////
		////////////////////////////// Item Filter Logic ///////////////////////////////
		////////////////////////////////////////////////////////////////////////////////
		/******************************************************************************\
		|
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

		// Re-filter the items each time the search bar is modified
		$("#item_filter").bind("propertychange change click keyup input paste", function(){
			filter_items();
		});

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
		function set_recipe (target, source, source_quantity) {
			var recipe = get_recipe(target);

			var source_item_count = -recipe.requirements[source];
			var item_multiplier = source_quantity / source_item_count;

			if (recipe.recipe_type === "crafting") {

				for (var i in recipe.recipe) {
					$("#crafting_slot_"+i).removeClass (function (index, className) {
						return (className.match (/\bitem_[a-z0-9_]*/) || []).join(" ");
					}).addClass("item_" + filenameify(recipe.recipe[i]));

					if (item_multiplier > 1 && recipe.recipe[i] !== null) {
						$("#crafting_slot_"+i).text(item_multiplier);
					}
					else {
						$("#crafting_slot_"+i).text("");
					}
				}
				$("#crafting_output_image").removeClass (function (index, className) {
					return (className.match (/\bitem_[a-z0-9_]*/) || []).join(" ");
				}).addClass("item_" + filenameify(target));

				if (recipe.output * item_multiplier > 1){
					$("#crafting_output_image").text(recipe.output * item_multiplier);
				}
				else {
					$("#crafting_output_image").text("");
				}
			}
			else {
				console.error("The recipe type for " + target + " has not been created yet");
			}
		}

		$(document).on("mousemove", function(e) {


			var left_offset = e.pageX + hover_x_offset;
			var top_offset = e.pageY + hover_y_offset;

			if ($(window).width() < $("#hover_recipe").outerWidth() + e.pageX + hover_x_offset ) {
				left_offset = e.pageX - hover_x_offset - $("#hover_recipe").outerWidth();
			}

			if ($(window).height() + $(document).scrollTop() < $("#hover_recipe").outerHeight() + e.pageY + hover_y_offset ) {
				top_offset = e.pageY - hover_y_offset - $("#hover_recipe").outerHeight();
			}

			$("#hover_recipe").offset ({
				left:  left_offset,
				top:   top_offset,
			});
		});









		/******************************************************************************\
		|
		\******************************************************************************/
		function switch_recipe(item_name, event) {
			var recipe_selector = $("#recipe_select");
			var recipe_selector_list = $("#recipe_selector_list");
			recipe_selector_list.empty();

			for (var i in recipe_json[item_name]) {
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

				for (var j in recipe_json[item_name][i].requirements) {
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

			for (var i in recipe_json[node_name]){
				if (recipe_json[node_name][i].recipe_type === "raw_resource"){
					set_recipe_index(node_name, i);
					return;
				}
			}
			alert("ERROR SETTING RAW RESOURCE RECIPE");
		}



		function get_recipe(node_name) {
			return recipe_json[node_name][get_recipe_index(node_name)];
		}

		function find_loop_from_node(start_node) {
			// Generate Light Node Mapping
			var nodes = {};
			for (var node in recipe_json)  {
				// Add all the edges
				nodes[node] = [];
				for (var edge in get_recipe(node).requirements) {
					// console.log(get_recipe(node).requirements[edge]);
					if (-get_recipe(node).requirements[edge] > 0) {
						nodes[node].push(edge);
					}
				}
			}

			//Depth First search
			var recipe_changes = depth_first_search(nodes, start_node, start_node);


			for (var i in recipe_changes){
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
			for (var i in nodes[node]) {
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
	});
})(jQuery);
