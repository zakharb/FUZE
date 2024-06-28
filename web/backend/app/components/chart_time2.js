class VTimeChart extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });

        this.data = [
            {
                label: 'Line 1',
                values: [
                    { time: '2023-10-16T12:00:00', value: 70 },
                    { time: '2023-10-16T13:00:00', value: 60 },
                    { time: '2023-10-16T14:00:00', value: 65 },
                    { time: '2023-10-16T15:00:00', value: 65 },
                    { time: '2023-10-16T16:00:00', value: 75 },
                    { time: '2023-10-16T17:00:00', value: 62 },
                    { time: '2023-10-16T18:00:00', value: 78 },
                    { time: '2023-10-16T19:00:00', value: 65 },
                    { time: '2023-10-16T20:00:00', value: 75 },
                    { time: '2023-10-17T12:00:00', value: 70 },
                    { time: '2023-10-17T13:00:00', value: 60 },
                    { time: '2023-10-17T14:00:00', value: 65 },
                    { time: '2023-10-17T15:00:00', value: 65 },
                    { time: '2023-10-17T16:00:00', value: 75 },
                    { time: '2023-10-17T17:00:00', value: 62 },
                    { time: '2023-10-17T18:00:00', value: 78 },
                    { time: '2023-10-17T19:00:00', value: 65 },
                    { time: '2023-10-17T20:00:00', value: 75 },
                    { time: '2023-10-18T12:00:00', value: 70 },
                    { time: '2023-10-18T13:00:00', value: 60 },
                    { time: '2023-10-18T14:00:00', value: 65 },
                    { time: '2023-10-18T15:00:00', value: 65 },
                    { time: '2023-10-18T16:00:00', value: 75 },
                    { time: '2023-10-18T17:00:00', value: 62 },
                    { time: '2023-10-18T18:00:00', value: 78 },
                    { time: '2023-10-18T19:00:00', value: 65 },
                    { time: '2023-10-18T20:00:00', value: 75 },
                    // Add more data points for Line 1
                ],
                color: 'rgb(152, 152, 157)'
            },
            {
                label: 'Line 2',
                values: [
                    { time: '2023-10-16T12:00:00', value: 15 },
                    { time: '2023-10-16T13:00:00', value: 25 },
                    { time: '2023-10-16T14:00:00', value: 20 },
                    { time: '2023-10-16T15:00:00', value: 20 },
                    { time: '2023-10-16T16:00:00', value: 20 },
                    { time: '2023-10-16T17:00:00', value: 23 },
                    { time: '2023-10-16T18:00:00', value: 20 },
                    { time: '2023-10-16T19:00:00', value: 25 },
                    { time: '2023-10-16T20:00:00', value: 20 },
                    { time: '2023-10-16T12:00:00', value: 15 },
                    { time: '2023-10-16T13:00:00', value: 25 },
                    { time: '2023-10-16T14:00:00', value: 20 },
                    { time: '2023-10-16T15:00:00', value: 20 },
                    { time: '2023-10-16T16:00:00', value: 20 },
                    { time: '2023-10-16T17:00:00', value: 23 },
                    { time: '2023-10-16T18:00:00', value: 20 },
                    { time: '2023-10-16T19:00:00', value: 25 },
                    { time: '2023-10-16T20:00:00', value: 20 },
                    { time: '2023-10-16T12:00:00', value: 15 },
                    { time: '2023-10-16T13:00:00', value: 25 },
                    { time: '2023-10-16T14:00:00', value: 20 },
                    { time: '2023-10-16T15:00:00', value: 20 },
                    { time: '2023-10-16T16:00:00', value: 20 },
                    { time: '2023-10-16T17:00:00', value: 23 },
                    { time: '2023-10-16T18:00:00', value: 20 },
                    { time: '2023-10-16T19:00:00', value: 25 },
                    { time: '2023-10-16T20:00:00', value: 20 },
                    // Add more data points for Line 2
                ],
                color: "rgb(106, 196, 220)"
            },
            {
                label: 'Line 3',
                values: [
                    { time: '2023-10-16T12:00:00', value: 5 },
                    { time: '2023-10-16T13:00:00', value: 10 },
                    { time: '2023-10-16T14:00:00', value: 7 },
                    { time: '2023-10-16T15:00:00', value: 3 },
                    { time: '2023-10-16T16:00:00', value: 7 },
                    { time: '2023-10-16T17:00:00', value: 8 },
                    { time: '2023-10-16T18:00:00', value: 2 },
                    { time: '2023-10-16T19:00:00', value: 7 },
                    { time: '2023-10-16T20:00:00', value: 3 },
                    { time: '2023-10-16T12:00:00', value: 5 },
                    { time: '2023-10-16T13:00:00', value: 10 },
                    { time: '2023-10-16T14:00:00', value: 7 },
                    { time: '2023-10-16T15:00:00', value: 3 },
                    { time: '2023-10-16T16:00:00', value: 7 },
                    { time: '2023-10-16T17:00:00', value: 8 },
                    { time: '2023-10-16T18:00:00', value: 2 },
                    { time: '2023-10-16T19:00:00', value: 7 },
                    { time: '2023-10-16T20:00:00', value: 3 },
                    { time: '2023-10-16T12:00:00', value: 5 },
                    { time: '2023-10-16T13:00:00', value: 10 },
                    { time: '2023-10-16T14:00:00', value: 7 },
                    { time: '2023-10-16T15:00:00', value: 3 },
                    { time: '2023-10-16T16:00:00', value: 7 },
                    { time: '2023-10-16T17:00:00', value: 8 },
                    { time: '2023-10-16T18:00:00', value: 2 },
                    { time: '2023-10-16T19:00:00', value: 7 },
                    { time: '2023-10-16T20:00:00', value: 3 },
                    // Add more data points for Line 3
                ],
                color: "rgb(10, 132, 255)"

            }
        ];
    }

    connectedCallback() {
        this.render();
    }

    render() {
        this.shadowRoot.innerHTML = `
            <div style="height: 100%; width: 100%" id="chart-container">
            </div>
        `;

        this.createChart();
    }

    createChart() {
        const container = this.shadowRoot.querySelector('#chart-container');
    
        const width = container.clientWidth;
        const height = container.clientHeight;
    
        const svg = d3.select(container).append('svg')
            .attr('width', width)
            .attr('height', height);
    
        const margin = { top: 15, right: 5, bottom: 5, left: 5 };
        const innerWidth = width - margin.left - margin.right;
        const innerHeight = height - margin.top - margin.bottom;
    
        const xScale = d3.scaleTime()
            .domain(d3.extent(this.data[0].values, d => new Date(d.time)))
            .range([0, innerWidth]);
    
        const yScale = d3.scaleLinear()
            .domain([0, d3.max(this.data.flatMap(d => d.values.map(v => v.value)))])
            .range([innerHeight, 0]);
    
        const area = d3.area()
            .x(d => xScale(new Date(d.time)))
            .y0(innerHeight) // The baseline
            .y1(d => yScale(d.value));
    
        const chart = svg.append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);
    
        const xAxisTooltip = chart.append('g')
            .attr('class', 'x-axis-tooltip')
            .style('display', 'none');

        xAxisTooltip.append('text')
            .attr('class', 'x-axis-text')
            .attr('text-anchor', 'middle')
            .style('fill', 'white');

        this.data.forEach((series, index) => {
            chart.append('path')
                .datum(series.values)
                .attr('class', 'area')
                .attr('d', area)
                .style('fill', series.color)
                .on('mouseenter', function () {
                    d3.select(this).style('opacity', 0.7);
                    chart.selectAll('.tooltip-text').remove();
                    series.values.forEach((dataPoint) => {
                        const xPosition = xScale(new Date(dataPoint.time));
                        const yPosition = yScale(dataPoint.value);
                        chart.append('text')
                            .attr('class', 'tooltip-text')
                            .attr('x', xPosition)
                            .attr('y', yPosition - 10)
                            .text(dataPoint.value.toFixed(0))
                            .style('text-anchor', 'middle')
                            .style('fill', 'white')
                            .style('font-size', '10px');
                    });
                })
                .on('mouseleave', function () {
                    d3.select(this).style('opacity', 1);
                    chart.selectAll('.tooltip-text').remove();
                    xAxisTooltip.style('display', 'none');

                })
                .on('mousemove', function(event) {
                    const xPosition = d3.pointer(event)[0];
                    const dateValue = xScale.invert(xPosition);
                    const xValue = d3.timeFormat('%Y-%m-%d %H:%M')(dateValue);
                    xAxisTooltip.select('.x-axis-text')
                        .text(xValue)
                        .attr('x', xPosition)
                        .attr('y', innerHeight + 20)
                        .style('font-size', '10px');
                    xAxisTooltip.style('display', 'block');
                });
        });
    }
}

customElements.define('v-timechart', VTimeChart);
