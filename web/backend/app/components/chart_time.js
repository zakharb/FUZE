class VTimeChart extends HTMLElement {
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
    render() {
        this.innerHTML = `
            <div class="vcard chart">
                <div class="vcard-header">
                    <div class="vcard-title">
                        ${this.data_title}
                    </div>
                </div>
                <div class="vcard-body">
                    <canvas style="width: 100%; height: 100%" id="myChart"></canvas>
                </div>
            </div>
        `;

        this.createChart();
    }


    async createChart() {
        const chart_data = await fetch(this.data_url)
            .then((response) => response.json())
        const ctx = this.querySelector('#myChart');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: chart_data.labels,
                datasets: chart_data.datasets.map((dataset) => {
                    return({'label': dataset.label,
                    'data': dataset.data,
                    'cubicInterpolationMode': 'monotone',
                    'tension': 2,
                    'backgroundColor': dataset.color,
                    'borderColor': dataset.color,
                    'borderWidth': dataset.border_width,
                    'fill': dataset.fill})
                })
            },
            options: {
                onClick: function (evt, element) {
                    if (element.length > 0) {
                        const selectedIndex = element[0].index;
                        const selectedValue = data.labels[selectedIndex];
                        const queryParams = new URLSearchParams({ [filter]: selectedValue }).toString();
                        navigate(`${link}?${queryParams}`);
                    }
                },
                maintainAspectRatio: false,

                scales: {
                    y: {
                        display: false,

                        min: 0,
                        ticks: {
                            stepSize: 25
                        },
                        grid: {
                            display: false
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgb(53, 53, 53)',
                            display: false
                        },
                        ticks: {
                            display: false
                        }

                    }
                },
                elements: {
                    point: {
                        radius: 0
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        align: 'end',
                        labels: {
                            color: 'rgb(221, 221, 221)',
                            boxWidth: 8,
                            boxHeight: 8,
                            usePointStyle: true,
                            font: {
                                size: 12,
                                weight: '500'
                            }
                        }
                    },
                    title: {
                        display: false,
                    }
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function (tooltipItem, data) {
                            const datasetLabel = data.datasets[tooltipItem.datasetIndex].label || '';
                            const value = tooltipItem.yLabel.toFixed(2);
                            return `${datasetLabel}: ${value}%`;
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
customElements.define('v-timechart', VTimeChart);
