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

				console.log(result[i]);

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
			console.log(name);
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
							});
						}
					}
				});

				console.log(output_requirements);
				requirements = output_requirements;
			}



			var chart = $("#chart");
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




		// keyup(function() {
		// 	console.log($(this).val());
		// })


	}); 






// Requires []
// Feeds []



// Parents
// - request item type
// Children
// - quantity



})(jQuery);



