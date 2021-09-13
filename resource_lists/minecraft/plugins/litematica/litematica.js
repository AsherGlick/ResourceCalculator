function convertMaterialListToRequestHash(inputString) {
    // unify line endings
    inputString = inputString.replace(/\r\n/gm, "\n")
        // remove preface lines
        .replace(/^(.*\n){5}/, "")
        // remove delimiter lines
        .replace(/(\r?\n|^)\+-+\+-+\+-+\+-+\+(\r?\n|$)/gm, "$1")
        // remove all lines without numbers between the pipes (aka headlines)
        .replace(/(\r?\n|^)\|[^0-9]+\|(\r?\n|$)/gm, "$1")
        // convert into csv
        .replace(/\| +(.+?) +\| +(\d+) +\| +(\d+) +\| +(\d+) +\|/gm, "$1;$2;$3;$4")
        // remove leading & trailing blank lines
        .trim();

    // convert each line into a "name=##"-format with the totals as value
    var items = inputString.split("\n");
    var totals = items.map((item) => {
        var itemTotal = item.split(";");
        return [itemTotal[0].trim().toLowerCase().replaceAll(/[^a-z0-9]/gm, ""), itemTotal[1]].join("=");
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

        if (file.name.match(/\.(txt)$/)) {
            var reader = new FileReader();

            reader.onload = function() {
                document.getElementById("input").value = reader.result;
                processInput();
            };

            reader.readAsText(file);
        } else {
            alert("File not supported, .txt files only");
        }
    });

    document.getElementById("input").addEventListener('change', processInput);
    document.getElementById("input").addEventListener('keyup', processInput);

    processInput();
});