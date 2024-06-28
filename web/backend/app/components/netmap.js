class VNetmap extends HTMLElement {
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
    <div style="width: 100%; height: 900px">
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
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [0, 0, width, height])
            .attr("style", "max-width: 100%; height: auto;");
        const color = {
          "unknown": "rgb(255, 69, 58)",
          "offline": "rgb(255, 159, 10)",
          "online": "rgb(50, 215, 75)",
          "tap": "rgb(152, 152, 157)"
        };
      
        // The force simulation mutates links and nodes, so create a copy
        // so that re-evaluating this cell produces the same result.
        const links = chart_data.links.map(d => ({...d}));
        const nodes = chart_data.nodes.map(d => ({...d}));
      
        // Create a simulation with several forces.
        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.id).distance(75))
            .force("charge", d3.forceManyBody())
            .force("center", d3.forceCenter(width / 2, height / 2));
      
        // Add a line for each link, and a circle for each node.
        const link = svg.append("g")
            .attr("stroke", 'rgb(152, 152, 157)')
            .attr("stroke-opacity", 0.6)
          .selectAll("line")
          .data(links)
          .join("line")
            .attr("stroke-width", d => Math.sqrt(d.value));
      
        // const node = svg.append("g")
        //   .selectAll("circle")
        //   .data(nodes)
        //   .join("circle")
        //     .attr("r", d => d.radius)
            // .attr("fill", d => color[d.status]);
// Inside createChart method

const node = svg.append("g")
  .selectAll("foreignObject") // Use foreignObject to embed HTML content
  .data(nodes)
  .join("foreignObject")
    .attr("width", d => d.radius * 2) // Set the width of the foreignObject
    .attr("height", d => d.radius * 2) // Set the height of the foreignObject
    .attr("x", d => d.x)
    .attr("y", d => d.y - d.radius)
    .attr("x1", d => d.x)
    .attr("y1", d => d.y)
    .html(d => `<i class="fab fa-js"  style="font-size: ${d.radius}px;"></i>`)
    // <i class="fab fa-${getFontAwesomeClass(d.status)}" style="font-size: ${d.radius}px;"></i>`);

  // Function to get the Font Awesome class based on the node status
  function getFontAwesomeClass(status) {
    switch (status) {
      case "unknown":
        return "question-circle";
      case "offline":
        return "times-circle";
      case "online":
        return "check-circle";
      case "tap":
        return "hand-pointer";
      default:
        return "";
    }
  }
      
        node.append("title")
            .text(d => d.name);

            
        // Add a drag behavior.
        node.call(d3.drag()
              .on("start", dragstarted)
              .on("drag", dragged)
              .on("end", dragended));
        
        // Set the position attributes of links and nodes each time the simulation ticks.
        simulation.on("tick", () => {
          link
              .attr("x1", d => d.source.x)
              .attr("y1", d => d.source.y)
              .attr("x2", d => d.target.x)
              .attr("y2", d => d.target.y);
      
          node
              .attr("cx", d => d.x)
              .attr("cy", d => d.y);
        });
      
        // Reheat the simulation when drag starts, and fix the subject position.
        function dragstarted(event) {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          event.subject.fx = event.subject.x;
          event.subject.fy = event.subject.y;
        }
      
        // Update the subject (dragged node) position during drag.
        function dragged(event) {
          event.subject.fx = event.x;
          event.subject.fy = event.y;
        }
      
        // Restore the target alpha so the simulation cools after dragging ends.
        // Unfix the subject position now that it’s no longer being dragged.
        function dragended(event) {
          if (!event.active) simulation.alphaTarget(0);
          event.subject.fx = null;
          event.subject.fy = null;
        }
  }

}
customElements.define('v-netmap', VNetmap);
