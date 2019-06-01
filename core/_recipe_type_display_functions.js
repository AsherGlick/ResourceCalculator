var recipe_type_functions = {
	{% for recipe_type in recipe_type_format_functions %}
		"{{recipe_type.name}}":function(inputs, output, output_count, text_item_object) {
			var line_wrapper = $("<div/>").addClass("instruction_wrapper");
			var tokenized_inputs = {{recipe_type.tokenized_inputs}};

			// Parse out seperate ingrediants
			var all_other_inputs = [];
			for (var input in inputs) {
				if (tokenized_inputs.indexOf(input) == -1) {
					all_other_inputs.push({"name":input,"quantity":inputs[input]});
				}
			}




			{% for input_chunk in recipe_type.input_chunks %}
				{% if input_chunk.type == "text" %}
					// Raw Text
					$("<span/>").text("{{input_chunk.text}}").appendTo(line_wrapper);
				{% elif input_chunk.type == "all_other_inputs" %}
					// all other inputs:
					for (var input_index = 0; input_index < all_other_inputs.length; input_index++){
						if (input_index > 0 && input_index < all_other_inputs.length-1 && all_other_inputs.length > 2) {
							$("<span/>").text(", ").appendTo(line_wrapper);
						}
						else if (input_index > 0 && input_index == all_other_inputs.length-1 && all_other_inputs.length > 2) {
							$("<span/>").text(", and ").appendTo(line_wrapper);
						}
						else if (input_index > 0 && input_index == all_other_inputs.length-1 && all_other_inputs.length == 2) {
							$("<span/>").text(" and ").appendTo(line_wrapper);
						}
						text_item_object(all_other_inputs[input_index].quantity, all_other_inputs[input_index].name).appendTo(line_wrapper);
					}
				{% elif input_chunk.type == "tokenized_input" %}
					// Tokenized Input
					text_item_object(inputs["{{input_chunk.name}}"], "{{input_chunk.name}}").appendTo(line_wrapper);
				{% elif input_chunk.type == "output" %}
					// Output Text
					text_item_object(output_count, output).appendTo(line_wrapper);
				{% endif %}
			{% endfor %}

			return line_wrapper
		},
	{% endfor %}
};