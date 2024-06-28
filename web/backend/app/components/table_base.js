export class vTable extends HTMLElement {
  constructor() {
    super();
    this.table_id = "";
    this.table_name = "";
    this.table_url = "";
    this.table_row_id = "";
    this.table_tds = "";
    this.panel1_buttons = "";
    this.panel2_buttons = "";
  }

  connectedCallback() {
    this.table_id = this.getAttribute("table_id");
    this.table_name = this.getAttribute("table_name");
    this.table_url = this.getAttribute("table_url");
    this.table_row_id = this.getAttribute("table_row_id");
    this.table_tds = JSON.parse(this.getAttribute("table_tds"));
    this.panel1_buttons = this.getAttribute("panel1_buttons");
    this.panel2_buttons = this.getAttribute("panel2_buttons");
    this.render();
    loadTable(this.table_id)
  }

  render() {
    const thead = makeThead(this.table_tds)
    this.innerHTML = `
      <div class="table-responsive" 
           id="${this.table_id}"
           data-url="${this.table_url}"
           data-rowid="${this.table_row_id}">
        <v-table-panel
          table_name=${this.table_name}
          panel1_buttons=${this.panel1_buttons}
          panel2_buttons=${this.panel2_buttons}
        ></v-table-panel>
        <table class="table">
          <thead>
            <tr>
              ${thead}
            </tr>    
          </thead>
          <tbody>
          </tbody>
        </table>
      </div>
    `;
  }
}

customElements.define("v-table", vTable);