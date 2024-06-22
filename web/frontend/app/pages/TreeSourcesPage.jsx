import { useState, useEffect } from "react";
import { Tooltip as ReactTooltip }  from "react-tooltip";
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import "react-tooltip/dist/react-tooltip.css";

import SummaryChart from "../charts/SummaryChart"
import PolarChart from "../charts/PolarChart"
import Treemap from "../components/Treemap"
import TopCat from "../components/TopCat"

import {
  fetchTreeSourcesData,
  } from "../api/ApiNetmapPage"

function NetTreePage() {
  const [mapData, setMapData] = useState();
  const [content, setContent] = useState("");

  useEffect(() => {
    fetchTreeSourcesData(setMapData);
  }, []);

  return (  
  <div style={{ width: '100%' }}>
    <Box sx={{ width: '100%', paddingTop:4 }}>
      <Grid container rowSpacing={2} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
        <Grid item md={12} lg={12} xl={12}>
          <Box sx={{ width: '100%' }}>
            <Grid container rowSpacing={2} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
              <Grid item md={12}>
                {mapData && 
                  <Treemap 
                    data={mapData} 
                    link='/source'
                  />
                }
              </Grid>
            </Grid>
          </Box>
        </Grid>
      </Grid>
    </Box>
    <ReactTooltip
      anchorId="app-title"
      place="top"
      content={content}>
    </ReactTooltip>
  </div>
);
}

export default NetTreePage;