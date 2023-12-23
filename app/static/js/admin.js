rowAddIndex = 3;

function addRow() {
    var id = document.getElementById("id");
    var quanVal = document.getElementById("quantity").value;
    var cate = document.getElementById("categories");
    var auth = document.getElementById("authors");
    var del = document.getElementById("del");

    if (quanVal !== '' && cate.selectedIndex !== -1 && auth.selectedIndex !== -1) {
        var table = document.getElementById("addTable");
        var row = table.insertRow(rowAddIndex++);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);
        var cell5 = row.insertCell(4);
        var cell6 = row.insertCell(5);
        cell1.innerHTML = "<p style='text-align: center; vertical-align: center'>" + id.value + "</p>";
        cell2.innerHTML = ""
        cell3.innerHTML = "<p style='text-align: center; vertical-align: center'>" + getSelectText(cate) + "</p>"
        cell4.innerHTML = "<p style='text-align: center; vertical-align: center'>" + getSelectText(auth) + "</p>"
        cell5.innerHTML = "<p style='text-align: center; vertical-align: center'>" + quanVal + "</p>"
        cell6.innerHTML = "<button id='del' onclick='deleteRow(this)' type='button' class='btn btn-danger'>X</button>"
        id.value++;
    }
}

function deleteRow(r) {
    var i = r.parentNode.parentNode.rowIndex;
    document.getElementById("addTable").deleteRow(i);
    rowAddIndex--;
}

function getSelectText(select) {
    var result = [];
    var options = select && select.options;
    var opt;

    for (var i = 0; i < options.length; i++) {
        opt = options[i];

        if (opt.selected) {
            result.push(' ' + opt.text);
        }
    }
    return result;
}