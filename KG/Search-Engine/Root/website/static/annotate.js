document.addEventListener("DOMContentLoaded", function(event) {   
    var canvas = document.getElementById("canvas");
    var rect = canvas.getBoundingClientRect();
    var main_image = document.getElementById("image");
    var image_rect = null;
    var widthScale = 1.0;
    var heightScale = 1.0;
    var current_index = 0;
    var data = null;
    var got_images = false;
    
    document.getElementById('loadingsym').style.visibility = 'visible';
    document.getElementById('canvas').style.visibility = 'hidden';

    main_image.onload = function(e) {
        document.getElementById('path_str').innerText = data[current_index].path.split('/').slice(-2).join('/');
        image_rect = main_image.getBoundingClientRect();
        widthScale = image_rect.width / main_image.naturalWidth;
        heightScale = image_rect.height / main_image.naturalHeight;
        draw_bounding_boxes();
        }

    function save_bounding_boxes() {
        var p_bounding_boxes = [];
        var scrollTop = window.pageYOffset || (document.documentElement || document.body.parentNode || document.body).scrollTop;
        var c = canvas.children;
        for(let i = 1; i < c.length; i++) {
            item = {};
            item['word'] = c[i].dataset.word;
            var boxRect = c[i].getBoundingClientRect();
            console.log(boxRect);
            item['boundingbox'] = {};
            item['boundingbox']['topLeftx'] = Math.ceil((boxRect.left - rect.left)/widthScale);
            item['boundingbox']['topLefty'] = Math.ceil((boxRect.top - scrollTop - rect.top)/heightScale);
            item['boundingbox']['botRightx'] = item['boundingbox']['topLeftx'] + Math.ceil(boxRect.width / widthScale);
            item['boundingbox']['botRighty'] = item['boundingbox']['topLefty'] + Math.ceil(boxRect.height / heightScale);
            console.log(item);
            p_bounding_boxes.push(item);
        }
        if (p_bounding_boxes.length > 0) {
            data[current_index]['p_bounding_boxes'] = p_bounding_boxes;
        }
    }

    function draw_bounding_boxes() {
        var bbx = data[current_index].bounding_boxes;
        if("p_bounding_boxes" in data[current_index])
            bbx = data[current_index].p_bounding_boxes;
        for(let i=0; i < bbx.length; i++) {
            bounding_box = bbx[i];
            console.log(bounding_box);
            addDiv(bounding_box.word, Math.floor(bounding_box.boundingbox.topLeftx * widthScale) + rect.left, Math.floor(bounding_box.boundingbox.topLefty * heightScale), Math.floor(Math.abs(bounding_box.boundingbox.topLeftx - bounding_box.boundingbox.botRightx) * widthScale), Math.floor(Math.abs(bounding_box.boundingbox.topLefty - bounding_box.boundingbox.botRighty) * heightScale));
        }
    }

    function get_annotations() {
        var annotations = [];
        for(let i = 0; i < data.length; i++) {
            item = {};
            item['path'] = data[i].path;
            if("p_bounding_boxes" in data[i]) {
                item['bounding_boxes'] = data[i]['p_bounding_boxes'];
            }
            else {
                item['bounding_boxes'] = data[i]['bounding_boxes'];
            }
            annotations.push(item);
        }
        return annotations;
    }

    function clearCanvas() {
        var c = canvas.children;
        for(let i = c.length - 1; i > 0; i--) {
            canvas.removeChild(c[i]);
        }
    }

    function get(paths) {
        let xhr = new XMLHttpRequest();
        let url = location.origin + '/getimages';
    
        // open a connection
        xhr.open("POST", url, true);

        // Set the request header i.e. which type of content you are sending
        xhr.setRequestHeader("Content-Type", "application/json");

        // Create a state change callback
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                // Print received data from server
                resp = JSON.parse(this.responseText);
                for(let i = 0; i < resp.data.length; i++) {
                    for(let j = 0; j < data.length; j++) {
                        if (resp.data[i].path === data[i].path) {
                            data[i]['b_image'] = resp.data[i].b_image;
                        }
                    }
                  }
                got_images = true;
                document.getElementById('loadingsym').style.visibility = 'hidden';
                initialize_image(current_index);
                document.getElementById('canvas').style.visibility = 'visible';
            }
        };

        // Converting JSON data to string
        var d_paths = JSON.stringify({'paths': paths});

        // Sending data with the request
        xhr.send(d_paths);
    }
    
    function setData(uuid) {
        data = JSON.parse(localStorage.getItem(uuid));
        var paths = [];
        for(let i = 0; i < data.length; i++) {
            paths.push(data[i].path);
        }
        get(paths.join(","));
        if (current_index === 0) {
            document.getElementById("previous_button").style.visibility = "hidden";
        }
        if (current_index < data.length-1) {
            document.getElementById("next_button").style.visibility = "visible";
        }
        // initialize_image(current_index);
    }
    setData(main_image.dataset.uuid);

    var ro = new ResizeObserver(entries => {
        if (got_images) {
            save_bounding_boxes();
            clearCanvas();
            set_image(current_index);
        }
    });
    ro.observe(canvas);

    function initialize_image(index) {
        set_image(index)
        if(data.length == 1) {
            document.getElementById("next_button").disabled = true;
            document.getElementById("previous_button").disabled = true;
        }
    }

    function set_image(index) {
        main_image.setAttribute('src', 'data:image/png;base64,' + data[index]['b_image']);
    }

    /*===== LINK ACTIVE =====*/
    const linkColor = document.querySelectorAll('.nav_link')

    function colorLink(){
        if(linkColor){
            linkColor.forEach(l=> l.classList.remove('active'))
            this.classList.add('active')
        }
    }
    linkColor.forEach(l=> l.addEventListener('click', colorLink))

    function addDiv(word, x1, y1, width, height) {
        console.log(word + " " + x1 + " " + y1 + " " + width + " " + height);
        var scrollTop = window.pageYOffset || (document.documentElement || document.body.parentNode || document.body).scrollTop;
        var new_child = document.createElement('div');
        new_child.className = "rectangle";
        new_child.style.left = (x1) + "px";
        new_child.style.top = (y1 + scrollTop) + "px";
        new_child.style.width = width + "px";
        new_child.style.height = height + "px";
        new_child.dataset.word = word;
        new_child.dataset.toggle = "tooltip";
        new_child.title = word;
        new_child.dataset.placement = "bottom";
        new_child.addEventListener("mouseover", function(event){
            $(word).tooltip();
        });

        var new_child_word_span = document.createElement('span');
        new_child_word_span.innerHTML = word;
        new_child.appendChild(new_child_word_span);

        var new_child_delete_i = document.createElement('i');
        new_child_delete_i.className = "bx bx-trash idelete";
        new_child_delete_i.addEventListener("click", function(event) {
            var answer = confirm("Do you want to delete this annotation?");
            if (answer == true) {
                canvas.removeChild(new_child);
            }
            event.stopPropagation();
        });
        new_child.appendChild(new_child_delete_i);

        var new_child_edit_i = document.createElement('i');
        new_child_edit_i.className = "bx bx-edit-alt iedit";
        new_child_edit_i.addEventListener("click", function(event) {
            word = prompt("Enter the updated label:");
            if(word != null && word !== "") {
                new_child_word_span.innerHTML = word;
                new_child.dataset.word = word;
                new_child.dataset.title = word;
            }
            event.stopPropagation();
        });
        new_child.appendChild(new_child_edit_i);
        canvas.appendChild(new_child);
        return new_child;
    }

    var element = null;
    var mouse = { x: 0, y: 0, startX: 0, startY: 0 };

    function initDraw() {
        function setMousePosition(e) {
            var scrollTop = window.pageYOffset || (document.documentElement || document.body.parentNode || document.body).scrollTop;
            var ev = e || window.event; //Moz || IE
            if (ev.pageX) { //Moz
                mouse.x = ev.pageX + window.pageXOffset;
                mouse.y = ev.pageY;
            } else if (ev.clientX) { //IE
                mouse.x = ev.clientX + document.body.scrollLeft;
                mouse.y = ev.clientY;
            }
        };  

        canvas.onmousemove = function (e) {
            var scrollTop = window.pageYOffset || (document.documentElement || document.body.parentNode || document.body).scrollTop;
            setMousePosition(e);
            if (element !== null) {
                element.style.width = Math.abs(mouse.x - mouse.startX) + 'px';
                element.style.height = Math.abs(mouse.y - mouse.startY) + 'px';
                element.style.left = (mouse.x - mouse.startX < 0) ? mouse.x + 'px' : mouse.startX + 'px';
                element.style.top = (mouse.y - mouse.startY < 0) ? (mouse.y - rect.top) + 'px' : (mouse.startY - rect.top) + 'px';
            }
        }

        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape'){
                canvas.removeChild(element);
                element = null;
            }
        });

        canvas.onclick = function (e) {
            
            if (element !== null) {
                var userInput = prompt("Label?");
                if (userInput != null && userInput != "" && userInput !== undefined) {
                    result = userInput;
                    element.children[0].innerText = result;
                    element.dataset.word = result;
                    element.title = result;
                    element = null;
                    canvas.style.cursor = "default";
                    console.log("finished.");
                }
                else {
                    canvas.removeChild(element);
                    element = null;
                }
            } else {
                console.log("begun.");
                mouse.startX = mouse.x;
                mouse.startY = mouse.y;
                element = addDiv("", mouse.x, mouse.y - rect.top, 0, 0);
                canvas.style.cursor = "crosshair";
            }
        }
    }

    initDraw();

    document.getElementById("previous_button").addEventListener('click', function(event) {
        save_bounding_boxes();
        clearCanvas();
        current_index--;
        set_image(current_index);
        if (current_index === 0) {
            document.getElementById("previous_button").style.visibility = "hidden";
        }
        if (current_index < data.length-1) {
            document.getElementById("next_button").style.visibility = "visible";
        }
    });

    document.getElementById("next_button").addEventListener('click', function(event) {
        save_bounding_boxes();
        clearCanvas();
        current_index++;
        set_image(current_index);
        if (current_index === data.length-1) {
            document.getElementById("next_button").style.visibility = "hidden";
        }
        if (current_index > 0) {
            document.getElementById("previous_button").style.visibility = "visible";
        }
    });

    document.getElementById("save_button").addEventListener('click', function(event){
        save_bounding_boxes();
        save_annotations();
        if (confirm('Do you want to save the annotations?')){
            alert("Annotations have been saved! \nEmail has been sent with the annotations!");
          } else {
            alert("Annotations have not been saved!");
          }
    });

    document.getElementById("cancel_button").addEventListener('click', function(event){
        if(confirm("Save progress before you go back?\nCancel will take you back to the home page.")) {
            alert("Saved!");
            window.location = location.origin;
        }
        else {
            window.location = location.origin;
        }
    });

    document.getElementById("instructions_button").addEventListener('click', function(event){
    alert("To draw boxes, click once on the word, drag, and then resize the box accordingly around the desired word to annotate.")
    });

    function save_annotations() {
        let xhr = new XMLHttpRequest();
        let url = location.origin + '/save';
    
        // open a connection
        xhr.open("POST", url, true);

        // Set the request header i.e. which type of content you are sending
        xhr.setRequestHeader("Content-Type", "application/json");

        // Create a state change callback
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                // Print received data from server
                resp = JSON.parse(this.responseText);
                if (resp.status == 'success') {
                    alert("Email has been sent with the annotations!");
                }
            }
        };

        // Converting JSON data to string
        var d_annotations = JSON.stringify({"data": get_annotations()});

        // Sending data with the request
        xhr.send(d_annotations);
    } 
    });