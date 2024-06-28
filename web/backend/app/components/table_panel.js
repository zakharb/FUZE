const existing_buttons = {
  'export':`
    <a 
    class="btn btn-outline-secondary mx-1" 
    data-toggle="tooltip" 
    title="Export data"
    onclick="exportData(this)">
    Export
    </a>
    `,
  'add':`
    <a 
    class="btn btn-primary mx-1" 
    data-toggle="tooltip" 
    title="Add"
    onclick="showAddModal(this)">
    Add
    </a>
    `,
    'import': `
    <label 
      class="btn btn-outline-secondary mx-1" 
      data-toggle="tooltip" 
      title="Import data">
      Import
      <input
        type="file"
        accept=".json"
        hidden
        onchange="importData(this)"
      />
    </label>
  `,  
  'filter':`
    <a 
    class="btn btn-outline-secondary mx-1" 
    data-toggle="tooltip" 
    title="Filter"
    data-bs-toggle="offcanvas" 
    data-bs-target="#offcanvasRight" 
    aria-controls="offcanvasRight"
    >
    Filter
    </a>
  `,
  'delete':`
    <a 
    class="btn btn-danger mx-1" 
    title="Delete"
    onclick="deleteRow(this)">
    Delete
    </a>
  `,
  'save':`
    <a 
    class="btn btn-outline-secondary mx-1" 
    title="Save"
    onclick="">
    Save
    </a>
  `,
  'copy':`
    <a 
    class="btn btn-outline-secondary mx-1" 
    title="Copy"
    onclick="copyRow(this)">
    Copy
    </a>
  `,
}

export default class vTablePanel extends HTMLElement {

  
    constructor() {
      super();
      this.table_name = "";
      this.panel1_buttons = [];
      this.panel2_buttons = "";
    }
  
    connectedCallback() {
      this.table_name = this.getAttribute("table_name");
      this.panel1_buttons = JSON.parse(this.getAttribute("panel1_buttons"));
      this.panel2_buttons = JSON.parse(this.getAttribute("panel2_buttons"));
      this.render();
    }

    handleFileSelect(event) {
      console.log(1)
      const formData = new FormData();
      formData.append("file", event.target.files[0]);
      fetchCollectorRuleImport(setData, formData)
    }

    render() {
      const panel1_buttons = this.panel1_buttons.map(buttonName => existing_buttons[buttonName]).join('\n');
      const panel2_buttons = this.panel2_buttons.map(buttonName => existing_buttons[buttonName]).join('\n');
      this.innerHTML = `
        <div class="row mx-4 mt-4" id="panel_one">
          <div class="col-4 d-flex">
            <h4>
              ${this.table_name}
            </h4>
            <h7 class="px-2">
              <span 
                class="badge bg-warning"
                id="table_count">
              </span>
            </h7>
          </div>
          <div class="col d-flex flex-row-reverse mb-5">
            ${panel1_buttons}
            <input
              class="form-control mx-3" 
              type="text" 
              placeholder="Search..." 
              onkeyup="searchRow(this.value)"
              id="search_input">
          </div>                          
        </div>  
        <div class="row mx-4 mt-4 d-none" id="panel_two">
          <div class="col-4 d-flex">
            <h4>
              Selected
            </h4>
            <h7 class="px-2">
            <span 
                class="badge bg-danger"
                id="checked_count">
              </span>
            </h7>
          </div>
          <div class="col d-flex flex-row-reverse mb-5">
            ${panel2_buttons}
          </div>          
        </div>
  
      `;
    }
  }
  
  customElements.define("v-table-panel", vTablePanel);