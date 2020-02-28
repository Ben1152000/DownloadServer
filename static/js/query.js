
function query() {
    var query = document.getElementById('query-box').value;
    var files = document.getElementById('file-box').children;
    var count = 0;
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        if (file.id == "file-box-label") {
            // pass
        } else if (file.id == "file-box-empty") {
            file.style.display = count? "none": "block";
        } else {
            if (query.charAt(0) == '.') { // search for extension
                if (file.dataset.type.toLowerCase().includes(query.substring(1).toLowerCase())) {
                    file.style.display = "block";
                    count += 1;
                } else { 
                    file.style.display = "none"; 
                }
            } else {
                if (file.dataset.name.toLowerCase().includes(query.toLowerCase())) {
                    file.style.display = "block";
                    count += 1;
                } else { 
                    file.style.display = "none"; 
                }
            }
        }
    }
}

function clear() {
    document.getElementById('query-box').value = "";
}