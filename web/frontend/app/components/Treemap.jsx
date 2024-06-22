import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3'; // Import D3.js library

const ClusterTreeComponent = ({ data }) => {
  const svgRef = useRef(null);

  useEffect(() => {
    if (data && svgRef.current) {
      const width = 1528;
      const dx = 15;
      const root = d3.hierarchy(data);
      const dy = width / (root.height + 1);

      const tree = d3.cluster().nodeSize([dx, dy]);

      root.sort((a, b) => d3.ascending(a.data.name, b.data.name));
      tree(root);

      let x0 = Infinity;
      let x1 = -x0;
      root.each(d => {
        if (d.x > x1) x1 = d.x;
        if (d.x < x0) x0 = d.x;
      });

      const height = x1 - x0 + dx * 2;

      const svg = d3.select(svgRef.current)
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [-dy / 3, x0 - dx, width, height])
        .attr("style", "max-width: 100%; height: auto; font: 14px sans-serif;");

      const link = svg.append("g")
        .attr("fill", "none")
        .attr("stroke", "#555")
        .attr("stroke-opacity", 0.4)
        .attr("stroke-width", 1.5)
        .selectAll()
        .data(root.links())
        .join("path")
        .attr("d", d3.linkHorizontal()
          .x(d => d.y)
          .y(d => d.x));

      const node = svg.append("g")
        .attr("stroke-linejoin", "round")
        .attr("stroke-width", 3)
        .selectAll()
        .data(root.descendants())
        .join("g")
        .attr("transform", d => `translate(${d.y},${d.x})`);

      node.append("circle")
        .attr("fill", d => d.children ? "#555" : "#999")
        .attr("r", 2.5);

      node.append("text")
        .attr("dy", "0.31em")
        .attr("x", d => d.children ? -6 : 6)
        .attr("text-anchor", d => d.children ? "end" : "start")
        .text(d => d.data.name)
        .attr("stroke", "white")
        .attr("paint-order", "stroke");
    }
  }, [data]);

  return (
    <svg ref={svgRef}></svg>
  );
};

export default ClusterTreeComponent;
