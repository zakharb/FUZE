class VTotalCard extends HTMLElement {
    constructor() {
        super();
        this.data_url = "";
        this.data_title = "";
        this.data_color = "";
    }

    connectedCallback() {
        this.data_url = this.getAttribute("data_url");
        this.data_title = this.getAttribute("data_title");
        this.data_color = this.getAttribute("data_color");
        this.render();
    }

    render() {
        this.innerHTML = `
            <div class="vcard">
                <div class="vcard-header">
                    <div class="vcard-title">
                        ${this.data_title}
                    </div>
                    <div class="vcard-subtitle"></div>
                </div>
                <div class="total-body">
                    <span class="circle ${this.data_color}"></span>
                </div>
            </div>
        `;
        this.loadData();
    }

    async loadData() {
        const data = await fetch(this.data_url)
        .then((response) => response.json())
        const subtitle = this.querySelector('.vcard-subtitle');
        subtitle.innerHTML = data.change + "%";
        const body = this.querySelector('.total-body');
        body.innerHTML += data.total;
    }
}

customElements.define("v-total-card", VTotalCard);

