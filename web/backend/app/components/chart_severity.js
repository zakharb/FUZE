class VSeverityChart extends HTMLElement {
    constructor() {
        super();
        this.data_url = "";
        this.data_title = "";
    }

    connectedCallback() {
        this.data_url = this.getAttribute("data_url");
        this.data_title = this.getAttribute("data_title");
        this.render();
    }

    async render() {

        this.innerHTML = `
            <div class="vcard top">
                <div class="vcard-header">
                    <div class="vcard-title">
                        ${this.data_title}
                    </div>
                </div>
                <div class="severity-body">
                </div>
            </div>
        `;
        this.loadData();
    }

    async loadData() {
        const color = {
            0: "bg-secondary",
            1: "bg-warning",
            2: "bg-danger"
        }
        const data = await fetch(this.data_url)
        .then((response) => response.json())
        const body = this.querySelector('.severity-body');
        body.innerHTML = `
            <div class="progress progress-lg">
                <div class="progress-bar ${color[data.bar.color]}" role="progressbar" style="width: ${data.bar.value}%;">
                </div>
            </div>
            ${data.values.map((value) => `
                <div class="severity">
                    <div class="severity-level">${value.title}</div>
                    <div class="severity-value ${value.color}">${value.data}</div>
                </div>
            `).join('')}`
    }
}

customElements.define("v-severitychart", VSeverityChart);


