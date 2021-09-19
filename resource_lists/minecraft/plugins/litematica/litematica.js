function convertMaterialListToRequestHash(inputString) {
    // unify line endings
    inputString = inputString.replace(/\r\n/gm, "\n")
        // remove leading spaces
        .replace(/(\n|^)\s+/gm, "$1")
        // remove trailing spaces
        .replace(/\s+(\n|$)/gm, "$1")
        // remove illegal characters (see build.py get_simple_name function)
        .toLowerCase().replaceAll(/[^a-z0-9|,\n]/gm, "")
        // remove non-item lines
        .replace(/(\n|^)(?!\|(\S+)\|(\d+)\|(\d+)\|(\d+)\||[a-z0-9]+,\d+,\d+,\d+)(.*?)(\n|$)/gm, "")
        // convert into csv
        .replace(/(\n|^)\|(.+?)\|(\d+)\|(\d+)\|(\d+)\|(\n|$)/gm, "$1$2,$3,$4,$5$6")
        // remove leading & trailing blank lines
        .trim();

    // convert each line into a "name=##"-format with the totals as value
    var items = inputString.split("\n");
    var totals = items.map((item) => {
        var itemTotal = item.split(",");
        return [itemTotal[0], itemTotal[1]].join("=");
    });

    var totalsQuery = "#" + totals.join("&");
    return totalsQuery;
}

function setOutput(outputString) {
    var outputElement = document.getElementById("output");
    outputElement.innerText = outputString;
    outputElement.href = "../../" + outputString;
}

function processInput() {
    var inputString = document.getElementById("input").value;
    var outputString = convertMaterialListToRequestHash(inputString);
    setOutput(outputString);
}

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("loadInputFile").addEventListener('change', function() {
        var file = document.getElementById("loadInputFile").files[0];

        if (file.name.match(/\.(txt|csv)$/)) {
            var reader = new FileReader();

            reader.onload = function() {
                document.getElementById("input").value = reader.result;
                processInput();
            };

            reader.readAsText(file);
        } else {
            alert("File not supported, .txt or .csv files only");
        }
    });

    document.getElementById("input").addEventListener('change', processInput);
    document.getElementById("input").addEventListener('keyup', processInput);

    processInput();
});