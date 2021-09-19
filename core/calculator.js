"use strict";
var __values = (this && this.__values) || function(o) {
    var s = typeof Symbol === "function" && Symbol.iterator, m = s && o[s], i = 0;
    if (m) return m.call(o);
    if (o && typeof o.length === "number") return {
        next: function () {
            if (o && i >= o.length) o = void 0;
            return { value: o && o[i++], done: !o };
        }
    };
    throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
};
if (!String.prototype.endsWith) {
    String.prototype.endsWith = function (searchString, endPosition) {
        if (endPosition === undefined || endPosition > this.length) {
            endPosition = this.length;
        }
        return this.substring(endPosition - searchString.length, endPosition) === searchString;
    };
}
if (!String.prototype.startsWith) {
    String.prototype.startsWith = function (searchString, startPosition) {
        if (startPosition === undefined || startPosition <= 0) {
            startPosition = 0;
        }
        return this.substring(startPosition, startPosition + searchString.length) === searchString;
    };
}
////////////////////////////////////////////////////////////////////////////////
// calculator.js handles all of the javascript for the calculator page
////////////////////////////////////////////////////////////////////////////////
// Closure wrapper for the script file
(function () {
    "use strict";
    // Closure wrapper for the script file
    /// DOM Gathering ///
    var inventory_import_text_elem = document.getElementById("inventory_import_text");
    var hover_name_elem = document.getElementById("hover_name");
    var reset_item_count_elem = document.getElementById("reset_item_count");
    var text_instructions_elem = document.getElementById("text_instructions");
    var hide_unused_checkbox_elem = document.getElementById("unused_hide_checkbox");
    var hide_unused_checkbox_label_elem = document.getElementById("unused_hide_checkbox_label");
    var recipe_selector_list_elem = document.getElementById("recipe_selector_list");
    var recipe_select_elem = document.getElementById("recipe_select");
    ////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////// Header Bar Logics ///////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////
    /******************************************************************************\
    | "Reset Item Counts" Button Logic                                             |
    \******************************************************************************/
    function clear_item_counts() {
        document.querySelectorAll(".desired_item").forEach(function (desired_item) {
            var field = desired_item.querySelector(".desired_item_count");
            field.value = "";
            set_textbox_background(field);
        });
        // uncheck the hide unused checkbox element
        if (hide_unused_checkbox_elem.checked) {
            hide_unused_checkbox_elem.click();
        }
        generatelist();
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
    document.querySelectorAll("input[name=unit_name]").forEach(function (stack_size_button) {
        stack_size_button.addEventListener("click", function () {
            generatelist();
        });
    });
    // Bind events to the item list elements // TODO THIS FUNCTION NEEDS A BETTER COMMENT
    function initilize_all_items() {
        document.querySelectorAll(".desired_item").forEach(function (item) {
            var item_input_box = item.querySelector(".desired_item_count");
            var item_label = item_input_box.getAttribute("aria-label");
            // When clicking on the box focus the text box
            item.addEventListener("click", function () {
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
            item_input_box.addEventListener("focus", function () {
                item.classList.add("desired_item_input_focused");
                item_input_box.style.backgroundColor = "rgba(0,0,0,.5)";
                item_input_box.select();
            });
            item_input_box.addEventListener("blur", function () {
                item.classList.remove("desired_item_input_focused");
                set_textbox_background(item_input_box);
            });
            // When doubleclicking open the recipe select menu
            item.addEventListener("dblclick", function (event) {
                switch_recipe(item_label, event);
                switch_inventory_amount_input(item_label);
            });
            // Enable item name hover text
            item.addEventListener("mouseover", function () {
                hover_name_elem.textContent = item_label;
                hover_name_elem.style.opacity = "1";
            });
            item.addEventListener("mouseout", function () {
                hover_name_elem.style.opacity = "0";
            });
        });
    }
    initilize_all_items();
    /******************************************************************************\
    | Search Bar filter logic
    \******************************************************************************/
    function filter_items() {
        var search_string = item_filter_elem.value.toLowerCase();
        ;
        var hide_unused = hide_unused_checkbox_elem.checked;
        // Loop through each item
        document.querySelectorAll(".desired_item").forEach(function (item) {
            var item_name = item.querySelector("input").getAttribute("aria-label").toLowerCase();
            var item_count = parseInt(item.querySelector(".desired_item_count").value);
            // If the search string does not match hide the item
            // If the item count is not greater than 0 and hide unused is true hide
            if (item_name.indexOf(search_string) === -1 || !(item_count > 0 || !hide_unused)) {
                item.style.display = "none";
            }
            else {
                item.style.display = "block";
            }
        });
    }
    var item_filter_elem = document.getElementById("item_filter");
    item_filter_elem.addEventListener("change", filter_items);
    item_filter_elem.addEventListener("click", filter_items);
    item_filter_elem.addEventListener("keyup", filter_items);
    item_filter_elem.addEventListener("input", filter_items);
    item_filter_elem.addEventListener("paste", filter_items);
    /******************************************************************************\
    | "Hide Unused" "Show Unused" Button Logic                                     |
    \******************************************************************************/
    hide_unused_checkbox_elem.addEventListener("change", function () {
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
    function filenameify(rawname) {
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
        var selected_items = {};
        document.querySelectorAll(".desired_item").forEach(function (item) {
            var key = item.querySelector(".desired_item_count").id;
            var value = item.querySelector(".desired_item_count").value;
            var int_value = parseInt(value);
            if (!isNaN(int_value)) {
                selected_items[key] = int_value;
            }
        });
        // TODO: We probably want to do something here with replace state instead of
        // push state if possible.
        if (history.pushState) {
            history.pushState(null, "", "#" + to_url_params(selected_items));
        }
        else {
            window.location.hash = to_url_params(selected_items);
        }
        export_inventory_to_localstorage();
    }
    function to_url_params(source) {
        var array = [];
        for (var key in source) {
            array.push(encodeURIComponent(key) + "=" + encodeURIComponent(source[key]));
        }
        return array.join("&");
    }
    var inventory = {};
    var inventory_label_suffix = " [from Inventory]";
    function export_inventory_to_localstorage() {
        var input = inventory;
        input = remove_null_entries(input);
        input = input ? input : {};
        var calculatorName = window.location.pathname.replace(/\//g, "");
        localStorage.setItem("[" + calculatorName + " Inventory]", JSON.stringify(input));
    }
    function export_inventory_to_textbox() {
        inventory = remove_null_entries(inventory);
        document.getElementById("inventory_import_text").value = JSON.stringify(inventory ? inventory : {}, null, 1);
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
            for (var i in pairs) {
                var split = pairs[i].split("=");
                var id = decodeURIComponent(split[0]);
                var value = decodeURIComponent(split[1]);
                var desired_item = document.getElementById(id);
                desired_item.value = value;
                set_textbox_background(desired_item);
            }
            // check the hide unused checkbox
            if (!hide_unused_checkbox_elem.checked) {
                hide_unused_checkbox_elem.click();
            }
            generatelist();
        }
    }
    function import_inventory_from_localstorage() {
        var calculatorName = window.location.pathname.replace(/\//g, "");
        var inventoryContent = JSON.parse(localStorage.getItem("[" + calculatorName + " Inventory]") || "{}");
        inventory = remove_null_entries(inventory);
        export_inventory_to_textbox();
        return inventory;
    }
    var inventory_import_error_elem = document.getElementById("inventory_import_error");
    function import_inventory_from_textbox() {
        var text = inventory_import_text_elem.value;
        if (text.trim().length > 0) {
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
    function remove_null_entries(item_collection) {
        for (var item_name in item_collection) {
            if (!item_collection[item_name]) {
                delete item_collection[item_name];
            }
        }
        return item_collection;
    }
    ////////////////////////////////////////////////////////////////////////////////
    ///////////////////////// Requirements Calculation Logic ///////////////////////
    ////////////////////////////////////////////////////////////////////////////////
    var generate_list_button_elem = document.getElementById("generatelist");
    generate_list_button_elem.addEventListener("click", generatelist);
    function negative_requirements_exist(requirements) {
        for (var requirement in requirements) {
            if (requirements[requirement] < 0) {
                return true;
            }
        }
        return false;
    }
    var ResourceEdge = /** @class */ (function () {
        function ResourceEdge(source, target, value) {
            this.passthrough_nodes = []; // temporarily used later on
            this.source_y_offset = 0; // temporarily used later for positioning
            this.target_y_offset = 0; // temporarily used later for positioning
            this.source = source;
            this.target = target;
            this.value = value;
        }
        return ResourceEdge;
    }());
    function generatelist() {
        var e_1, _a;
        var original_requirements = gather_requirements();
        var requirements = JSON.parse(JSON.stringify(original_requirements));
        var resource_tracker = {};
        var generation_totals = {}; // the total number of each resource produce (ignoring any consumption)
        var remaining_inventory_items = JSON.parse(JSON.stringify(inventory));
        var used_from_inventory = {};
        var raw_resources = {};
        // While we still have something that requires another resource to create
        while (negative_requirements_exist(requirements)) {
            // We create a copy of requirements so that the original can stay
            // unmodified while iterating over it in the for loop
            var output_requirements = JSON.parse(JSON.stringify(requirements));
            // For each negative requirement get it's base resources
            for (var requirement in requirements) {
                if (requirements[requirement] < 0) {
                    var recipe = get_recipe(requirement);
                    var recipe_requirements = recipe.requirements;
                    var recipe_output = recipe.output;
                    if (remaining_inventory_items[requirement] > 0) {
                        var owned = remaining_inventory_items[requirement];
                        var needed = Math.abs(requirements[requirement]);
                        var recipes_from_owned = Math.floor(owned / recipe_output);
                        var overshot_from_owned = owned % recipe_output;
                        var extra_from_produce = needed % recipe_output;
                        if (overshot_from_owned < extra_from_produce) {
                            if (recipes_from_owned > 0) {
                                recipes_from_owned--;
                            }
                            else {
                                extra_from_produce = 0;
                            }
                        }
                        // Only take so much from inventory, that no [Extra] will be crafted.
                        var usable_count = Math.min(needed, extra_from_produce + recipes_from_owned * recipe_output);
                        remaining_inventory_items[requirement] -= usable_count;
                        output_requirements[requirement] += usable_count;
                        requirements[requirement] += usable_count;
                        if (used_from_inventory[requirement] === undefined) {
                            used_from_inventory[requirement] = 0;
                        }
                        used_from_inventory[requirement] += usable_count;
                        var tracker_key_1 = requirement + requirement + inventory_label_suffix;
                        if (!(tracker_key_1 in resource_tracker)) {
                            resource_tracker[tracker_key_1] = new ResourceEdge(requirement + inventory_label_suffix, requirement, 0);
                        }
                        resource_tracker[tracker_key_1].value += usable_count;
                        var inventory_key = requirement + inventory_label_suffix;
                        if (!(inventory_key in generation_totals)) {
                            generation_totals[inventory_key] = 0;
                        }
                        generation_totals[inventory_key] += usable_count;
                        // console.log("using " + usable_count + " " + requirement + " from inventory.");
                    }
                    var required_count = -requirements[requirement];
                    // Figure out the minimum number of a given requirement can be produced
                    // to fit the quantity of that requirement needed.
                    // EG: if a recipe produces 4 of an item but you only need 3
                    //     then you must produce 4 of that item with 1 left over
                    var produce_count = Math.ceil(required_count / recipe_output);
                    output_requirements[requirement] += produce_count * recipe_output;
                    // Add the quantity of the item created to the generation_totals
                    // This is used to keep track of how many of any item in the crafting process are produced
                    if (!(requirement in generation_totals)) {
                        generation_totals[requirement] = 0;
                    }
                    generation_totals[requirement] += produce_count * recipe_output;
                    // if this is a raw resource then add it to the raw resource list
                    if (recipe_requirements[requirement] === 0 && Object.keys(recipe_requirements).length === 1) {
                        if (raw_resources[requirement] === undefined) {
                            raw_resources[requirement] = 0;
                        }
                        raw_resources[requirement] += produce_count * recipe_output;
                    }
                    // If this is not a raw resource, track the change the and modify the output requirements
                    else {
                        try {
                            for (var _b = (e_1 = void 0, __values(Object.keys(recipe_requirements))), _c = _b.next(); !_c.done; _c = _b.next()) {
                                var item = _c.value;
                                // Set the recipe requirements as new output requirements
                                if (output_requirements[item] === undefined) {
                                    output_requirements[item] = 0;
                                }
                                output_requirements[item] += recipe_requirements[item] * produce_count;
                                // Add the recipe's conversion
                                var tracker_key_2 = requirement + item;
                                if (!(tracker_key_2 in resource_tracker)) {
                                    resource_tracker[tracker_key_2] = new ResourceEdge(item, requirement, 0);
                                }
                                resource_tracker[tracker_key_2].value += recipe_requirements[item] * -produce_count;
                            }
                        }
                        catch (e_1_1) { e_1 = { error: e_1_1 }; }
                        finally {
                            try {
                                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                            }
                            finally { if (e_1) throw e_1.error; }
                        }
                        ;
                    }
                }
            }
            requirements = output_requirements;
        }
        // console.log("Used from inventory:", used_from_inventory);
        for (var original_requirement in original_requirements) {
            // console.log(get_recipe(original_requirement));
            if (get_recipe(original_requirement).recipe_type === "Raw Resource") {
                resource_tracker[original_requirement + "final"] = new ResourceEdge(original_requirement, "[Final] " + original_requirement, -original_requirements[original_requirement]);
            }
        }
        // This maps all extra items to an extra value
        // It is done in order to get the right heights for items that produce more then they take
        // TODO, it might be nice to have a special path instead of a node to represent "extra"
        for (var key in output_requirements) {
            if (output_requirements[key] > 0) {
                var tracker_key = key + "extra";
                resource_tracker[tracker_key] = new ResourceEdge(key, "[Extra] " + key, output_requirements[key]);
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
                var final_tracker = source + "final";
                resource_tracker[final_tracker] = new ResourceEdge(source, "[Final] " + source, -original_requirements[source]);
                // Add in value of the non-extra resource
                generation_totals["[Final] " + source] = -original_requirements[source];
            }
        }
        for (var tracked_resource in resource_tracker) {
            if (resource_tracker[tracked_resource].value === 0) {
                delete resource_tracker[tracked_resource];
            }
        }
        generate_chart(resource_tracker, generation_totals, used_from_inventory);
        generate_instructions(resource_tracker, generation_totals);
    }
    /******************************************************************************\
    |
    \******************************************************************************/
    function gather_requirements() {
        var resources = {};
        document.querySelectorAll(".desired_item").forEach(function (elem) {
            var key = elem.querySelector("input").getAttribute("aria-label");
            var value = elem.querySelector(".desired_item_count").value;
            var numeric_value = parseInt(value);
            if (!isNaN(numeric_value)) {
                // Set the value as negative to indicate they are needed
                resources[key] = -numeric_value;
            }
        });
        return resources;
    }
    ////////////////////////////////////////////////////////////////////////////////
    ////////////////////////// Text Instruction Creation ///////////////////////////
    ////////////////////////////////////////////////////////////////////////////////
    function generate_instructions(edges, generation_totals) {
        var node_columns = get_node_columns(edges);
        var instructions = document.createElement("div");
        var column_count = 0;
        var inventory_resources = [];
        var needed_resources = [];
        // List out raw resource numbers
        for (var node in node_columns) {
            if (node_columns[node] === 0) {
                var line_wrapper = document.createElement("div");
                line_wrapper.classList.add("instruction_wrapper");
                var is_inventory = node.endsWith(inventory_label_suffix);
                var base_ingredients = text_item_object(generation_totals[node], node.replace(inventory_label_suffix, ""));
                line_wrapper.appendChild(base_ingredients);
                if (is_inventory) {
                    inventory_resources.push(line_wrapper);
                }
                else {
                    needed_resources.push(line_wrapper);
                }
            }
            // Track the largest column as the max column count
            if (node_columns[node] >= column_count) {
                column_count = node_columns[node] + 1;
            }
        }
        var base_ingredients_title_elem = document.createElement("div");
        base_ingredients_title_elem.id = "text_instructions_title"; // TODO: this should be a class now that it effects multiple elements
        base_ingredients_title_elem.textContent = (inventory_resources.length > 0 ? "Missing " : "") + "Base Ingredients";
        instructions.appendChild(base_ingredients_title_elem);
        for (var needed_resource in needed_resources) {
            instructions.appendChild(needed_resources[needed_resource]);
        }
        if (inventory_resources.length > 0) {
            var inventory_resources_title = document.createElement("div");
            inventory_resources_title.setAttribute("id", "text_instructions_title");
            inventory_resources_title.textContent = "Already Owned Base Ingredients";
            instructions.appendChild(inventory_resources_title);
            for (var inventory_resource in inventory_resources) {
                instructions.appendChild(inventory_resources[inventory_resource]);
            }
        }
        // Text Instructions for crafting
        var text_instructions_title = document.createElement("div");
        text_instructions_title.id = "text_instructions_title"; // TODO: this should be a class now that it effects multiple elements
        text_instructions_title.textContent = "Text Instructions [Beta]";
        instructions.appendChild(text_instructions_title);
        // Create the step by step instructions
        for (var i = 1; i < column_count; i++) {
            for (var node in node_columns) {
                if (node_columns[node] === i) {
                    if (node.startsWith("[Final]") || node.startsWith("[Extra]")) {
                        continue;
                    }
                    instructions.appendChild(build_instruction_line(edges, node, generation_totals));
                    var instruction_inventory_line = build_instruction_inventory_line(edges, node);
                    if (instruction_inventory_line !== null) {
                        instructions.appendChild(instruction_inventory_line);
                    }
                }
            }
            var line_break = document.createElement("div");
            line_break.classList.add("instruction_line_break");
            instructions.appendChild(line_break);
        }
        // Delete any old instructions
        while (text_instructions_elem.firstChild) {
            text_instructions_elem.removeChild(text_instructions_elem.firstChild);
        }
        // Add the new instruction list to the page
        text_instructions_elem.appendChild(instructions);
    }
    function build_instruction_line(edges, item_name, generation_totals) {
        if (!generation_totals[item_name]) {
            return document.createElement("div");
        }
        // Build the input item sub string
        var inputs = {};
        for (var edge in edges) {
            // If this is pointing into the resource we are currently trying to craft
            if (edges[edge].target === item_name && !(edges[edge].source.endsWith(inventory_label_suffix))) {
                inputs[edges[edge].source] = edges[edge].value;
            }
        }
        var recipe_type = get_recipe(item_name).recipe_type;
        if (recipe_type_functions[recipe_type] === undefined) {
            return document.createElement("div");
        }
        return recipe_type_functions[recipe_type](inputs, item_name, generation_totals[item_name], text_item_object);
    }
    function build_instruction_inventory_line(edges, item_name) {
        var amount_to_take = 0;
        for (var edge in edges) {
            // If this is pointing into the resource we are currently trying to take from the inventory.
            if (edges[edge].target === item_name && (edges[edge].source.endsWith(inventory_label_suffix))) {
                amount_to_take = edges[edge].value;
                break;
            }
        }
        if (!amount_to_take) {
            return null;
        }
        var line_wrapper = document.createElement("div");
        line_wrapper.classList.add("instruction_wrapper");
        var prefix = document.createElement("span");
        prefix.textContent = "Take ";
        line_wrapper.appendChild(prefix);
        line_wrapper.appendChild(text_item_object(amount_to_take, item_name));
        var suffix = document.createElement("span");
        suffix.textContent = " from inventory.";
        line_wrapper.appendChild(suffix);
        return line_wrapper;
    }
    var ValueListElem = /** @class */ (function () {
        function ValueListElem(count) {
            this.name = "";
            this.count = count;
        }
        return ValueListElem;
    }());
    function build_unit_value_list(number, unit_name, item_name) {
        if (number === 0) {
            return [];
        }
        if (unit_name === null) {
            return [new ValueListElem(number)];
        }
        var unit = stack_sizes[unit_name];
        var unit_size = get_unit_size(unit_name, item_name);
        var quotient = Math.floor(number / unit_size);
        var remainder = number % unit_size;
        var value_list = [];
        if (quotient > 0) {
            var value_list_element = new ValueListElem(quotient);
            if (quotient > 1) {
                value_list_element.name = unit.plural;
            }
            else {
                value_list_element.name = unit_name;
            }
            value_list = [value_list_element];
        }
        // recurse down all the other possible units until
        value_list = value_list.concat(build_unit_value_list(remainder, unit.extends_from, item_name));
        return value_list;
    }
    ////////////////////////////////////////////////////////////////////////////////
    // Gets the base number of items that would fit in a particular unit accounting
    // for the units that it is based off of.
    ////////////////////////////////////////////////////////////////////////////////
    function get_unit_size(unit_name, item_name) {
        var multiplier = stack_sizes[unit_name].quantity_multiplier;
        // Check for unique sizes for this particular item
        if ("custom_multipliers" in stack_sizes[unit_name] && item_name in stack_sizes[unit_name].custom_multipliers) {
            multiplier = stack_sizes[unit_name].custom_multipliers[item_name];
        }
        // Chain sizes from extended size
        if (stack_sizes[unit_name].extends_from !== null) {
            multiplier = multiplier * get_unit_size(stack_sizes[unit_name].extends_from, item_name);
        }
        return multiplier;
    }
    function text_item_object(count, name) {
        var item_object = document.createElement("div");
        if (!count) {
            return item_object;
        }
        item_object.classList.add("instruction_item");
        var units = document.querySelector("input[name=unit_name]:checked").value;
        var count_object = document.createElement("div");
        count_object.classList.add("instruction_item_count");
        count_object.textContent = count.toString();
        if (units !== "" && units !== undefined) {
            var unit_value_list = build_unit_value_list(count, units, name);
            var join_plus_character = "";
            var smalltext = " (";
            for (var i = 0; i < unit_value_list.length; i++) {
                smalltext += join_plus_character + unit_value_list[i].count;
                if (unit_value_list[i].name !== null) {
                    smalltext += " " + unit_value_list[i].name;
                }
                join_plus_character = " + ";
            }
            smalltext += ")";
            // If there is more then one unit, or only one that is not default
            if (unit_value_list.length > 1 || unit_value_list[0].name !== null) {
                var small_unit_elem = document.createElement("span");
                small_unit_elem.classList.add("small_unit_name");
                small_unit_elem.textContent = smalltext;
                count_object.appendChild(small_unit_elem);
            }
            item_object.appendChild(count_object);
        }
        item_object.appendChild(count_object);
        var space_object = document.createElement("span");
        space_object.textContent = " ";
        item_object.appendChild(space_object);
        var name_object = document.createElement("div");
        name_object.classList.add("instruction_item_name");
        name_object.textContent = name;
        item_object.appendChild(name_object);
        return item_object;
    }
    // This function groups the list of nodes into ones that should share
    // the same column within the generated graph
    function get_node_columns(edges) {
        var nodes = [];
        // Start by getting a list of all the nodes
        for (var edge in edges) {
            if (nodes.indexOf(edges[edge].source) === -1) {
                nodes.push(edges[edge].source);
            }
            if (nodes.indexOf(edges[edge].target) === -1) {
                nodes.push(edges[edge].target);
            }
        }
        // Recursively populate the child count and parent counts via javascript closure magic
        var child_counts = {};
        var parent_counts = {};
        function populate_child_count(node) {
            if (!(node in child_counts)) {
                child_counts[node] = 0;
                for (var edge in edges) {
                    if (edges[edge].source === node) {
                        // make sure that this child has the correct child count
                        populate_child_count(edges[edge].target);
                        // If this child's child count is larger then any other child's thus far save it as the longest
                        if (child_counts[edges[edge].target] + 1 > child_counts[node]) {
                            child_counts[node] = child_counts[edges[edge].target] + 1;
                        }
                    }
                }
            }
        }
        function populate_parent_count(node) {
            if (!(node in parent_counts)) {
                parent_counts[node] = 0;
                for (var edge in edges) {
                    if (edges[edge].target === node) {
                        // make sure that this child has the correct child count
                        populate_parent_count(edges[edge].source);
                        // If this child's child count is larger then any other child's thus far save it as the longest
                        if (parent_counts[edges[edge].source] + 1 > parent_counts[node]) {
                            parent_counts[node] = parent_counts[edges[edge].source] + 1;
                        }
                    }
                }
            }
        }
        for (var node in nodes) {
            populate_child_count(nodes[node]);
            populate_parent_count(nodes[node]);
        }
        var max_column_index = 0;
        for (var node in parent_counts) {
            if (parent_counts[node] > max_column_index) {
                max_column_index = parent_counts[node];
            }
        }
        // Snap all final results to the rightmost column
        for (var node in child_counts) {
            if (child_counts[node] === 0) {
                parent_counts[node] = max_column_index;
            }
        }
        return parent_counts;
    }
    function get_columns(edges) {
        var node_columns = get_node_columns(edges);
        // determine how many columns there should be
        var column_count = 0;
        for (var node in node_columns) {
            if (node_columns[node] + 1 > column_count) {
                column_count = node_columns[node] + 1;
            }
        }
        // Create an array of those columns
        var columns = Array(column_count);
        for (var i = 0; i < column_count; i++) {
            columns[i] = [];
        }
        for (var node in node_columns) {
            columns[node_columns[node]].push(node);
        }
        return columns;
    }
    ////////////////////////////////////////////////////////////////////////////////
    //////////////////////////////// Chart Creation ////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////
    var ResourceNode = /** @class */ (function () {
        function ResourceNode() {
            this.input = 0;
            this.output = 0;
            this.size = 0;
            this.column = 0;
            this.passthrough = false;
            this.passthrough_node_index = null; // TODO: Confirm this is correct
            this.incoming_edges = []; // List of edge key ids
            this.outgoing_edges = []; // List of edge key ids
            this.passthrough_edge_id = ""; // todo: figure out how this should be used
            // Size and positions
            this.height = 0;
            this.y = 0;
        }
        ResourceNode.prototype.node = function (input, output, size, column) {
            this.input = input;
            this.output = output;
            this.size = size;
            this.column = column;
            return this;
        };
        ResourceNode.prototype.passthrough_node = function (size, column, passthrough_node_index, passthrough_edge_id) {
            this.size = size;
            this.column = column;
            this.passthrough_node_index = passthrough_node_index;
            this.passthrough_edge_id = passthrough_edge_id;
            this.passthrough = true;
            return this;
        };
        return ResourceNode;
    }());
    /******************************************************************************\
    | generate_chart                                                               |
    |                                                                              |
    | This function is in charge of drawing the sankey chart onto the canvas       |
    |
    | Arguments
    |   generation_events -
    \******************************************************************************/
    function generate_chart(edges, node_quantities, used_from_inventory) {
        // Set the margins for the area that the nodes and edges can take up
        var margin = {
            top: 10,
            right: 1,
            bottom: 10,
            left: 1,
        };
        // Reset the colors that have already been selected so we can get repeatable graphs
        color_lookup_cache = {};
        // Set the space between the bottom of one node and the top of the one below it to 10px
        var node_padding = 10;
        // Calculate the width and the height of the area that the nodes and edges can take up
        var height = 800 - margin.top - margin.bottom;
        // Get the matrix of nodes, sorted into an array of columns
        var columns = get_columns(edges);
        // Create a representation of node objects
        var nodes = {};
        for (var column_id in columns) {
            for (var node_id in columns[column_id]) {
                var node_name = columns[column_id][node_id];
                var input = get_input_size(edges, node_name);
                var output = void 0;
                if (node_quantities[node_name] !== undefined) {
                    output = node_quantities[node_name];
                }
                else {
                    output = 0;
                }
                if (used_from_inventory[node_name] !== undefined) {
                    output += used_from_inventory[node_name];
                }
                var size = Math.max(output, input);
                nodes[node_name] = new ResourceNode().node(input, output, size, Number(column_id));
            }
        }
        // Assign all edges to the nodes depending if the edge connects as a source
        // or as a target for the given node. Also cache which column the node is
        // in for the next step of finding edges that span multiple columns
        for (var edge_id in edges) {
            var edge = edges[edge_id];
            nodes[edge.target].incoming_edges.push(edge_id);
            nodes[edge.source].outgoing_edges.push(edge_id);
        }
        // Find edges that span multiple columns and create fake nodes for them in
        // the columns they pass over. This allows us to weight the edges so they
        // wont be overlapped by a node in that column
        for (var edge_id in edges) {
            var edge = edges[edge_id];
            edge.passthrough_nodes = [];
            var source_column_index = nodes[edge.source].column;
            var target_column_index = nodes[edge.target].column;
            for (var passthrough_column_index = source_column_index + 1; passthrough_column_index < target_column_index; passthrough_column_index += 1) {
                var passthrough_node_id = edge_id + "_" + passthrough_column_index;
                nodes[passthrough_node_id] = new ResourceNode().passthrough_node(edge.value, passthrough_column_index, edge.passthrough_nodes.length, edge_id);
                edge.passthrough_nodes.push(passthrough_node_id);
                columns[passthrough_column_index].push(passthrough_node_id);
            }
        }
        // Calculate the scale of a single item based on the tallest column of items
        // such that that column fits within the allotted height of the chart
        var value_scale = 9999;
        for (var column in columns) {
            var height_for_values = height + node_padding;
            var values = 0;
            for (var node_index in columns[column]) {
                var node = nodes[columns[column][node_index]];
                height_for_values -= node_padding;
                values += node.size;
            }
            var column_scale = height_for_values / values;
            if (value_scale > column_scale) {
                value_scale = column_scale;
            }
        }
        // Calculate the positions of the nodes in each column based on the nodes
        // in other columns. We do 32 iterations of the internal process to achieve
        // very good positions
        set_node_positions(32, columns, nodes, edges, value_scale, node_padding, height);
        // Make the call to draw the chart itself now that numbers have been calculated
        layout_chart(columns, nodes, edges, height, value_scale, margin);
    }
    function set_node_positions(iterations, columns, nodes, edges, value_scale, node_padding, svg_height) {
        // Calculate Node Heights and Positions
        for (var column_index in columns) {
            var running_y = 0;
            for (var node_index in columns[column_index]) {
                var node = nodes[columns[column_index][node_index]];
                node.height = node.size * value_scale;
                node.y = running_y;
                running_y += node.height + node_padding;
            }
        }
        // Run the relaxation algorithms forwards and backwards
        for (var alpha = 1; iterations > 0; --iterations) {
            relax_columns_right_to_left(alpha *= .99, columns, nodes, edges);
            relax_columns_left_to_right(alpha, columns, nodes, edges);
            resolve_node_collisions(columns, nodes, node_padding, svg_height);
        }
    }
    function relax_columns_left_to_right(alpha, columns, nodes, edges) {
        function weighted_source_sum(node) {
            var sum = 0;
            if (node.passthrough_node_index === null) {
                for (var source_id in node.incoming_edges) {
                    var edge = edges[node.incoming_edges[source_id]];
                    var source_node = nodes[edge.source];
                    if (edge.passthrough_nodes.length) {
                        source_node = nodes[edge.passthrough_nodes[edge.passthrough_nodes.length - 1]];
                    }
                    sum += y_midpoint(source_node) * edge.value;
                }
            }
            else {
                var passthrough_edge = edges[node.passthrough_edge_id];
                if (node.passthrough_node_index === 0) {
                    sum = y_midpoint(nodes[passthrough_edge.source]) * passthrough_edge.value;
                }
                else {
                    sum = y_midpoint(nodes[passthrough_edge.passthrough_nodes[node.passthrough_node_index - 1]]) * passthrough_edge.value;
                }
            }
            return sum;
        }
        function raw_source_sum(node) {
            // If the node is not a passthrough then return the sum of all of
            // the source edges
            if (node.passthrough === false) {
                var sum = 0;
                for (var source_id in node.incoming_edges) {
                    sum += edges[node.incoming_edges[source_id]].value;
                }
                return sum;
            }
            // If this is a passthrough node then both the target and source
            // edges will be the same size as the node
            else {
                return node.size;
            }
        }
        for (var column_index in columns) {
            if (Number(column_index) === 0) {
                continue;
            }
            for (var node_index in columns[column_index]) {
                var node = nodes[columns[column_index][node_index]];
                var y = weighted_source_sum(node) / raw_source_sum(node);
                node.y += (y - y_midpoint(node)) * alpha;
            }
        }
    }
    function relax_columns_right_to_left(alpha, columns, nodes, edges) {
        function weighted_target_sum(node) {
            var sum = 0;
            if (node.passthrough_node_index === null) {
                for (var target_id in node.outgoing_edges) {
                    var edge = edges[node.outgoing_edges[target_id]];
                    var target_node = nodes[edge.target];
                    if (edge.passthrough_nodes.length) {
                        target_node = nodes[edge.passthrough_nodes[0]];
                    }
                    sum += y_midpoint(target_node) * edge.value;
                }
            }
            else {
                var passthrough_edge = edges[node.passthrough_edge_id];
                if (node.passthrough_node_index === passthrough_edge.passthrough_nodes.length - 1) {
                    sum = y_midpoint(nodes[passthrough_edge.target]) * passthrough_edge.value;
                }
                else {
                    sum = y_midpoint(nodes[passthrough_edge.passthrough_nodes[node.passthrough_node_index + 1]]) * passthrough_edge.value;
                }
            }
            return sum;
        }
        function raw_target_sum(node) {
            // If the node is not a passthrough then return the sum of all of
            // the source edges
            if (node.passthrough === false) {
                var sum = 0;
                for (var target_id in node.outgoing_edges) {
                    sum += edges[node.outgoing_edges[target_id]].value;
                }
                return sum;
            }
            // If this is a passthrough node then both the target and source
            // edges will be the same size as the node
            else {
                return node.size;
            }
        }
        columns = columns.slice().reverse();
        for (var column_index in columns) {
            if (Number(column_index) === 0) {
                continue;
            }
            for (var node_index in columns[column_index]) {
                var node = nodes[columns[column_index][node_index]];
                var y = weighted_target_sum(node) / raw_target_sum(node);
                node.y += (y - y_midpoint(node)) * alpha;
            }
        }
    }
    function y_midpoint(node) {
        return node.y + node.height / 2;
    }
    function resolve_node_collisions(columns, nodes, node_padding, svg_height) {
        function y_comp(a, b) {
            return nodes[a].y - nodes[b].y;
        }
        // Sort all the nodes in the array based on their visual order
        for (var column_index in columns) {
            var column = columns[column_index];
            column.sort(y_comp);
            // If any node is overlapping the previous node push it downwards
            var bottom_of_previous_node = 0;
            for (var i = 0; i < column.length; i++) {
                var node = nodes[column[i]];
                // Check to see if there is an overlap and fix it if so
                var delta_y = bottom_of_previous_node - node.y;
                if (delta_y > 0) {
                    node.y += delta_y;
                }
                // Set the bottom of this node to be the bottom of the previous node for the next cycle
                bottom_of_previous_node = node.y + node.height + node_padding;
            }
            // If any node is overlapping push it upwards
            // maybe this can include node padding as we dont need a padding on the bottom
            var top_of_previous_node = svg_height;
            for (var i = column.length - 1; i >= 0; i--) {
                var node = nodes[column[i]];
                var delta_y = top_of_previous_node - (node.y + node.height);
                if (delta_y < 0) {
                    node.y += delta_y;
                }
                top_of_previous_node = node.y - node_padding;
            }
        }
    }
    function hexToRgb(hex) {
        var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16),
        } : { r: 0, b: 0, g: 0 };
    }
    function color_darken(color) {
        var k = 0.49;
        return {
            r: Math.round(color.r * k),
            g: Math.round(color.g * k),
            b: Math.round(color.b * k),
        };
    }
    function color_string(color) {
        return "rgb(" + color.r + "," + color.g + "," + color.b + ")";
    }
    /******************************************************************************\
    | get_color
    |
    | This function supplies a color for a node to use as it's fill color. The
    | color is determined by the first word in the string, excluding a [Extra] or
    | [Final] prefix. The first time that key is presented to the function a new
    | color is chosen for that key, each subsequent call after the first  with the
    | same key will return the same color but this is not necessarily the case for
    | a new chart generation.
    \******************************************************************************/
    var all_colors = [
        hexToRgb("1f77b4"),
        hexToRgb("aec7e8"),
        hexToRgb("ff7f0e"),
        hexToRgb("ffbb78"),
        hexToRgb("2ca02c"),
        hexToRgb("98df8a"),
        hexToRgb("d62728"),
        hexToRgb("ff9896"),
        hexToRgb("9467bd"),
        hexToRgb("c5b0d5"),
        hexToRgb("8c564b"),
        hexToRgb("c49c94"),
        hexToRgb("e377c2"),
        hexToRgb("f7b6d2"),
        hexToRgb("bcbd22"),
        hexToRgb("dbdb8d"),
        hexToRgb("17becf"),
        hexToRgb("9edae5"),
        hexToRgb("7f7f7f"),
        hexToRgb("c7c7c7"),
    ];
    var color_lookup_cache = {};
    function get_color(key) {
        // Strip out Extra and Final prefixes
        key = key.replace(/^\[Extra\] /, "");
        key = key.replace(/^\[Final\] /, "");
        // Strip out everything past the first word
        key = key.replace(/ .*/, "");
        // Lookup or set the color that is attached to this key
        var index = color_lookup_cache[key];
        if (index === undefined) {
            index = Object.keys(color_lookup_cache).length % all_colors.length;
            color_lookup_cache[key] = index;
        }
        return all_colors[index];
    }
    /******************************************************************************\
    | layout_chart
    |
    | draw the chart itself
    \******************************************************************************/
    var CachedChartData = /** @class */ (function () {
        function CachedChartData() {
            this.columns = [];
            this.nodes = {};
            this.edges = {};
            this.height = 0;
            this.value_scale = 0;
            this.margin = { top: 0, right: 0, bottom: 0, left: 0 };
        }
        return CachedChartData;
    }());
    var cached_chart_data;
    function layout_chart(columns, nodes, edges, height, value_scale, margin) {
        cached_chart_data = {
            columns: columns,
            nodes: nodes,
            edges: edges,
            height: height,
            value_scale: value_scale,
            margin: margin,
        };
        relayout_chart();
    }
    window.onresize = function () {
        relayout_chart();
    };
    var chart_elem = document.getElementById("chart");
    var content_elem = document.getElementById("content");
    function relayout_chart() {
        if (Object.keys(cached_chart_data).length === 0) {
            return;
        }
        var columns = cached_chart_data.columns;
        var nodes = cached_chart_data.nodes;
        var edges = cached_chart_data.edges;
        var height = cached_chart_data.height;
        var value_scale = cached_chart_data.value_scale;
        var margin = cached_chart_data.margin;
        var width = content_elem.offsetWidth - margin.left - margin.right;
        var node_width = 20;
        // Determine the space between the left hand side of each node column
        var node_spacing = (width - node_width) / (columns.length - 1);
        // Empty the chart immediately
        while (chart_elem.lastChild) {
            chart_elem.removeChild(chart_elem.lastChild);
        }
        // Create the new SVG object that will represent our chart
        var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        var padding_g = document.createElementNS("http://www.w3.org/2000/svg", "g");
        padding_g.setAttribute("transform", "translate(" + margin.left + "," + margin.top + ")");
        svg.appendChild(padding_g);
        // Create the group that will hold all of the edges to make sure they show up below nodes
        var edges_g = document.createElementNS("http://www.w3.org/2000/svg", "g");
        padding_g.appendChild(edges_g);
        // Create the group that will hold all the nodes after edges to make sure nodes show up on top
        var nodes_g = document.createElementNS("http://www.w3.org/2000/svg", "g");
        padding_g.appendChild(nodes_g);
        // Draw all of the node lines
        for (var column_index_string in columns) {
            var column_index = parseInt(column_index_string);
            var x = node_spacing * column_index;
            for (var node_index in columns[column_index]) {
                var node_id = columns[column_index][node_index];
                var node = nodes[node_id];
                // Build the node
                if (!node.passthrough) {
                    var left_height = node.input * value_scale;
                    var full_height = node.size * value_scale;
                    var right_height = node.output * value_scale;
                    if (Number(column_index) === 0) {
                        left_height = full_height;
                    }
                    var d = "M 0,0 L 0," + left_height + " " + node_width / 3 + "," + left_height + " " + node_width / 3 + "," + full_height + " " + node_width * 2 / 3 + "," + full_height + " " + node_width * 2 / 3 + "," + right_height + " " + node_width + "," + right_height + " " + node_width + ",0 Z";
                    var node_g = document.createElementNS("http://www.w3.org/2000/svg", "g");
                    node_g.setAttribute("transform", "translate(" + x + "," + node.y + ")");
                    node_g.setAttribute("class", "node");
                    var fill_color = get_color(node_id);
                    var edge_color = color_darken(fill_color);
                    var node_shape_elem = document.createElementNS("http://www.w3.org/2000/svg", "path");
                    node_shape_elem.setAttribute("d", d);
                    node_shape_elem.setAttribute("style", "fill: " + color_string(fill_color) + "; stroke: " + color_string(edge_color) + ";");
                    node_g.appendChild(node_shape_elem);
                    var text_offset = node_width + 6;
                    var text_anchor = "start";
                    if (column_index >= columns.length / 2) {
                        text_offset = -6;
                        text_anchor = "end";
                    }
                    var node_name_text = document.createElementNS("http://www.w3.org/2000/svg", "text");
                    node_name_text.setAttribute("x", text_offset.toString());
                    node_name_text.setAttribute("y", (full_height / 2).toString());
                    node_name_text.setAttribute("dy", ".35em");
                    node_name_text.setAttribute("text-anchor", text_anchor);
                    node_name_text.textContent = node_id;
                    node_g.appendChild(node_name_text);
                    nodes_g.appendChild(node_g);
                }
            }
        }
        // Determine offset of all the edge connections
        function source_y(edge_id) {
            var edge = edges[edge_id];
            // if this is a passthrough edge get the last passthrough node instead of the source
            if (edge.passthrough_nodes.length > 0) {
                return nodes[edge.passthrough_nodes[edge.passthrough_nodes.length - 1]].y;
            }
            else {
                return nodes[edge.source].y;
            }
        }
        function source_y_comp(a, b) {
            return source_y(a) - source_y(b);
        }
        function target_y(edge_id) {
            var edge = edges[edge_id];
            // if this is a passthrough edge get the first passthrough node instead of the target
            if (edge.passthrough_nodes.length > 0) {
                return nodes[edge.passthrough_nodes[0]].y;
            }
            else {
                return nodes[edge.target].y;
            }
        }
        function target_y_comp(a, b) {
            return target_y(a) - target_y(b);
        }
        for (var node_id_1 in nodes) {
            var node = nodes[node_id_1];
            if (node.passthrough === false) {
                node.incoming_edges.sort(source_y_comp);
                node.outgoing_edges.sort(target_y_comp);
                var running_edge_height = 0;
                for (var edge_id in node.incoming_edges) {
                    var edge_1 = edges[node.incoming_edges[edge_id]];
                    edge_1.target_y_offset = running_edge_height;
                    running_edge_height += edge_1.value * value_scale;
                }
                running_edge_height = 0;
                for (var edge_id in node.outgoing_edges) {
                    var edge_2 = edges[node.outgoing_edges[edge_id]];
                    edge_2.source_y_offset = running_edge_height;
                    running_edge_height += edge_2.value * value_scale;
                }
            }
        }
        // Draw all of the edge Lines
        for (var edge_index in edges) {
            var edge = edges[edge_index];
            var line_thickness = edge.value * value_scale;
            var node_g = document.createElementNS("http://www.w3.org/2000/svg", "g");
            node_g.setAttribute("transform", "translate(" + 0 + "," + 0 + ")");
            var start_node = nodes[edges[edge_index].source];
            var end_node = nodes[edges[edge_index].target];
            var mid_x_mod = (node_spacing - node_width) / 2;
            var start_x = start_node.column * node_spacing + node_width;
            var start_y = start_node.y + edge.source_y_offset + line_thickness / 2;
            var d = "M" + start_x + "," + start_y + "C" + (start_x + mid_x_mod) + "," + start_y + " ";
            for (var passthrough_node_index in edges[edge_index].passthrough_nodes) {
                var passthrough_node = nodes[edges[edge_index].passthrough_nodes[passthrough_node_index]];
                var passthrough_x = passthrough_node.column * node_spacing;
                var passthrough_y = passthrough_node.y + line_thickness / 2;
                d += (passthrough_x - mid_x_mod) + "," + passthrough_y + " " + passthrough_x + "," + passthrough_y + "C" + (passthrough_x + mid_x_mod) + "," + passthrough_y + " ";
            }
            var end_x = end_node.column * node_spacing;
            var end_y = end_node.y + edge.target_y_offset + line_thickness / 2;
            d += (end_x - mid_x_mod) + "," + end_y + " " + end_x + "," + end_y;
            var edge_shape_elem = document.createElementNS("http://www.w3.org/2000/svg", "path");
            edge_shape_elem.setAttribute("d", d);
            edge_shape_elem.setAttribute("style", "stroke-width: " + line_thickness + "px;");
            edge_shape_elem.setAttribute("class", "link");
            node_g.appendChild(edge_shape_elem);
            edges_g.appendChild(node_g);
        }
        var chart_width = width + margin.left + margin.right;
        var chart_height = height + margin.top + margin.bottom;
        svg.setAttribute("width", chart_width.toString());
        svg.setAttribute("height", chart_height.toString());
        chart_elem.appendChild(svg);
    }
    function get_input_size(edges, output) {
        var inputs_size = 0;
        for (var edge in edges) {
            if (edges[edge].target === output) {
                inputs_size += edges[edge].value;
            }
        }
        return inputs_size;
    }
    ////////////////////////////////////////////////////////////////////////////////
    /////////////////////////////// Hover Text Logic ///////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////
    // How far away from the mouse should the hoverbox be
    var hover_x_offset = 10;
    var hover_y_offset = -10;
    document.addEventListener("mousemove", function (e) {
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
    function switch_recipe(item_name, event) {
        var recipe_selector = recipe_select_elem;
        // Clear the recipe selector list
        while (recipe_selector_list_elem.lastChild) {
            recipe_selector_list_elem.removeChild(recipe_selector_list_elem.lastChild);
        }
        var _loop_1 = function (i) {
            recipe_item = document.createElement("div");
            recipe_item.classList.add("recipe_select_item");
            recipe_item.addEventListener("click", (function (index) {
                return function () {
                    set_recipe_index(item_name, index);
                    find_loop_from_node(item_name);
                    recipe_selector.style.opacity = "0";
                    recipe_selector.style.pointerEvents = "none";
                };
            })(i));
            var recipe_category = document.createElement("div");
            recipe_category.classList.add("recipe_select_item_name");
            recipe_category.textContent = recipe_json[item_name][i].recipe_type;
            for (var j in recipe_json[item_name][i].requirements) {
                (function (j) {
                    var quantity = -recipe_json[item_name][i].requirements[j];
                    var item_elem = document.createElement("div");
                    item_elem.classList.add("required_item");
                    item_elem.classList.add("item");
                    item_elem.classList.add("item_" + filenameify(j));
                    item_elem.textContent = quantity.toString();
                    recipe_category.appendChild(item_elem);
                    item_elem.addEventListener("mouseover", function () {
                        hover_name_elem.textContent = quantity + "x " + j;
                        hover_name_elem.style.opacity = "1";
                    });
                    item_elem.addEventListener("mouseout", function () {
                        hover_name_elem.style.opacity = "0";
                    });
                })(j);
            }
            recipe_item.appendChild(recipe_category);
            var clear_div = document.createElement("div");
            clear_div.classList.add("clear");
            recipe_item.appendChild(clear_div);
            recipe_selector_list_elem.appendChild(recipe_item);
        };
        var recipe_item;
        for (var i = 0; i < recipe_json[item_name].length; i++) {
            _loop_1(i);
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
        if (window.innerHeight + window.pageYOffset < recipe_selector.offsetHeight + event.pageY + menu_y_offset) {
            top_offset = event.pageY - menu_y_offset - recipe_selector.offsetHeight;
        }
        recipe_selector.style.top = top_offset.toString() + "px";
        recipe_selector.style.left = left_offset.toString() + "px";
    }
    function switch_inventory_amount_input(item_name) {
        inventory_amount_input_elem.setAttribute("item_name", item_name); //???
        if (inventory[item_name] === undefined) {
            inventory_amount_input_elem.value = "0";
        }
        else {
            inventory_amount_input_elem.value = inventory[item_name].toString();
        }
    }
    recipe_select_elem.addEventListener("mouseleave", function () {
        recipe_select_elem.style.opacity = "0";
        recipe_select_elem.style.pointerEvents = "none";
    });
    var inventory_amount_input_elem = document.getElementById("inventory_amount_input");
    inventory_amount_input_elem.addEventListener("change", function () {
        var item_name = inventory_amount_input_elem.getAttribute("item_name");
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
        for (var i = 0; i < recipe_json[node_name].length; i++) {
            if (recipe_json[node_name][i].recipe_type === "Raw Resource") {
                set_recipe_index(node_name, i);
                return;
            }
        }
        alert("ERROR: Failed to set raw resource for " + node_name);
    }
    function get_recipe(node_name) {
        return recipe_json[node_name][get_recipe_index(node_name)];
    }
    function find_loop_from_node(start_node) {
        // Generate Light Node Mapping
        var nodes = {};
        for (var node in recipe_json) {
            // Add all the edges
            nodes[node] = [];
            for (var edge in get_recipe(node).requirements) {
                if (-get_recipe(node).requirements[edge] > 0) {
                    nodes[node].push(edge);
                }
            }
        }
        //Depth First search
        var recipe_changes = depth_first_search(nodes, start_node, start_node);
        for (var i in recipe_changes) {
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
            // if a requirement is the original node then change this item to a source and report back
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
    function set_textbox_background(textbox) {
        if (textbox.value === "") {
            textbox.style.backgroundColor = "rgba(0,0,0,0)";
        }
        else {
            textbox.style.backgroundColor = "rgba(0,0,0,.5)";
        }
    }
    // Run the load function to load arguments from the URL if they exist
    load();
    // Closure wrapper for the script file
})();
// Closure wrapper for the script file
//# sourceMappingURL=calculator.js.map