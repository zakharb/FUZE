class VRadarChart extends HTMLElement {
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
                    <canvas id="myChart"></canvas>
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
            type: 'radar',
            data: {
                labels: chart_data.labels,
                datasets: chart_data.datasets
            },
            options: {
                responsive: true,
                onClick: function (evt, element) {
                    if (element.length > 0) {
                        const selectedIndex = element[0].index;
                        const selectedValue = data.labels[selectedIndex];
                        const queryParams = new URLSearchParams({ [filter]: selectedValue }).toString();
                        navigate(`${link}?${queryParams.toLowerCase()}`);
                    }
                },
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom',
                        labels: {
                            color: 'rgb(221, 221, 221)'
                        },
                    },
                    title: {
                        display: false,
                    }
                },
                scales: {
                    r: {
                        ticks: {
                            display: false
                        },
                        angleLines: {
                            color: 'rgba(65, 65, 65, 0.5)',
                            lineWidth: 2,
                        },
                        grid: {
                            color: 'rgba(65, 65, 65, 0.5)',
                            lineWidth: 1,
                        },
                        pointLabels: {
                            color: 'rgb(221, 221, 221)'
                        }
                    },
                },
                elements: {
                    point: {
                        radius: 0,
                        pointHitRadius: 10
                    },
                    line: {
                        tension: 0.2,
                    },
                },
                scale: {
                    r: {
                        min: 0,
                        beginAtZero: true,
                        angleLines: {
                           display: true,
                        }
                    }
                }
            }
        });
    }
}
customElements.define('v-radarchart', VRadarChart);
