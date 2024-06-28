class VBubbleChart extends HTMLElement {
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
        <div class="vcard-body" id="chart-container">
        </div>
      </div>
    `;

    this.createChart();
  }


  async createChart() {
    const chart_data = await fetch(this.data_url)
      .then((response) => response.json())

    const container = this.querySelector('#chart-container');
    const width = container.clientWidth;
    const height = container.clientHeight;

    const svg = d3.select(container).append('svg')
      .attr('width', width)
      .attr('height', height);

    const colorDict = {
      0: 'rgb(152, 152, 157)',
      1: 'rgb(255, 159, 10)',
      2: 'rgb(255, 69, 58)',
    };

    function generateRandomCoordinates(radius, existingCoordinates) {
      const x = Math.random() * (width - 5 * radius) + radius;
      const y = Math.random() * (height - 5 * radius) + radius;

      const collision = existingCoordinates.some(coord => {
        const dx = x - coord.x;
        const dy = y - coord.y;
        const distance = Math.sqrt(dx * dx + dy * dy + 1);
        return distance < radius + coord.radius;
      });

      if (collision) {
        return generateRandomCoordinates(radius, existingCoordinates);
      } else {
        return { x, y };
      }
    }
    console.log(chart_data)
    chart_data.forEach(d => {
      const { x, y } = generateRandomCoordinates(d.radius, chart_data);
      d.x = x;
      d.y = y;
    });

    const simulation = d3.forceSimulation(chart_data)
      .force("x", d3.forceX().x(d => d.x).strength(0.05))
      .force("y", d3.forceY().y(d => d.y).strength(0.05))
      .force("collide", d3.forceCollide(d => d.radius + 2));

      const bubbles = svg.selectAll("circle")
      .data(chart_data)
      .enter()
      .append("circle")
      .attr("r", d => d.radius)
      .attr("fill", d => colorDict[d.color]);


      svg.selectAll("text")
      .data(chart_data)
      .enter()
      .append("text")
      .attr("x", d => d.x)
      .attr("y", d => d.y - d.radius - 10)
      .attr("dy", 5)
      .attr("text-anchor", "middle")
      .text(d => d.name)
      .style("fill", "white");
    

    bubbles.on("mouseover", (event, d) => {
      const tooltip = svg.append("text")
        .attr("x", d.x)
        .attr("y", d.y + d.radius*2 )
        .attr("text-anchor", "middle")
        .attr("class", "tooltip2")
        .text(`${d.value}`)
        .style("font-size", "16px")
        .style("fill", "white");
    });

    bubbles.on("mouseout", () => {
      svg.select(".tooltip2").remove();
    });

    simulation.on("tick", () => {
      bubbles
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
    });
    const drag = d3.drag()
    .on("start", (event, d) => {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;

    })
    .on("drag", (event, d) => {
      d.fx = event.x;
      d.fy = event.y;
      svg.select(".tooltip2").remove();
      bubbles
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
      svg.selectAll("text")
        .filter(data => data === d)
        .attr("x", d.x)
        .attr("y", d.y - d.radius - 10);
    })
  bubbles.call(drag);
  }

}
customElements.define('v-bubblechart', VBubbleChart);
