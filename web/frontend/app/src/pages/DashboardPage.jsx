import { useState, useEffect } from "react";
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import ReportIcon from '@mui/icons-material/Report';
import StorageIcon from '@mui/icons-material/Storage';
import AccountTreeIcon from '@mui/icons-material/AccountTree';

import TopCat from "../components/TopCat"
import BarChart from "../charts/BarChart"
import BubbleChart from "../charts/BubbleChart"
import CardTotal from "../components/CardTotal"
import PolarChart from "../charts/PolarChart"
import RadarChart from "../charts/RadarChart"
import TimelineChart from "../charts/TimeLineChart"
import SummaryChart from "../charts/SummaryChart"

import {
  fetchTimelineData,
  fetchSummaryData,
  fetchBarData,
  fetchRadarData,
  fetchPolarData,
  fetchCard1Data,
  fetchCard2Data,
  fetchCard3Data,
  fetchCategoriesData,
  } from "../api/ApiSiemPage"

function Siem() {

  const [timelineData, setTimelineData] = useState({
        datasets: [],});
  const [summaryData, setSummaryData] = useState({});
  const [barData, setBarData] = useState({});
  const [radarData, setRadarData] = useState({});
  const [polarData, setPolarData] = useState({});
  const [card1Data, setCard1Data] = useState('');
  const [card2Data, setCard2Data] = useState('');
  const [card3Data, setCard3Data] = useState('');
  const [categoriesData, setCategoriesData] = useState([{}]);
  
  useEffect(() => {
    fetchSummaryData(setSummaryData);
    fetchCategoriesData(setCategoriesData);
    fetchCard1Data(setCard1Data);
    fetchCard2Data(setCard2Data);
    fetchCard3Data(setCard3Data);
  }, []);

  return (  
  <div>
    <Box sx={{ width: '100%' }}>
      <Grid container rowSpacing={2} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
        <Grid item xs={12} md={12} lg={12} xl={9}>
          <Box sx={{ width: '100%' }}>
            <Grid container rowSpacing={2} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
              <Grid item xs={12} md={12} lg={4}>
                <CardTotal 
                  data={card1Data} 
                  icon={<AccountTreeIcon color="primary" sx={{ fontSize: 48 }} />} 
                  totalText='Sources' 
                  lastMinuteText='' 
                />
              </Grid>
              <Grid item xs={12} md={12} lg={4}>
                <CardTotal 
                  data={card2Data} 
                  icon={<StorageIcon color="primary" sx={{ fontSize: 48 }} />} 
                  totalText='Destinations'
                  lastMinuteText='' 
                />
              </Grid>
              <Grid item xs={12} md={12} lg={4}>
                <CardTotal 
                  data={card3Data} 
                  icon={<ReportIcon color="primary" sx={{ fontSize: 48 }} />} 
                  totalText='Services'
                  lastMinuteText='' 
                />
              </Grid>
              <Grid item xs={12} md={12} marginTop={2}>
                <TimelineChart 
                  fetchApi={fetchTimelineData}
                  timelineData={timelineData}
                  setTimelineData={setTimelineData}
                  name='Critical Sources'
                  color="primary"
                  filter="endDate" 
                  link="/data"
                />
              </Grid>
            </Grid>
          </Box>
        </Grid>
        <Grid item md={12} lg={12} xl={3}>
          <Box sx={{ width: '100%' }}>
            <Grid container rowSpacing={2} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
              <Grid item xs={12} md={12} lg={6} xl={12}>
                <TopCat 
                  categories={categoriesData} 
                  setCategories={setCategoriesData} 
                  name={'Critical Rules'}
                />
              </Grid>
              <Grid item xs={12} md={12} lg={6} xl={12}>
                <div className="incidents-wrapper">
                  <SummaryChart 
                    summaryData={summaryData} 
                    name='Firewall Rules'
                  />
                </div>
              </Grid>
            </Grid>
          </Box>
        </Grid>
        <Grid item xs={12} md={12} lg={12} xl={12}>
          <Grid container rowSpacing={2} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
            <Grid item xs={12} md={12} lg={4} xl={3}>
              <PolarChart 
                fetchApi={fetchPolarData}
                polarData={polarData}
                setPolarData={setPolarData}
                name='Severity'
                filter="source" 
                link="/data"
              />
            </Grid>
            <Grid item xs={12} md={12} lg={8} xl={6}>
              <BubbleChart 
                fetchApi={fetchBarData}
                barData={barData}
                setBarData={setBarData}
                name='Services'
                filter="tactic" 
                link="/data"
              />
            </Grid>
            <Grid item xs={12} md={12} lg={4} xl={3}>
              <RadarChart 
                fetchApi={fetchRadarData}
                radarData={radarData}
                setRadarData={setRadarData}
                name='Classification'
                filter="tactic" 
                link="/data"
              />
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Box>
  </div>
);
}

export default Siem;