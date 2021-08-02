// BEGINGENERATOR
function write_ResourceList(object, indented=0){
    let output = "";
    const tab = "  ";
    let indent = tab.repeat(indented);
    const key_list = ["authors","index_page_display_name","row_group_count","game_version","banner_message","recipe_types","requirement_groups","stack_sizes","default_stack_size","resources"];
    const key_set = new Set(key_list);
    let key_names = Object.keys(object);
    for (var i in key_names) {
        let key_name = key_names[i];
        if (!key_set.has(key_name)) {
            console.warn("Unknown Key Found " + key_name);
        }
    }
    if ("authors" in object) {
        output += indent + "authors:"
        output += "\n";
        for (let list_index in object["authors"]) {
        output += indent + tab + "- " + write_Author(object["authors"][list_index], indented+2).trim() + "\n";
        }
    }
    if ("index_page_display_name" in object) {
        output += "\n"
        output += indent + "index_page_display_name:"
        output += " \"" + object["index_page_display_name"] + "\"\n";
    }
    if ("row_group_count" in object) {
        output += "\n"
        output += indent + "row_group_count:"
        output += " " + object["row_group_count"] + "\n";
    }
    if ("game_version" in object) {
        output += "\n"
        output += indent + "game_version:"
        output += " \"" + object["game_version"] + "\"\n";
    }
    if ("banner_message" in object) {
        output += "\n"
        output += indent + "banner_message:"
        output += " \"" + object["banner_message"] + "\"\n";
    }
    if ("recipe_types" in object) {
        output += "\n"
        output += indent + "recipe_types:"
        output += "\n";
        for (let dict_key in object["recipe_types"]) {
            output += indent + tab + dict_key + ": \"" + object["recipe_types"][dict_key] + "\"\n";
        }
    }
    if ("requirement_groups" in object) {
        output += "\n"
        output += indent + "requirement_groups:"
        for (let dict_key in object["requirement_groups"]) {
            output += "\n"
              output += indent + tab + dict_key + ":\n";
              for (let list_index in object["requirement_groups"][dict_key]) {
                  output +=  indent + tab + tab + "- " + object["requirement_groups"][dict_key][list_index] + "\n"
              }
        }
    }
    if ("stack_sizes" in object) {
        output += "\n"
        output += indent + "stack_sizes:"
        output += "\n";
        for (let dict_key in object["stack_sizes"]) {
              output += indent + tab + dict_key + ":\n" + write_StackSize( object["stack_sizes"][dict_key], indented+2);
        }
    }
    if ("default_stack_size" in object) {
        output += "\n"
        output += indent + "default_stack_size:"
        output += " \"" + object["default_stack_size"] + "\"\n";
    }
    if ("resources" in object) {
        output += "\n"
        output += indent + "resources:"
        for (let list_index in object["resources"]) {
            output += "\n"
        output += indent + tab + "- " + write_Resource(object["resources"][list_index], indented+2).trim() + "\n";
        }
    }
    return output;
}


function write_StackSize(object, indented=0){
    let output = "";
    const tab = "  ";
    let indent = tab.repeat(indented);
    const key_list = ["quantity_multiplier","plural","extends_from","custom_multipliers"];
    const key_set = new Set(key_list);
    let key_names = Object.keys(object);
    for (var i in key_names) {
        let key_name = key_names[i];
        if (!key_set.has(key_name)) {
            console.warn("Unknown Key Found " + key_name);
        }
    }
    if ("quantity_multiplier" in object) {
        output += indent + "quantity_multiplier:"
        output += " " + object["quantity_multiplier"] + "\n";
    }
    if ("plural" in object) {
        output += indent + "plural:"
        output += " \"" + object["plural"] + "\"\n";
    }
    if ("extends_from" in object) {
        output += indent + "extends_from:"
        if (object["extends_from"] == null) {
            output += " null\n";
        } else {
            output += " \"" + object["extends_from"] + "\"\n";
        }
    }
    return output;
}


function write_Resource(object, indented=0){
    let output = "";
    const tab = "  ";
    let indent = tab.repeat(indented);
    const key_list = ["name","id","recipes","custom_stack_multipliers","custom_simplename","currency"];
    const key_set = new Set(key_list);
    let key_names = Object.keys(object);
    for (var i in key_names) {
        let key_name = key_names[i];
        if (!key_set.has(key_name)) {
            console.warn("Unknown Key Found " + key_name);
        }
    }
    if ("name" in object) {
        output += indent + "name:"
        output += " \"" + object["name"] + "\"\n";
    }
    if ("id" in object) {
        output += indent + "id:"
        output += " " + object["id"] + "\n";
    }
    if ("recipes" in object) {
        output += indent + "recipes:"
        output += "\n";
        for (let list_index in object["recipes"]) {
        output += indent + tab + "- " + write_Recipe(object["recipes"][list_index], indented+2).trim() + "\n";
        }
    }
    if ("custom_stack_multipliers" in object) {
        output += indent + "custom_stack_multipliers:"
        output += "\n";
        for (let dict_key in object["custom_stack_multipliers"]) {
              output += indent + tab + dict_key + ": " + object["custom_stack_multipliers"][dict_key] + "\n";
        }
    }
    if ("custom_simplename" in object) {
        output += indent + "custom_simplename:"
        output += " \"" + object["custom_simplename"] + "\"\n";
    }
    if ("currency" in object) {
        output += indent + "currency:"
        if (object["currency"]) {
            output += " true\n";
        } else {
            output += " false\n";
        }
    }
    return output;
}


function write_Recipe(object, indented=0){
    let output = "";
    const tab = "  ";
    let indent = tab.repeat(indented);
    const key_list = ["output","recipe_type","requirements"];
    const key_set = new Set(key_list);
    let key_names = Object.keys(object);
    for (var i in key_names) {
        let key_name = key_names[i];
        if (!key_set.has(key_name)) {
            console.warn("Unknown Key Found " + key_name);
        }
    }
    if ("output" in object) {
        output += indent + "output:"
        output += " " + object["output"] + "\n";
    }
    if ("recipe_type" in object) {
        output += indent + "recipe_type:"
        output += " \"" + object["recipe_type"] + "\"\n";
    }
    if ("requirements" in object) {
        output += indent + "requirements:"
        output += "\n";
        for (let dict_key in object["requirements"]) {
              output += indent + tab + dict_key + ": " + object["requirements"][dict_key] + "\n";
        }
    }
    return output;
}


function write_Author(object, indented=0){
    let output = "";
    const tab = "  ";
    let indent = tab.repeat(indented);
    const key_list = ["name","link"];
    const key_set = new Set(key_list);
    let key_names = Object.keys(object);
    for (var i in key_names) {
        let key_name = key_names[i];
        if (!key_set.has(key_name)) {
            console.warn("Unknown Key Found " + key_name);
        }
    }
    if ("name" in object) {
        output += indent + "name:"
        output += " \"" + object["name"] + "\"\n";
    }
    if ("link" in object) {
        output += indent + "link:"
        output += " \"" + object["link"] + "\"\n";
    }
    return output;
}
// ENDGENERATOR