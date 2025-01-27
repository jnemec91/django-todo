// this variable stores current number of fields in the form, it is used to create unique id for each field. Doesnt go back on field removal.
let field_count = 0;


// this function is used to add new field to the form. It creates new div element with all the necessary elements and appends it to the form.
// it also creates small field description that is used to display task name and description in the list of tasks when field form is minimized.
function add_field() {

    let task_field = document.createElement("div");
    task_field.setAttribute("id", "task_"+field_count);

    let modal_box =  document.createElement("div");
    modal_box.setAttribute("id", "modal_"+field_count+"_wrapper")
   
    const new_field = `
    <div id="form_field_new_${field_count}" class="sticker long task-field">
    <h1>New task</h1><label class="sticker-label" for="name-field_${field_count}">Task name</label>
    <input id="name-field_${field_count}" type="text" name="fields_new" required="true">
    <label class="sticker-label" for="text-field_${field_count}">Task description</label>
    <textarea id="text-field_${field_count}" type="text" name="descriptions_new"></textarea>
    <label class="sticker-label" for="deadline_${field_count}">Deadline</label>
    <input id="deadline_${field_count}" type="date" name="deadlines_new"><hr>
    <button type="button" class="sticker-button top-sticker-button" onclick="showModal('remove_field_modal_${field_count}','modal-wrap')"><i class="fa-solid fa-xmark"></i></button>
    <button type="button" class="sticker-button" onclick="toggle_fields('${field_count}');">Add</button>
    </div>
    `;

    const delete_modal = `
    <div class="share-modal" id="remove_field_modal_${field_count}">
        <div class="modal-header">
            <h2>Delete field</h2>
        </div>
        <div class="modal-body">
            <p>Are you sure you want to delete this field?</p>

            <button type="button" class="sticker-button" onclick="hideModal('remove_field_modal_${field_count}','modal-wrap');setTimeout(remove_field('form_field_new_${field_count}'),1000);">Delete</button>
            <button class="sticker-button" onclick="hideModal('remove_field_modal_${field_count}','modal-wrap');">Close</button>
        </div>
    </div>
    `;


    const small_field_description = `
    <div id="small_field_description_${field_count}" class="sticker long field-hidden">
    <h1>asdadas</h1>
    <p id="description_text"></p>
    <p id="description_deadline">None</p>
    <button type="button" class="sticker-button top-sticker-button" onclick="toggle_fields('${field_count}');"><i class="fa-regular fa-window-maximize"></i></button>
    </div>
    `;


    let task =  document.getElementById("task");
    let pagecont = document.getElementById("pagecont")
    task.appendChild(task_field);
    pagecont.appendChild(modal_box);

    task_field = document.getElementById("task_"+field_count);
    task_field.innerHTML = new_field + small_field_description;

    modals_box= document.getElementById("modal_"+field_count+"_wrapper")
    modals_box.innerHTML = delete_modal

    // scrolling to the newly created field
    let this_field = document.getElementById("task_"+field_count);
    window.scrollTo({ top: this_field.offsetTop-50, behavior: 'smooth'});

    
    toggle_add_button();

    // incrementing field count
    field_count++;


};
// end of add_field function


// this function is used to remove field from the form. It takes id of the field as an argument and removes it from the form.
function remove_field(id) {
    let field = document.getElementById(id);
    field.parentNode.removeChild(field);
    
    toggle_add_button();
};
// end of remove_field function


// this function is used to toggle between field form and small field description. It takes id of the field as an argument and toggles between them.
// it also changes the content of small field description to match the content of the field form and scrolls to the field form when form is maximized 
// or to the small field description when it is minimized.
function toggle_fields(id) {
    let field1 = document.getElementById('form_field_new_'+id);
    if (!(field1)) {
        field1 = document.getElementById('form_field_'+id);
    }

    let field2 = document.getElementById('small_field_description_'+id);

    let headingElement = field2.querySelector("h1");
    let heading_text = field1.querySelector("#name-field_"+id);

    let textElement = field2.querySelector("#description_text");
    let text = field1.querySelector("#text-field_"+id);

    let deadlineElement = field2.querySelector("#description_deadline");
    let deadline = field1.querySelector("#deadline_"+id);

    // check if task name is empty, so user cant add  empty tasks.
    if (document.getElementById("name-field_"+id).value == "") {
        alert("Task name cannot be empty!");
    }
    else{
        headingElement.innerHTML = heading_text.value;
        textElement.innerHTML = text.value;
        deadlineElement.innerHTML = deadline.value;
    
        field1.classList.toggle('field-hidden');
        field2.classList.toggle('field-hidden');
    
        if (field1.classList.contains('field-hidden')) {
            field2.focus(); 
            window.scrollTo({ top: field2.offsetTop });
            toggle_add_button();
        }
        else {
            field1.focus();
            window.scrollTo({ top: field1.offsetTop, behavior: 'smooth'});
            toggle_add_button();
        }
        
    }
    
};

// this function is used to hide save and add buttons when field form is maximized and show them when it is minimized.
function toggle_add_button() {
    let add_button = document.getElementById("add-field-button");
    add_button.classList.toggle('field-hidden');
    let save_button = document.getElementById("save-button");
    save_button.classList.toggle('field-hidden');   
}