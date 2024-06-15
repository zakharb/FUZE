import { useState, useEffect } from "react";
import { Tooltip as ReactTooltip }  from "react-tooltip";
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import "react-tooltip/dist/react-tooltip.css";

import SummaryChart from "../charts/SummaryChart"
import PolarChart from "../charts/PolarChart"
import Netmap from "../components/Netmap"
import TopCat from "../components/TopCat"

import {
  fetchSummaryData,
  fetchPolarData,
  fetchCategoriesData,
  fetchMapData,
  } from "../api/ApiNetmapPage"

function NetMapPage() {
  const [summaryData, setSummaryData] = useState({});
  const [categoriesData, setCategoriesData] = useState([]);
  const [mapData, setMapData] = useState();
  const [polarData, setPolarData] = useState({});
  const [content, setContent] = useState("");

  useEffect(() => {
    fetchSummaryData(setSummaryData);
    fetchCategoriesData(setCategoriesData);
    fetchMapData(setMapData);
  }, []);

  return (  
  <div style={{ width: '100%' }}>
    <Box sx={{ width: '100%', paddingTop:4 }}>
      <Grid container rowSpacing={2} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
        <Grid item md={12} lg={12} xl={9}>
          <Box sx={{ width: '100%' }}>
            <Grid container rowSpacing={2} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
              <Grid item md={12}>
                {mapData && 
                  <Netmap 
                    data={mapData} 
                    link='/source'
                  />
                }
              </Grid>
            </Grid>
          </Box>
        </Grid>
        <Grid item md={12} lg={12} xl={3}>
          <Box sx={{ width: '100%' }}>
            <Grid container rowSpacing={2} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
              <Grid item md={12} lg={6} xl={12}>
                <TopCat 
                  categories={categoriesData} 
                  setCategories={setCategoriesData}
                  name={'Top connections'}
                />
              </Grid>
              {/* <Grid item md={12} lg={6} xl={12}>
                <div className="netmap-wrapper">
                  <SummaryChart 
                    summaryData={summaryData} 
                    name='Some chart'/>
                </div>
              </Grid> */}
              <Grid item md={12} lg={6} xl={12}>
                <div>
                   <PolarChart 
                    fetchApi={fetchPolarData}
                    polarData={polarData}
                    setPolarData={setPolarData}
                    name='Services Severity'
                    filter="source" 
                    link="/source"
                  />
               </div>
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

export default NetMapPage;