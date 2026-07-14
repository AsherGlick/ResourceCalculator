import { set_recipe_index, find_loop_from_node } from "./recipe_info";
import { generatelist } from "./requirements_calculation";

declare var resource_simple_names: {[key: string]: string};
declare var recipe_json: {[key: string]: {output: number, recipe_type: string, requirements: {[key:string]:number}}[]};


////////////////////////////////////////////////////////////////////////////////
// calculator.js handles all of the javascript for the calculator page
////////////////////////////////////////////////////////////////////////////////

/// DOM Gathering ///
const inventory_import_text_elem = <HTMLInputElement>document.getElementById("inventory_import_text");
const hover_name_elem: HTMLElement = document.getElementById("hover_name")!;
const reset_item_count_elem: HTMLElement = document.getElementById("reset_item_count")!;
const hide_unused_checkbox_elem: HTMLInputElement = <HTMLInputElement>document.getElementById("unused_hide_checkbox");
const hide_unused_checkbox_label_elem: HTMLElement = document.getElementById("unused_hide_checkbox_label")!;
const recipe_selector_list_elem = document.getElementById("recipe_selector_list")!;
const recipe_select_elem = document.getElementById("recipe_select")!;
const inventory_amount_input_elem = <HTMLInputElement>document.getElementById("inventory_amount_input");

////////////////////////////////////////////////////////////////////////////////
////////////////////////////// Header Bar Logics ///////////////////////////////
////////////////////////////////////////////////////////////////////////////////

/******************************************************************************\
| "Reset Item Counts" Button Logic                                             |
\******************************************************************************/
function clear_item_counts() {
	if (!confirm("Are you sure you want to clear all items?")) {
		return;
	}

	document.querySelectorAll(".desired_item").forEach((desired_item) => {
		const field = <HTMLInputElement>desired_item.querySelector(".desired_item_count");
		field.value = "";
		set_textbox_background(field);
	});

	// uncheck the hide unused checkbox element
	if (hide_unused_checkbox_elem.checked) {
		hide_unused_checkbox_elem.click();
	}

	generatelist(inventory);
}

reset_item_count_elem.addEventListener("click", clear_item_counts);
inventory_import_text_elem.addEventListener("change", clear_item_counts);

/******************************************************************************\
| "About Us" Button Logic                                                      |
\******************************************************************************/
// $(".inventory_import_export_toggle").click(function() {
// 	$("#inventory_import_export").slideToggle();
// }); // TODO: Re enable when desired

// $("#about_button").click(function() {
// 	$("#about_us").slideToggle();
// }); // TODO: Re enable when desired

// TODO: We should not need to regenerate the calculator every time a stack size
// button is clicked. This is especially visible if the calculator has not yet
// been generated.
document.querySelectorAll("input[name=unit_name]").forEach(function(stack_size_button) {
	stack_size_button.addEventListener("click", function() {
		generatelist(inventory);
	});
});

// Bind events to the item list elements // TODO THIS FUNCTION NEEDS A BETTER COMMENT
function initilize_all_items() {
	document.querySelectorAll(".desired_item").forEach((item) => {
		let item_input_box = <HTMLInputElement>item.querySelector(".desired_item_count");
		let item_label = item_input_box.getAttribute("aria-label")!;

		// When clicking on the box focus the text box
		item.addEventListener("click", function() {
			item_input_box.style.display = "block";
			console.log("showing item");
			item_input_box.focus();
		});

		// Make the item counts save when modified
		item_input_box.addEventListener("propertychange", save);
		item_input_box.addEventListener("change", save);
		item_input_box.addEventListener("click", save);
		item_input_box.addEventListener("keyup", save);
		item_input_box.addEventListener("input", save);
		item_input_box.addEventListener("paste", save);

		// Put an orange border around the item when the text box is focused
		// This makes it more noticeable when an item is selected
		item_input_box.addEventListener("focus", function() {
			item.classList.add("desired_item_input_focused");
			item_input_box.style.backgroundColor = "rgba(0,0,0,.5)";
			item_input_box.select();
		});
		item_input_box.addEventListener("blur", function() {
			item.classList.remove("desired_item_input_focused");
			set_textbox_background(item_input_box);

		});

		// When doubleclicking open the recipe select menu
		item.addEventListener("dblclick", function (event) {
			switch_recipe(item_label, <MouseEvent>event);
			switch_inventory_amount_input(item_label);
		});

		// Enable item name hover text
		item.addEventListener("mouseover", function() {
			hover_name_elem.textContent = item_label;
			hover_name_elem.style.opacity = "1";
		});
		item.addEventListener("mouseout", function() {
			hover_name_elem.style.opacity = "0";
		});
	});
}
initilize_all_items();


/******************************************************************************\
| Search Bar filter logic
\******************************************************************************/
function filter_items() {
	let search_string = item_filter_elem.value.toLowerCase();;
	let hide_unused = hide_unused_checkbox_elem.checked;

	// Loop through each item
	document.querySelectorAll(".desired_item").forEach(function(item) {
		let item_name = item.querySelector("input")!.getAttribute("aria-label")!.toLowerCase();
		let item_count: number = parseInt((<HTMLInputElement>item.querySelector(".desired_item_count")).value);

		// If the search string does not match hide the item
		// If the item count is not greater than 0 and hide unused is true hide
		if (item_name.indexOf(search_string) === -1 || !(item_count > 0 || !hide_unused)) {
			(<HTMLInputElement>item).style.display = "none";
		}
		else {
			(<HTMLInputElement>item).style.display = "block";
		}
	});
}



let item_filter_elem: HTMLInputElement = <HTMLInputElement>document.getElementById("item_filter");
item_filter_elem.addEventListener("change", filter_items);
item_filter_elem.addEventListener("click", filter_items);
item_filter_elem.addEventListener("keyup", filter_items);
item_filter_elem.addEventListener("input", filter_items);
item_filter_elem.addEventListener("paste", filter_items);


/******************************************************************************\
| "Hide Unused" "Show Unused" Button Logic                                     |
\******************************************************************************/
hide_unused_checkbox_elem.addEventListener("change", function() {
	if (this.checked) {
		hide_unused_checkbox_label_elem.textContent = "Show Unused";
	}
	else {
		hide_unused_checkbox_label_elem.textContent = "Hide Unused";
	}
	filter_items();
});


////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////// // TODO THIS FUNCTION NEEDS A BETTER PLACE TO LIVE
////////////////////////////////////////////////////////////////////////////////
function filenameify(rawname: string): string {
	if (rawname === null) {
		return "";
	}
	return rawname.toLowerCase().replace(/[^a-z0=9]/g, "");
}


////////////////////////////////////////////////////////////////////////////////
//////////////////////////////// Save and Load /////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

/******************************************************************************\
| save()                                                                       |
|                                                                              |
| This function saves the current state of the resource requirement list to    |
| the URI hash so that it can be shared with other users or so the page can be |
| refreshed without losing current information.                                |
\******************************************************************************/
function save() {
	let selected_items: {[key: string]: number} = {};

	document.querySelectorAll(".desired_item").forEach(function(item) {
		let key: string = item.querySelector(".desired_item_count")!.id;
		let value: string = (<HTMLInputElement>item.querySelector(".desired_item_count")).value;

		let int_value: number = parseInt(value);
		if (!isNaN(int_value)) {
			selected_items[key] = int_value;
		}
	});
	// TODO: We probably want to do something here with replace state instead of
	// push state if possible.
	if(history.pushState) {
		history.pushState(null, "", "#" + to_url_params(selected_items));
	}
	else {
		window.location.hash = to_url_params(selected_items);
	}

	export_inventory_to_localstorage();
}

function to_url_params(source: {[key: string]: number}): string {
	let array = [];

	for (let key in source) {
		array.push(encodeURIComponent(key) + "=" + encodeURIComponent(source[key]));
	}

	return array.join("&");
}



let inventory: { [key: string]: number} = {};
function export_inventory_to_localstorage() {
	let input = inventory;

	input = remove_null_entries(input);

	input = input ? input : {};
	let calculatorName = window.location.pathname.replace(/\//g, "");

	localStorage.setItem("[" + calculatorName + " Inventory]", JSON.stringify(input));
}

function export_inventory_to_textbox() {
	inventory = remove_null_entries(inventory);
	(<HTMLInputElement>document.getElementById("inventory_import_text")).value = JSON.stringify(inventory ? inventory : {}, null, 1);
}


/******************************************************************************\
| load()                                                                       |
|                                                                              |
| This function is an inverse to save() and reads the state of the resource    |
| requirement list from the URI hash. In addition it will automatically call   |
| generatelist() to save the user from having to click the button for a saved  |
| list.                                                                        |
\******************************************************************************/
function load() {
	import_inventory_from_localstorage();
	export_inventory_to_textbox();

	var uri_arguments = decodeURIComponent(window.location.hash.substr(1));
	if (uri_arguments !== "") {
		var pairs = uri_arguments.split("&");
		for(let i in pairs){
			var split = pairs[i].split("=");
			var id = decodeURIComponent(split[0]);
			var value = decodeURIComponent(split[1]);
			let desired_item = <HTMLInputElement>document.getElementById(id);
			if (desired_item === null) {
				continue;
			}
			desired_item.value = value;
			desired_item.style.display = "block";
			set_textbox_background(desired_item);
		}
		// check the hide unused checkbox
		if (!hide_unused_checkbox_elem.checked) {
			hide_unused_checkbox_elem.click();
		}
		generatelist(inventory);
	}
}

function import_inventory_from_localstorage() {
	let calculatorName = window.location.pathname.replace(/\//g, "");
	let inventoryContent = JSON.parse(localStorage.getItem("[" + calculatorName + " Inventory]") || "{}");
	inventory = remove_null_entries(inventory);
	export_inventory_to_textbox();
	return inventory;
}


const inventory_import_error_elem = document.getElementById("inventory_import_error")!;

function import_inventory_from_textbox(){
	let text: string = inventory_import_text_elem.value;
	if (text.trim().length > 0){
		try {
			inventory = JSON.parse(text);
			inventory_import_error_elem.classList.add("hidden");
		}
		catch (exception) {
			inventory_import_error_elem.classList.remove("hidden");
		}
	}
	else {
		inventory = {};
		inventory_import_error_elem.classList.add("hidden");
	}

	inventory = remove_null_entries(inventory);
	export_inventory_to_localstorage();
}



function remove_null_entries<T>(item_collection: {[key: string]:T}): {[key: string]:T}{
	for (let item_name in item_collection) {
		if (!item_collection[item_name]){
			delete item_collection[item_name];
		}
	}
	return item_collection;
}

const generate_list_button_elem = document.getElementById("generatelist")!;
generate_list_button_elem.addEventListener("click", ()=>{generatelist(inventory)});


////////////////////////////////////////////////////////////////////////////////
/////////////////////////////// Hover Text Logic ///////////////////////////////
////////////////////////////////////////////////////////////////////////////////
// How far away from the mouse should the hoverbox be
let hover_x_offset: number = 10;
let hover_y_offset: number = -10;

document.addEventListener("mousemove", function(e: MouseEvent){
	// If the hoverbox is not hanging over the side of the screen when rendered, render normally
	if (window.innerWidth > hover_name_elem.offsetWidth + e.pageX + hover_x_offset) {
		hover_name_elem.style.left = (e.pageX + hover_x_offset).toString() + "px";
		hover_name_elem.style.top = (e.pageY + hover_y_offset).toString() + "px";
	}
	// If the hoverbox is hanging over the side of the screen then render on the other side of the mouse
	else {
		hover_name_elem.style.left = (e.pageX - hover_x_offset - hover_name_elem.offsetWidth).toString() + "px";
		hover_name_elem.style.top = (e.pageY + hover_y_offset).toString() + "px";
	}
});


////////////////////////////////////////////////////////////////////////////////
////////////////////////////// Hover Recipe Logic //////////////////////////////
////////////////////////////////////////////////////////////////////////////////
// function set_recipe (target, source, source_quantity) {
// 	var recipe = get_recipe(target);

// 	var source_item_count = -recipe.requirements[source];
// 	var item_multiplier = source_quantity / source_item_count;

// 	if (recipe.recipe_type === "crafting") {

// 		for (let i in recipe.recipe) {
// 			$("#crafting_slot_"+i).removeClass (function (index, className) {
// 				return (className.match (/\bitem_[a-z0-9_]*/) || []).join(" ");
// 			}).addClass("item_" + filenameify(recipe.recipe[i]));

// 			if (item_multiplier > 1 && recipe.recipe[i] !== null) {
// 				$("#crafting_slot_"+i).text(item_multiplier);
// 			}
// 			else {
// 				$("#crafting_slot_"+i).text("");
// 			}
// 		}
// 		$("#crafting_output_image").removeClass (function (index, className) {
// 			return (className.match (/\bitem_[a-z0-9_]*/) || []).join(" ");
// 		}).addClass("item_" + filenameify(target));

// 		if (recipe.output * item_multiplier > 1){
// 			$("#crafting_output_image").text(recipe.output * item_multiplier);
// 		}
// 		else {
// 			$("#crafting_output_image").text("");
// 		}
// 	}
// 	else {
// 		console.error("The recipe type for " + target + " has not been created yet");
// 	}
// }

// $(document).on("mousemove", function(e) {


// 	var left_offset = e.pageX + hover_x_offset;
// 	var top_offset = e.pageY + hover_y_offset;

// 	if ($(window).width() < $("#hover_recipe").outerWidth() + e.pageX + hover_x_offset ) {
// 		left_offset = e.pageX - hover_x_offset - $("#hover_recipe").outerWidth();
// 	}

// 	if ($(window).height() + $(document).scrollTop() < $("#hover_recipe").outerHeight() + e.pageY + hover_y_offset ) {
// 		top_offset = e.pageY - hover_y_offset - $("#hover_recipe").outerHeight();
// 	}

// 	$("#hover_recipe").offset ({
// 		left:  left_offset,
// 		top:   top_offset,
// 	});
// });



////////////////////////////////////////////////////////////////////////////////
/////////////////////////////// Recipe Switching ///////////////////////////////
////////////////////////////////////////////////////////////////////////////////


/******************************************************************************\
|
\******************************************************************************/
function switch_recipe(item_name: string, event: MouseEvent) {
	var recipe_selector = recipe_select_elem;

	// Clear the recipe selector list
	while (recipe_selector_list_elem.lastChild) {
		recipe_selector_list_elem.removeChild(recipe_selector_list_elem.lastChild);
	}

	for (let i = 0; i < recipe_json[item_name].length; i++) {
		var recipe_item = document.createElement("div");
		recipe_item.classList.add("recipe_select_item");

		recipe_item.addEventListener("click", (function(index: number) {
			return function() {
				set_recipe_index(item_name, index);
				find_loop_from_node(item_name);
				recipe_selector.style.opacity = "0";
				recipe_selector.style.pointerEvents = "none";
			};
		})(i));

		let recipe_category = document.createElement("div");
		recipe_category.classList.add("recipe_select_item_name");
		recipe_category.textContent = recipe_json[item_name][i].recipe_type;

		for (let j in recipe_json[item_name][i].requirements) {
			(function(j) {

				let quantity = -recipe_json[item_name][i].requirements[j];

				let item_elem = document.createElement("div");
				item_elem.classList.add("required_item");
				item_elem.classList.add("item");
				item_elem.classList.add("item_" + (resource_simple_names[j] ? resource_simple_names[j] : filenameify(j)));
				item_elem.textContent = quantity.toString();
				recipe_category.appendChild(item_elem);

				item_elem.addEventListener("mouseover", function() {
					hover_name_elem.textContent = quantity + "x " + j;
					hover_name_elem.style.opacity = "1";
				});
				item_elem.addEventListener("mouseout", function() {
					hover_name_elem.style.opacity = "0";
				});
			})(j);
		}
		recipe_item.appendChild(recipe_category);

		let clear_div = document.createElement("div");
		clear_div.classList.add("clear");
		recipe_item.appendChild(clear_div)

		recipe_selector_list_elem.appendChild(recipe_item);
	}

	recipe_selector.style.opacity = "1";
	recipe_selector.style.pointerEvents = "auto";



	var menu_x_offset = -10;
	var menu_y_offset = -10;

	var left_offset = event.pageX + menu_x_offset;
	var top_offset = event.pageY + menu_y_offset;

	if (window.innerWidth < recipe_selector.offsetWidth + event.pageX + menu_x_offset) {
		left_offset = event.pageX - menu_x_offset - recipe_selector.offsetWidth;
	}


	if (window.innerHeight + window.pageYOffset < recipe_selector.offsetHeight + event.pageY + menu_y_offset && event.pageY - menu_y_offset - recipe_selector.offsetHeight >= 0) {
		top_offset = event.pageY - menu_y_offset - recipe_selector.offsetHeight;
	}

	recipe_selector.style.top = top_offset.toString() + "px";
	recipe_selector.style.left = left_offset.toString() + "px";
}

function switch_inventory_amount_input(item_name: string) {
	inventory_amount_input_elem.setAttribute("item_name", item_name); //???
	if (inventory[item_name] === undefined) {
		inventory_amount_input_elem.value = "0";
	} else {
		inventory_amount_input_elem.value = inventory[item_name].toString();
	}
}

recipe_select_elem.addEventListener("mouseleave", function() {
	recipe_select_elem.style.opacity = "0";
	recipe_select_elem.style.pointerEvents = "none";
});


inventory_amount_input_elem.addEventListener("change", function(){
	let item_name = inventory_amount_input_elem.getAttribute("item_name");
	if (item_name === null) {
		// TODO: create a nicer method of identification where this can never
		// be true. Some sort of closure that has this value set already.
		console.error("No actively selected item name");
	}
	else {
		inventory[item_name] = parseInt(inventory_amount_input_elem.value);
		export_inventory_to_localstorage();
		export_inventory_to_textbox();
	}
});

inventory_amount_input_elem.addEventListener("focus", function() {
	this.select();
});

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

// TODO: This seems very related to the function loop at the top that is not
// well commented, see if we can combine these two things together in a
// reasonable way. Or split up the other loop to be like this one
/******************************************************************************\
| set_textbox_background                                                       |
|                                                                              |
| This function darkens the background of a textbox based on if the box has    |
| any text in it. It is paired with a focus and blur trigger that causes the   |
| background to go dark when clicked, and only go light again when the text    |
| box is blank.                                                                |
\******************************************************************************/
function set_textbox_background(textbox: HTMLInputElement){
	if (textbox.value === ""){
		textbox.style.backgroundColor = "rgba(0,0,0,0)";
	}
	else {
		textbox.style.backgroundColor = "rgba(0,0,0,.5)";
	}
}



// Run the load function to load arguments from the URL if they exist
load();
