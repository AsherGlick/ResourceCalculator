(function($) {






	$(window).load(function(){
		var global_recepies;
		// Assign handlers immediately after making the request,
		// and remember the jqxhr object for this request
		var jqxhr = $.getJSON( "recipes.json", function(result) {
			// console.log( "success" );

			var content = $("#content_field");
			// var cList = $('<ul/>');


			$.each(result, function(i)
			{
				var li = $('<div/>')
					.addClass('desired_item')
					.attr("mc_value", i)
					// .attr("mc_value", i.toLowerCase())
					.css('background-image', 'url(items/' + filenameify(i) + '.png)')
					// .text(i)
					.appendTo(content);
				var aaa = $('<input/>')
					.addClass('desired_item_count')
					.attr('type','textbox')
					.appendTo(li);




				li.mouseover( function() {
					$("#hover_name").show();
					$("#hover_name").text(i);
				});

				li.mouseout( function() {
					$("#hover_name").hide();
				})

			/*	if (!result[i]["raw_material"]){
					console.log(result[i]["raw_material"]);
					console.log("Not Raw");
				}*/
				$.each(result[i], function(recipe) {
					// console.log(recipe);
					result[i][recipe]['requirements'] = condence_recepie(result[i][recipe]['recipe']);
				});

				// console.log(result[i]);

			});

			global_recepies = result;
			// cList.appendTo(content);

		})
		.done(function() {
			console.log( "second success" );
		})
		.fail(function() {
			console.log( "error" );
		})
		.always(function() {
			console.log( "complete" );
		});

		// Perform other work here ...

		// Set another completion function for the request above
		jqxhr.complete(function() {
			console.log( "second complete" );
		});	


		function filenameify(rawname) {
			name = rawname.toLowerCase();
			name = name.split(" ").join('_');
			name = name.replace(/[^a-zA-Z0-9_]/g,"");
			// console.log(name);
			return name;
		}

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

		var resource_tracker = {};

		$("#generatelist").click(function() {
			requirements = gather_requirements();

			console.log(requirements);

			raw_resources = {};

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

			// console.log(resource_tracker);

			generate_chart(resource_tracker);

			var chart = $("#item_list");
			chart.empty();
			// var cList = $('<ul/>');

			// Fill output
			$.each(raw_resources, function(i) {
				var li = $('<div/>')
					.addClass('required_item')
					.css('background-image', 'url(items/' + filenameify(i) + '.png)')
					.text(raw_resources[i] )
					.appendTo(chart);
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
				})
			});

			// cList.appendTo(chart);


		});

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

		// Re-filter the items each time the search bar is modified
		$("#item_filter").bind("propertychange change click keyup input paste", function(event){
			filter_items();
		});


		$("#hover_name").hide();

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




		////////////////////////////////////////////////////////////////////////////
		////////////////////////////////////////////////////////////////////////////
		////////////////////////////////////////////////////////////////////////////
		// Flow Chart stuff
		function generate_chart(resource_tracker) {

			var sankey = d3.sankey();
			var margin = {
				top: 1,
				right: 1,
				bottom: 6,
				left: 1
			},
			width = 960 - margin.left - margin.right,
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
				.nodeWidth(15)
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




			for (var key in resource_tracker) {
				var resource = resource_tracker[key];


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
					return d.source.name + " → " + d.target.name + "\n" + format(d.value);
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

			node.append("rect")
				.attr("height", function(d) {
					return d.dy;
				})
				.attr("width", sankey.nodeWidth())
				.style("fill", function(d) {
					return d.color = color(d.name.replace(/ .*/, ""));
				})
				.style("stroke", function(d) {
					return d3.rgb(d.color).darker(2);
				})
				.append("title")
				.text(function(d) {
					return d.name + "\n" + format(d.value);
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
	}); 
})(jQuery);



