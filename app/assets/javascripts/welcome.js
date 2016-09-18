(function($) {






	$(window).load(function(){
		var global_recepies;
		// Assign handlers immediately after making the request,
		// and remember the jqxhr object for this request
		var jqxhr = $.getJSON( "recipes.json", function(result) {
			// console.log( "success" );

			var content = $("#contentfield");
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
			var cList = $('<ul/>');

			// Fill output
			$.each(raw_resources, function(i) {
				var li = $('<li/>')
					.addClass('desired_item')
					.text(i + ": " + raw_resources[i] )
					.appendTo(cList);
				// var aaa = $('<input/>')
				// 	.addClass('desired_item_count')
				// 	.attr('type','textbox')
				// 	.appendTo(li);
			});

			cList.appendTo(chart);


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



		$("#item_filter").bind("propertychange change click keyup input paste", function(event){
			// // If value has changed...
			// if (elem.data('oldVal') != elem.val()) {
			// // Updated stored value
			// elem.data('oldVal', elem.val());

			var search_string = $(this).val().toLowerCase()


			$("#contentfield").children().each(function(index) {
				// console.log(index)

				var item_name = $(this).attr('mc_value');

				if (item_name.indexOf(search_string) === -1) {
					$(this).hide();
				}
				else {
					$(this).show();
				}

			});




			// Do action
			// ....
		});


		$("#hover_name").hide();


		$(document).on('mousemove', function(e){
		    $('#hover_name').offset	({
		       left:  e.pageX +10,
		       top:   e.pageY -10
		    });
		    console.log("mousemove");
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



