var recipe_type_functions = {
	{% for recipe_type in recipe_type_format_functions %}
		"{{recipe_type.name}}":function(inputs, output, output_count, text_item_object) {
			var line_wrapper = document.createElement("div");
			line_wrapper.classList.add("instruction_wrapper");
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
					{
						// Raw Text
						let input_chunk_text = document.createElement("span");
						input_chunk_text.textContent = "{{input_chunk.text}}";
						line_wrapper.appendChild(input_chunk_text);
					}

				{% elif input_chunk.type == "all_other_inputs" %}
					// all other inputs:
					for (var input_index = 0; input_index < all_other_inputs.length; input_index++){
						if (input_index > 0 && input_index < all_other_inputs.length-1 && all_other_inputs.length > 2) {
							let comma_span = document.createElement("span");
							comma_span.textContent = ", ";
							line_wrapper.appendChild(comma_span);
						}
						else if (input_index > 0 && input_index == all_other_inputs.length-1 && all_other_inputs.length > 2) {
							let final_and = document.createElement("span");
							final_and.textContent = ", and ";
							line_wrapper.appendChild(final_and);
						}
						else if (input_index > 0 && input_index == all_other_inputs.length-1 && all_other_inputs.length == 2) {
							let middle_and = document.createElement("span");
							middle_and.textContent = " and ";
							line_wrapper.appendChild(middle_and);
						}
						line_wrapper.appendChild(text_item_object(all_other_inputs[input_index].quantity, all_other_inputs[input_index].name));
					}
				{% elif input_chunk.type == "tokenized_input" %}
					// Tokenized Input
					line_wrapper.appendChild(text_item_object(inputs["{{input_chunk.name}}"], "{{input_chunk.name}}"));
				{% elif input_chunk.type == "output" %}
					// Output Text
					line_wrapper.appendChild(text_item_object(output_count, output));
				{% endif %}
			{% endfor %}

			return line_wrapper
		},
	{% endfor %}
};