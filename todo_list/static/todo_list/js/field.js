let field_count = 0;

// add input field to the form
function add_field() {
    let field = document.createElement("div");
    field.setAttribute("id", "form_field_new_"+field_count);
    field.setAttribute("class", "sticker long");

    let heading = document.createElement("h1");
    heading.innerHTML = "Add task";

    let name_label = document.createElement("label");
    name_label.setAttribute("class", 'sticker-label');
    name_label.setAttribute("for", "name-field");
    name_label.innerHTML = "Task name";

    let name_field = document.createElement("input");
    name_field.setAttribute("id", "name-field");
    name_field.setAttribute("type", "text");
    name_field.setAttribute("name", "fields_new");
    name_field.setAttribute("class", "");
    name_field.setAttribute("required", "true");

    let text_label = document.createElement("label");
    text_label.setAttribute("class", 'sticker-label');
    text_label.setAttribute("for", "text-field");
    text_label.innerHTML = "Task description";

    let text_field = document.createElement("textarea");
    text_field.setAttribute("id", "text-field");
    text_field.setAttribute("type", "text");
    text_field.setAttribute("name", "descriptions_new");
    text_field.setAttribute("class", "");

    let deadline_label = document.createElement('label')
    deadline_label.setAttribute("class", 'sticker-label');
    deadline_label.setAttribute('for', 'deadline')
    deadline_label.innerHTML = 'Deadline'

    let deadline = document.createElement('input')
    deadline.setAttribute('id', 'deadline')
    deadline.setAttribute('type','date')
    deadline.setAttribute('name', 'deadlines_new')

    let hr = document.createElement("hr");

    let remove_button = document.createElement("button");
    remove_button.setAttribute("type", "button");
    remove_button.setAttribute("class", "sticker-button");
    remove_button.setAttribute("onclick", "remove_field('form_field_new_"+field_count+"')");
    remove_button.innerHTML = "Remove";
    
    document.getElementById("task").appendChild(field);
    
    let this_field = document.getElementById("form_field_new_"+field_count);

    this_field.appendChild(heading);

    this_field.appendChild(name_label);

    this_field.appendChild(name_field);

    this_field.appendChild(text_label);

    this_field.appendChild(text_field);

    this_field.appendChild(deadline_label);

    this_field.appendChild(deadline);

    
    this_field.appendChild(hr);
    this_field.appendChild(remove_button);
    field_count++;
}

function remove_field(id) {
    let field = document.getElementById(id);
    // console.log(field.parentNode)
    field.parentNode.removeChild(field);
}

