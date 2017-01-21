//= require d3.v4.min.js
//= require sankey.js


(function($) {






	$(window).load(function(){
		var global_recepies;




		// Assign event handlers
		$("#unused_hide_checkbox").change(function() {
			if ($(this).prop('checked')) {
				var label = $("label[for='"+$(this).attr('id')+"']");
				label.text("Show Unused");
			}
			else {
				var label = $("label[for='"+$(this).attr('id')+"']");
				label.text("Hide Unused");
			}
			filter_items()
		});



		// Create the recipe list
		var content = $("#content_field");
		$.each(recipe_json, function(i)
		{
			var li = $('<div/>')
				.addClass('desired_item')
				.addClass('item_' + filenameify(i))
				.attr("mc_value", i)
				// .attr("mc_value", i.toLowerCase())
				// .text(i)
				.appendTo(content);
			var aaa = $('<input/>')
				.addClass('desired_item_count')
				.attr('type','number')
				.attr('id', i.toLowerCase().replace(/[^a-z]/g,''))
				.bind("propertychange change click keyup input paste", function(event){
					save();
				})
				.focus(function() {
					li.addClass("item_input_focused")
				})
				.blur(function() {
					li.removeClass("item_input_focused")
				})
				.appendTo(li);


			li.click(function() {
				aaa.focus();
			});




			li.mouseover( function() {
				$("#hover_name").show();
				$("#hover_name").text(i);
			});

			li.mouseout( function() {
				$("#hover_name").hide();
			})

			// Build unformatted recipe requirements for each recipe in the list
			$.each(recipe_json[i], function(recipe) {
				recipe_json[i][recipe]['requirements'] = condence_recepie(recipe_json[i][recipe]['recipe']);
			});
		});

		global_recepies = recipe_json;


		// Run the load function to load arguments from the URL if they exist
		load();


		function filenameify(rawname) {
			name = rawname.toLowerCase();
			name = name.split(" ").join('_');
			name = name.replace(/[^a-zA-Z0-9_]/g,"");
			// console.log(name);
			return name;
		}

		// This function changes the url hash whenever an item is added or removed
		function save() {
			var selected_items = {};
			$(".desired_item").each(function() {
				var key = $(this).find(".desired_item_count").attr('id');
				// console.log(key);
				var value = $(this).find(".desired_item_count").val();

				if ($.isNumeric(value)) {
					// Set the value as negative to indicate they are needed
					selected_items[key] = value;
				}

			});
			// console.log($.param(selected_items));
			window.location.hash = $.param(selected_items);
		}
		// This function should only be called once on pageload and after the item elements are created
		// loads the url into the item list then generates the results
		function load() {
			var arguments = decodeURIComponent(window.location.hash.substr(1));
			// console.log("Loading");
			// console.log(arguments);
			// var obj = {};
			if (arguments !== "") {
				var pairs = arguments.split('&');
				for(i in pairs){
					var split = pairs[i].split('=');
					var id = decodeURIComponent(split[0]);
					var value = decodeURIComponent(split[1]);
					$("#"+id).val(value);
					console.log($("#andesite"));

				}
				$("#unused_hide_checkbox").prop("checked", true).change();
				// filter_items();
				generatelist();

			}
		}


		  //////////////////////////////////////////////////////////////////////////////
		 /////////////////////// Requirements Calculation Logic /////////////////////// 
		//////////////////////////////////////////////////////////////////////////////  
		$("#generatelist").click(generatelist);


		function generatelist() {
			requirements = gather_requirements();

			console.log(requirements);
			var resource_tracker = {};
			var generation_totals = {}; // the total number of each resource produce (ignoring any consumption)

			var raw_resources = {};
			for (var i = 0; i < 50; i++) {
				var output_requirements = JSON.parse(JSON.stringify(requirements));

				$.each(requirements, function(requirement) {
					if (requirements[requirement] < 0) {


						console.log(requirement);
						var recipe = global_recepies[requirement][0]['requirements'];
						var produces_count = global_recepies[requirement][0]['output'];
						var required_count = -requirements[requirement];

						var produce_count = Math.ceil(required_count/produces_count);
						console.log(produce_count);

						// console.log(produce_count);

						output_requirements[requirement] += produce_count * produces_count;

						if (!(requirement in generation_totals)) {
							generation_totals[requirement] = 0;
						}

						generation_totals[requirement] += produce_count * produces_count;
						console.log(recipe); 

						if ($.isEmptyObject(recipe)) {
							if (raw_resources[requirement] == undefined) {
								raw_resources[requirement] = 0;
							}
							raw_resources[requirement] += produce_count * produces_count;
						}

						else {
							$.each(recipe, function(item) {
								if (output_requirements[item] == undefined) {
									output_requirements[item] = 0;
								}
								output_requirements[item] += recipe[item] * produce_count;

								// Log the transaction
								// console.log( requirement + "<=" + item + "(" + recipe[item] * -produce_count + ")" );


								//Key
								var tracker_key = requirement+item;
								if (!(tracker_key in resource_tracker)) {
									resource_tracker[tracker_key] = {
										"source":item,
										"target":requirement,
										"value":0
									}
								}
								resource_tracker[tracker_key]["value"] += recipe[item] * -produce_count
							});
						}
					}
				});

				console.log(output_requirements);
				requirements = output_requirements;
			}

			// This mapps all extra items to an extra value
			// It is done in order to get the right heights for items that produce more then they take
			// TODO, it might be nice to have a special path instead of a node to represent "extra"
			for (var key in output_requirements) {
				if (output_requirements[key] > 0) {
					var tracker_key = key+"extra";
					resource_tracker[tracker_key] = {
						"source":key,
						"target":"extra",
						"value":output_requirements[key]
					}
				}
			}

			// console.log(resource_tracker);

			generate_chart(resource_tracker, generation_totals);

			generate_chest_list(raw_resources);

			generate_instructions(resource_tracker);


			function generate_chest_list(raw_resources){
				var chart = $("#item_list");
				chart.empty();
				// var cList = $('<ul/>');





				var chest;

				var items_in_chest = 0;

				// Fill output
				$.each(raw_resources, function(i) {

					function add_item(item_name, item_count) {
						if (items_in_chest === 0) {
							chest = $('<div/>');
							chest.addClass("chest_list");
							var title = $('<div/>');
							title.appendTo(chest);
							title.addClass('chest_list_title');
							title.text("Large Chest");
							chest.appendTo(chart);
						}
						var li = $('<div/>')
							.addClass('required_item')
							.addClass('item_' + filenameify(item_name))
							.text(item_count)
							.appendTo(chest);
						// var aaa = $('<input/>')
						// 	.addClass('desired_item_count')
						// 	.attr('type','textbox')
						// 	.appendTo(li);

						li.mouseover( function() {
							$("#hover_name").show();
							$("#hover_name").text(i);
						});

						li.mouseout( function() {
							$("#hover_name").hide();
						});

						items_in_chest += 1;
						if (items_in_chest >= 6 * 9) {
							items_in_chest = 0;
						}
					}


					var count = raw_resources[i];
					while (count > 64) {
						add_item(i, 64);
						count -= 64
					}
					if (count > 0) {
						add_item(i,count);
					}
				});
				for (var i = 0; i < 9 * 6 - items_in_chest; i++) {
					var li = $('<div/>')
						.addClass('required_item')
						// .css('background-image', 'url(items/' + filenameify(item_name) + '.png)')
						// .text(item_count)
						.appendTo(chest);
				}
			}

			// cList.appendTo(chart);


		};

		function craft_requirements(requirements) {
			return output_requirements;
		}


		function condence_recepie(recipe) {
			var hash = {};
			for (var i = 0; i< recipe.length; i++) {

				if (recipe[i] == null) {
					continue;
				}
				if (hash[recipe[i]] == undefined) {
					hash[recipe[i]] = 0;
				}
				hash[recipe[i]] -= 1;
			}
			return hash;
		}


		function gather_requirements() {
			var resources = {};
			$(".desired_item").each(function() {
				var key = $(this).attr("mc_value");
				console.log(key);
				var value = $(this).find(".desired_item_count").val();

				if ($.isNumeric(value)) {
					// Set the value as negative to indicate they are needed
					resources[key] = -value;
				}

			});
			return resources;
		}



		  //////////////////////////////////////////////////////////////////////////////
		 ///////////////////////////// Item Filter Logic ////////////////////////////// 
		//////////////////////////////////////////////////////////////////////////////  

		// Re-filter the items each time the search bar is modified
		$("#item_filter").bind("propertychange change click keyup input paste", function(event){
			filter_items();
		});

		function filter_items() {
			var search_string = $("#item_filter").val().toLowerCase()
			var hide_unused = $("#unused_hide_checkbox").prop('checked');

			// Loop through each item
			$("#content_field").find(".desired_item").each(function(index) {
				var item_name = $(this).attr('mc_value').toLowerCase();
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




		  //////////////////////////////////////////////////////////////////////////////
		 ////////////////////////////// Hover Text Logic ////////////////////////////// 
		//////////////////////////////////////////////////////////////////////////////  
		// How far away from the mouse should hte hoverbox be
		var hover_x_offset = 10;
		var hover_y_offset = -10;
		$(document).on('mousemove', function(e){

			// If the hoverbox is not hanging over the side of the screen when rendered, render normally
			if ($(window).width() > $('#hover_name').outerWidth() + e.pageX + hover_x_offset) {

				$('#hover_name').offset	({
					 left:  e.pageX + hover_x_offset,
					 top:   e.pageY + hover_y_offset
				});
			}
			// If the hoverbox is hanging over the side of the screen then render on the other side of the mouse
			else {

				$('#hover_name').offset	({
					left:  e.pageX - hover_x_offset - $('#hover_name').outerWidth(),
					top:   e.pageY + hover_y_offset
				});
			}
		});


		function generate_instructions(generation_events) {

		}

		/******************************* Generate Chart *******************************\
		| This functoin takes in the resources list and generates a graphical chart    |
		| that is displayed to the user                                                |
		\******************************************************************************/
		function generate_chart(generation_events, resource_totals) {

			console.log(resource_totals);

			var sankey = d3.sankey();
			var margin = {
				top: 1,
				right: 1,
				bottom: 6,
				left: 1
			},



			width = $('body').width() - margin.left - margin.right,
			height = 500 - margin.top - margin.bottom;

			var formatNumber = d3.format(",.0f"),
				format = function(d) {
					return formatNumber(d) + " TWh";
				},
				color = d3.scaleOrdinal(d3.schemeCategory20);

			$("#chart").empty();

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


				var source = resource["source"];
				var target = resource["target"];

				var value = resource["value"];


				var source_index;
				if (source in inverted_nodes) {
					source_index = inverted_nodes[source];
				}
				else {
					source_index = nodes.length;
					nodes.push({"name":source});
					inverted_nodes[source] = source_index
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
					"value":value
				})


			}


			var energy = {
				"nodes":nodes,
				"links":links
			}

			sankey
				.nodes(energy.nodes)
				.links(energy.links)
				.layout(32);

			var link = svg.append("g").selectAll(".link")
				.data(energy.links)
				.enter().append("path")
				.attr("class", "link")
				.attr("d", path)
				.style("stroke-width", function(d) {
					return Math.max(1, d.dy);
				})
				.sort(function(a, b) {
					return b.dy - a.dy;
				});

			link.append("title")
				.text(function(d) {
					return d.value +" " + d.source.name + " → " + d.target.name;
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
					if (left_count === 0) {left_count = d.value};

					var right_count = 0; // sum source links
					for (var source_link in d.sourceLinks) {
						right_count += d.sourceLinks[source_link].value;
					}
					// If this is the last element make it the full height
					if (right_count === 0) {right_count = d.value};



					var left_height = d.dy * (left_count / d.value);
					var full_height = d.dy;
					var right_height = d.dy * (right_count / d.value);
					var width = d.dx;
					return "M 0,0 L 0,"+left_height+" "+width/3+","+left_height+" "+width/3+","+full_height+" "+width*2/3+","+full_height+" "+width*2/3+","+right_height+" "+width+","+right_height+" "+width+",0 Z"
				})
				.style("fill", function(d) {
					return d.color = color(d.name.replace(/ .*/, ""));
				})
				.style("stroke", function(d) {
					return d3.rgb(d.color).darker(2);
				})
				.append("title")
				.text(function(d) {
					console.log(d);
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
					return d.name;
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

		// About us lightbox
		$('#about_us_lightbox').click(function (evt) {
			evt.stopPropagation();
		});
		$("#about_us_lightbox_background").click(function(evt) {
			$(this).hide();
		});
		$("#about_us_button").click(function(evt) {
			$("#about_us_lightbox_background").show();
		});

	}); 
})(jQuery);



