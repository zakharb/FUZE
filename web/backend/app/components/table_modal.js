const existing_buttons = {
  "close": `
    <button 
    type="button" 
    class="btn btn-outline-secondary btn-save" 
    data-bs-dismiss="modal">
    Close  
    </button>
  `,
  "close_edit": `
    <button 
    type="button" 
    class="btn btn-outline-secondary" 
    data-bs-dismiss="modal">
    Close  
    </button>
  `,
  "save": `
    <button 
    type="button" 
    class="btn btn-primary btn-save" 
    data-url=""
    onclick="saveModal(this)">
    Save
    </button>
  `,
  "delete": `
    <button
    type="button" 
    style="width:50px"
    class="btn btn-outline-secondary" 
    data-url=""
    onclick="delModalRow(this)">
    -
    </button>
  `,
  "add": `
    <button 
    type="button" 
    class="btn btn-outline-secondary" 
    data-url=""
    onclick="addModalRow(this)">
    Add
    </button>
  `,
  "playbook": `
    <button 
    type="button" 
    class="btn btn-primary" 
    data-url=""
    onclick="createPlaybook(this)">
    Playbook
    </button>
  `
}

function makeGeneralInputs(inputs) {
  let general_inputs = '<div class="row" id="general_inputs">'
  for (const [key, value] of Object.entries(inputs)) {
    general_inputs += `
      <div class="mb-3 row justify-content-center">
        <label 
          for="${key}" 
          class="col-sm-2">
          ${value}
        </label>
        <div class="col-sm-7">
          <input 
            type="text" 
            class="form-control" 
            id="${key}" 
            placeholder="${value}"
            value="">
        </div>
      </div>`
  }
  general_inputs += '</div>'
  return general_inputs
}

function makeRowInputs(inputs, modal_edit, rows_name) {
  let rows_inputs = '<div class="pt-2 row d-none" id="row-0">'
  for (const [key, value] of Object.entries(inputs)) {
    rows_inputs += `
      <div class="mb-3 row justify-content-center">
      <label 
    for="${key}" 
    class="col-sm-2">
    ${value}
  </label>
  <div class="col-sm-7">
    <input 
      type="text" 
      class="form-control" 
      id="${key}" 
      placeholder="${value}"
      value="">
  </div>
  </div>
    `
  }
  rows_inputs += `</div>
    <div id="row_inputs_name" class="p-3 col d-none">${rows_name.toUpperCase()}</div>
    <div id="row_inputs" data-rows_name=${rows_name}></div>`;
  return rows_inputs
}

function makeEditRowInputs(inputs, modal_edit, rows_name) {
  let rows_inputs = '<div class="pt-2 row flex-nowrap d-none" id="row-0">'
  for (const [key, value] of Object.entries(inputs)) {
    rows_inputs += `
      <div class="form-floating col">
        <input class="form-control" id="${key}" placeholder="${key}">
        <label for="${key}" class="px-4">${value}</label>
      </div>
    `
  }
    rows_inputs += existing_buttons.delete
    rows_inputs += `</div>
      <div class="p-3">${existing_buttons.add}</div>
      <div class="p-3" id="row_inputs" data-rows_name=${rows_name}></div>`;
  return rows_inputs
}

function makeInputs(inputs, modal_id, rows, rows_name, modal_edit) {
  const general_inputs = makeGeneralInputs(inputs)
  let rows_inputs
  if (modal_edit == "true") {
    rows_inputs = makeEditRowInputs(rows, modal_edit, rows_name)
  } else {
    rows_inputs = makeRowInputs(rows, modal_edit, rows_name)
  }
  let data = `
    <input 
      type="hidden" 
      id="${modal_id}" 
      value="">`
  data += general_inputs
  data += rows_inputs
  return data
}

function makeFooter(modal_edit, modal_buttons) {
  let modal_footer = ''
  if (modal_edit == "true") {
    modal_footer = `
      <div class="modal-footer">
        ${existing_buttons.close_edit}
        ${existing_buttons.save}
      </div>
    `
  } else {
    modal_footer = `<div class="modal-footer">`
    if (modal_buttons) {
      modal_footer += existing_buttons[modal_buttons]
    }
    modal_footer += `${existing_buttons.close}</div>`
  }
  return modal_footer
}

export default class vTableModal extends HTMLElement {
  constructor() {
    super();
    this.modal_title = "";
    this.modal_id = "";
    this.modal_inputs = "";
    this.modal_rows = "";
    this.modal_rows_name = "";
    this.modal_edit = "";
    this.modal_buttons = "";
  }

  connectedCallback() {
    this.modal_title = this.getAttribute("modal_title");
    this.modal_id = this.getAttribute("modal_id");
    this.modal_inputs = JSON.parse(this.getAttribute("modal_inputs"));
    this.modal_rows = JSON.parse(this.getAttribute("modal_rows"));
    this.modal_rows_name = this.getAttribute("modal_rows_name");
    this.modal_edit = this.getAttribute("modal_edit");
    this.modal_buttons = this.getAttribute("modal_buttons");
    this.render();
  }

  render() {
    let table = document.querySelector(".table-responsive")
    let url = table.dataset.url
    const modal_body = makeInputs(this.modal_inputs, this.modal_id, this.modal_rows, this.modal_rows_name, this.modal_edit)
    const modal_footer = makeFooter(this.modal_edit, this.modal_buttons)
    this.innerHTML = `
      <div class="modal modal-xl mt-5" tabindex="-1" data-modal_edit=${this.modal_edit}>
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">${this.modal_title}</h5>
              <div class="modal-status"></div>
            </div>
            <div class="modal-body">
              ${modal_body}
            </div>
            ${modal_footer}
          </div>
        </div>
      </div>
    `;
  }
}

customElements.define("v-table-modal", vTableModal);