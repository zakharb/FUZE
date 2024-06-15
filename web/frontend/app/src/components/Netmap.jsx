import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import ForceGraph3D from '3d-force-graph';
import { useNavigate } from 'react-router-dom';
import SpriteText from 'three-spritetext';
import DrawerFilter from "../components/DrawerFilter"
import { useState } from 'react';
import { Drawer, List, ListItem, TextField, Button, Typography } from '@mui/material';


const GraphComponent = ({ data , link}) => {

  // Date time now and -1 week
  const now = new Date();
  const oneWeekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
  const [startDate, setStartDate] = useState(oneWeekAgo.toISOString().slice(0, 16));
  const [endDate, setEndDate] = useState(now.toISOString().slice(0, 16));


  const [filters, setFilters] = useState({
    'Source Name': '',
    'Description': '',
    'Group': '',
  });



  const [openDrawer, setOpenDrawer] = React.useState(false);
  const [filterValues, setFilterValues] = React.useState({});

  const handleOpenDrawer = () => {
    setOpenDrawer(true);
  };

  const handleCloseDrawer = () => {
    setOpenDrawer(false);
  };

  const handleFilterChange = (field) => (event) => {
    setFilters((prevState) => ({
      ...prevState,
      [field]: event.target.value,
    }));
  };

  const handleApplyFilters = () => {
    applyFilters(filters);
    setOpenDrawer(false);
  };



  const navigate = useNavigate();
  const graphRef = useRef(null);

  useEffect(() => {
    if (graphRef.current) {
      const graphInstance = ForceGraph3D()(graphRef.current)
        .backgroundColor('rgba(0, 255, 0, 0.0)')
        .width(1300)
        .height(800)
        .nodeLabel(d => {
            const formattedName = d.name;
            return `<span style="color: gray"><b>${formattedName}</b></span>`;
        })
        .linkOpacity(1)
        .linkColor(d => {
          if (d.severity === "high") {
            return "#dc143c";
          } else if (d.severity === "medium") {
            return '#ffb648'
          } else {
            return '#00aaff';
          }
        })
        .nodeThreeObject((node) => {
          var radius;
          const name_length = parseInt(node.name.length);
          if (name_length == 1) {
            radius = 5;
          } else if (name_length < 5) {
            radius = 5;
          } else {
            radius = 5;
          }
          const nodeObject = new THREE.Mesh(
            new THREE.SphereGeometry(radius),
            new THREE.MeshBasicMaterial({ color: '#007fff' })
          );
          if (node.status === "warning") {
            nodeObject.material.color.set('#ffb648');
          }
          if (node.status === "error") {
            nodeObject.material.color.set('#dc143c');
          }
          if (node.status === "secondary") {
            nodeObject.material.color.set('#808080');
          }
          return nodeObject;
        })
        .onNodeClick(handleOpenDrawer);
         // Set the desired link distance here      
        // });
      graphInstance.graphData(data);
      graphInstance.d3VelocityDecay(0.8);
    }

  
  }, []);
  return (
    <div id="3d-graph" ref={graphRef}>



<Drawer anchor="right" open={openDrawer} onClose={handleCloseDrawer}>
  <div style={{ width: 500, marginTop: 100 }}>
    <div style={{ display: 'flex', justifyContent: 'center', marginTop: 'auto' }}>
      <Button variant="contained" color="primary" onClick={handleApplyFilters}>
        Apply
      </Button>
    </div>
    <List>
      {Object.entries(filters).map(([filterName, filterLabel]) => (
        <ListItem key={filterName}>
          <TextField
            label={filterName}
            name={filterName}
            value={filters[filterName] || ''}
            onChange={handleFilterChange(filterName)}
            variant="standard"
            fullWidth
          />
        </ListItem>
      ))}
    </List>
  </div>
</Drawer>
</div>

  
  );
};

export default GraphComponent;
