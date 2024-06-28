class VSummaryChart extends HTMLElement {
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
            <div class="vcard sum ${this.data_color}">
                <div class="vcard-header">
                    <div class="vcard-title">
                        ${this.data_title}
                    </div>
                </div>
                <div class="vcard-body" style="height: 60%; ">
                    <canvas id="myChart"></canvas>
                </div>
            </div>
        `;
        this.createChart();
    }

    getGradient(ctx, chartArea) {

        return gradient;
    }

    async createChart() {
        const chart_data = await fetch(this.data_url)
            .then((response) => response.json())
        const ctx = this.querySelector('#myChart');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: chart_data.labels,
                datasets: [{
                    label: chart_data.label,
                    data: chart_data.data,
                    borderColor: 'rgb(255, 255, 255)',
                    borderWidth: 2,
                    cubicInterpolationMode: 'monotone',
                    tension: 2,

                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        display: false
                    },
                    x: {
                        display: false
                    }
                },
                elements: {
                    point: {
                        radius: 1
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                        align: 'end',
                        labels: {
                            color: '#fff',
                            size: 18,
                            fontStyle: 800,
                            boxWidth: 0
                        }
                    },
                    title: {
                        display: false,
                        color: '#fff',
                        font: {
                            size: 16,
                            family: 'Inter',
                            weight: '600',
                            lineHeight: 1.4
                        },
                        padding: {
                            top: 20
                        }
                    },
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function (tooltipItem, data) {
                            const datasetLabel = data.datasets[tooltipItem.datasetIndex].label || '';
                            const value = tooltipItem.yLabel.toFixed(2);
                            return `1`;
                        }
                    }
                },
                hover: {
                    mode: 'index',
                    intersect: false
                },
                interaction: {
                    mode: "index",
                    intersect: false,
                }
            }
        });
    }
}
customElements.define('v-summarychart', VSummaryChart);
