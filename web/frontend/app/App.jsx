import Drawer from './components/Drawer';

import {BrowserRouter, Routes, Route} from 'react-router-dom'

import NoPage from "./pages/NoPage"
import DashboardPage from "./pages/DashboardPage"
import CollectorsPage from "./pages/CollectorsPage"
import SourcesPage from "./pages/SourcesPage"
import NormalizationPage from "./pages/NormalizationPage"
import CorrelationPage from "./pages/CorrelationPage"
import MessagesPage from "./pages/MessagesPage"
import EventsPage from "./pages/EventsPage"
import MetaeventsPage from "./pages/MetaeventsPage"
import TaxanomyPage from "./pages/TaxanomyPage"
import NetmapPage from "./pages/NetmapPage"

import React, { useState, useEffect } from 'react';
import './App.css';
import './charts/SummaryChart.css';
import './charts/Chart.css';

import { ThemeProvider, createTheme } from '@mui/material/styles';

import Grid from '@mui/material/Grid';

import IconButton from '@mui/material/IconButton';

import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';

import CssBaseline from '@mui/material/CssBaseline';

import './App.css';

const ColorModeContext = React.createContext({ toggleColorMode: () => {} });

function App() {

  const [isLoggedIn, setIsLoggedIn] = useState(false);
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsLoggedIn(true);
    }
  }, []);

  const [mode, setMode] = React.useState('light');
  const colorMode = React.useMemo(
    () => ({
      toggleColorMode: () => {
        setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
      },
    }),
    [],
  );

  const theme = React.useMemo(
    () =>
      createTheme({
        palette: {
          mode,
          primary: {
            main: "#007fff",
            light: "#89CFF0",
          },
          secondary: {
            main: "#808080",
          },
          error: {
            main: "#dc143c",
          },
          success: {
            main: "#bef35f",
          },
          warning: {
            main: "#ffb648",
          },
        },
      }),
    [mode],
  );

  const ChangeTheme = () => (
    <IconButton sx={{ ml: 1 }} onClick={colorMode.toggleColorMode} color="inherit">
      {theme.palette.mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
    </IconButton>
  );

  const MainContent = () => (
    <Grid container spacing={2} paddingTop={3} paddingLeft={3} paddingRight={2} >
        <Routes>
          <Route exact path="/" element={<DashboardPage />} />
          <Route exact path="/collectors" element={<CollectorsPage />} />
          <Route exact path="/sources" element={<SourcesPage />} />
          <Route exact path="/normalization" element={<NormalizationPage />} />
          <Route exact path="/correlation" element={<CorrelationPage />} />
          <Route exact path="/messages" element={<MessagesPage />} />
          <Route exact path="/events" element={<EventsPage />} />
          <Route exact path="/metaevents" element={<MetaeventsPage />} />
          <Route exact path="/taxanomy" element={<TaxanomyPage />} />

          <Route exact path="/dashboard" element={<DashboardPage />} />
          <Route exact path="/netmap" element={<NetmapPage />} />
          <Route path="*" element={<NoPage />} />
        </Routes>
    </Grid>
  );

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <div>
          <CssBaseline enableColorScheme />
            <BrowserRouter>
              <Drawer ChangeTheme={ChangeTheme} MainContent={MainContent}/>
            </BrowserRouter>
        </div>
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
};

export default App;



