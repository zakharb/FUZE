import { useState, createContext, useContext } from 'react';
import { styled, useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import MuiDrawer from '@mui/material/Drawer';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import HubIcon from '@mui/icons-material/Hub';
import TextSnippetIcon from '@mui/icons-material/TextSnippet';
import FolderIcon from '@mui/icons-material/Folder';

import SpeedIcon from '@mui/icons-material/Speed';
import TroubleshootIcon from '@mui/icons-material/Troubleshoot';

import { Tooltip } from '@mui/material';
import "react-tooltip/dist/react-tooltip.css";

import Logo from '../assets/logo.png';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import {
  Link,
  useLocation,
} from 'react-router-dom';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';

import DownloadingIcon from '@mui/icons-material/Downloading';
import LogoutIcon from '@mui/icons-material/Logout';

import {
  fetchInstallConfig,
  fetchCheckRules,
  } from "../api/ApiSettingsPage"


const breadcrumbNameMap = {
  '/collectors': 'Collectors',
  '/sources': 'Sources',
  '/normalization': 'Normalization',
  '/correlation': 'Correlation',
  '/messages': 'Messages',
  '/events': 'Events',
  '/metaevents': 'Meta Events',
  '/dashboard': 'Dashboard',
  '/netmap': 'Network',
  '/taxanomy': 'Taxanomy',
};

function Page() {
  const location = useLocation();
  const pathnames = location.pathname.split('/').filter((x) => x);

  return (
    <Breadcrumbs aria-label="breadcrumb" color="white">
      {pathnames.map((value, index) => {
        const last = index === pathnames.length - 1;
        const to = `/${pathnames.slice(0, index + 1).join('/')}`;

        return last ? (
          <Typography variant="h5" key={to}>
            {breadcrumbNameMap[to]}
          </Typography>
        ) : (
          <Link underline="hover" color="inherit" to={to} key={to}>
            {breadcrumbNameMap[to]}
          </Link>
        );
      })}
    </Breadcrumbs>
  );
}


const drawerWidth = 200;

const openedMixin = (theme) => ({
  width: drawerWidth,
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.enteringScreen,
  }),
  overflowX: 'hidden',
});

const closedMixin = (theme) => ({
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  overflowX: 'hidden',
  width: `calc(1px)`,
  [theme.breakpoints.up('sm')]: {
    width: `calc(${theme.spacing(8)} + 1px)`,
  },
});

const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'flex-end',
  padding: theme.spacing(0, 1),
  ...theme.mixins.toolbar,
}));

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(['width', 'margin'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    width: drawerWidth,
    flexShrink: 0,
    whiteSpace: 'nowrap',
    boxSizing: 'border-box',
    ...(open && {
      ...openedMixin(theme),
      '& .MuiDrawer-paper': {...openedMixin(theme), borderWidth: 0},
    }),
    ...(!open && {
      ...closedMixin(theme),
      '& .MuiDrawer-paper': {...closedMixin(theme), borderWidth: 0},
    }),
  }),
);

export default function MiniDrawer({MainContent,  ChangeTheme}) {

  const [activeItem, setActiveItem] = useState('Dashboard');
  const menuId = 'primary-search-account-menu';
  const [anchorEl, setAnchorEl] = useState(null);
  const isMenuOpen = Boolean(anchorEl);

  const handleMenuClose = () => {
      setAnchorEl(null);
    };

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = `${import.meta.env.VITE_URL}`;
  };

  const renderMenu = (
    <Menu
      anchorEl={anchorEl}
      anchorOrigin={{
        vertical: 'bottom',
        horizontal: 'right',
      }}
      id={menuId}
      keepMounted
      transformOrigin={{
        vertical: 'top',
        horizontal: 'right',
      }}
      open={isMenuOpen}
      onClose={handleMenuClose}
    >
      <MenuItem                 
        component={Link}
        to="/profile"
        onClick={handleMenuClose}
        >
        Profile
      </MenuItem>
      <MenuItem onClick={handleLogout}>LogOut</MenuItem>
    </Menu>
  );
  const theme = useTheme();
  const [open, setOpen] = useState(false);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  const handleInstallConfig = () => {
    fetchInstallConfig();
  };

  const handleCheckRules = () => {
    fetchCheckRules();
  };

  const ColorModeContext = createContext({ toggleColorMode: () => {} });
  const colorMode = useContext(ColorModeContext);
  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar position="fixed" open={open} style={{ boxShadow: '5px 5px 5px rgba(0, 0, 0, 0.3)' }}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"
            sx={{
              marginRight: 5,
              ...(open && { display: 'none' }),
            }}
          >
            <MenuIcon />
          </IconButton>
          <img className="logo" src={Logo} alt="Help support" style={{ width: 90, height: 28, marginRight:20, marginLeft:20  }} />
          <Typography variant="h6" noWrap component="div">
            
          </Typography>
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ marginLeft: 10, display: { xs: 'none', sm: 'block' } }}>
            <Page />
          </Typography>
          <Box sx={{ flexGrow: 1 }} />
          <Box sx={{ display: { xs: 'none', md: 'flex' } }}>
            <IconButton 
              onClick={handleCheckRules}
              size="large" 
              color="warning">
              <DownloadingIcon />
            </IconButton>
            <IconButton 
              onClick={handleInstallConfig}
              size="large" 
              color="inherit">
              <DownloadingIcon />
            </IconButton>
            <ChangeTheme />
            <IconButton 
              size="large" 
              color="inherit"
              onClick={handleLogout}
            >
              <LogoutIcon />
            </IconButton>
          </Box>

        </Toolbar>
      </AppBar>
      <Drawer variant="permanent" open={open}>
        <DrawerHeader sx={{bgcolor: "primary" }}>
          <IconButton onClick={handleDrawerClose}>
            <ChevronLeftIcon sx={{color: "#808080"}}/>
          </IconButton >
        </DrawerHeader>
        <Divider />
        <List>
            <ListItem key="Dashboard" disablePadding sx={{ display: 'block' }}>
              <ListItemButton
                onClick={() => setActiveItem('Dashboard')}
                component={Link}
                to="/dashboard"
                sx={{
                  minHeight: 48,
                  justifyContent: open ? 'initial' : 'center',
                  px: 2.5,
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 0,
                    mr: open ? 3 : 'auto',
                    justifyContent: 'center',
                  }}
                >
                <Tooltip title="Dashboard">
                  <SpeedIcon color={activeItem === 'Dashboard' ? 'primary' : 'inherit'} />
                </Tooltip>                
                </ListItemIcon>
                <ListItemText primary="Dashboard" sx={{ opacity: open ? 1 : 0 }} />
              </ListItemButton>
            </ListItem>
            <ListItem key="Netmap" disablePadding sx={{ display: 'block' }}>
              <ListItemButton
                onClick={() => setActiveItem('Netmap')}
                component={Link}
                to="/netmap"
                sx={{
                  minHeight: 48,
                  justifyContent: open ? 'initial' : 'center',
                  px: 2.5,
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 0,
                    mr: open ? 3 : 'auto',
                    justifyContent: 'center',
                  }}
                >
                <Tooltip title="Net Map">
                  <HubIcon color={activeItem === 'Netmap' ? 'primary' : 'inherit'} />
                </Tooltip>                
                </ListItemIcon>
                <ListItemText primary="Netmap" sx={{ opacity: open ? 1 : 0 }} />
              </ListItemButton>
            </ListItem>


            <ListItem key="Collectors" disablePadding sx={{ display: 'block' }}>
              <ListItemButton
                onClick={() => setActiveItem('Collectors')}
                component={Link}
                to="/collectors"
                sx={{
                  minHeight: 48,
                  justifyContent: open ? 'initial' : 'center',
                  px: 2.5,
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 0,
                    mr: open ? 3 : 'auto',
                    justifyContent: 'center',
                  }}
                >
                <Tooltip title="Collectors">
                  <TroubleshootIcon color={activeItem === 'Collectors' ? 'primary' : 'inherit'} />
                </Tooltip>                
                </ListItemIcon>
                <ListItemText primary="Collectors" sx={{ opacity: open ? 1 : 0 }} />
              </ListItemButton>
            </ListItem>
          
            <ListItem key="Sources" disablePadding sx={{ display: 'block' }}>
              <ListItemButton
                onClick={() => setActiveItem('Sources')}
                component={Link}
                to="/sources"
                sx={{
                  minHeight: 48,
                  justifyContent: open ? 'initial' : 'center',
                  px: 2.5,
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 0,
                    mr: open ? 3 : 'auto',
                    justifyContent: 'center',
                  }}
                >
                <Tooltip title="Sources">
                  <TroubleshootIcon color={activeItem === 'Sources' ? 'primary' : 'inherit'} />
                </Tooltip>                
                </ListItemIcon>
                <ListItemText primary="Sources" sx={{ opacity: open ? 1 : 0 }} />
              </ListItemButton>
            </ListItem>
          
            <ListItem key="Normalization" disablePadding sx={{ display: 'block' }}>
              <ListItemButton
                onClick={() => setActiveItem('Normalization')}
                component={Link}
                to="/normalization"
                sx={{
                  minHeight: 48,
                  justifyContent: open ? 'initial' : 'center',
                  px: 2.5,
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 0,
                    mr: open ? 3 : 'auto',
                    justifyContent: 'center',
                  }}
                >
                <Tooltip title="Normalization">
                  <TroubleshootIcon color={activeItem === 'Normalization' ? 'primary' : 'inherit'} />
                </Tooltip>                
                </ListItemIcon>
                <ListItemText primary="Normalization" sx={{ opacity: open ? 1 : 0 }} />
              </ListItemButton>
            </ListItem>
            <ListItem key="Correlation" disablePadding sx={{ display: 'block' }}>
              <ListItemButton
                onClick={() => setActiveItem('Correlation')}
                component={Link}
                to="/correlation"
                sx={{
                  minHeight: 48,
                  justifyContent: open ? 'initial' : 'center',
                  px: 2.5,
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 0,
                    mr: open ? 3 : 'auto',
                    justifyContent: 'center',
                  }}
                >
                <Tooltip title="Correlation">
                  <TroubleshootIcon color={activeItem === 'Correlation' ? 'primary' : 'inherit'} />
                </Tooltip>                
                </ListItemIcon>
                <ListItemText primary="Correlation" sx={{ opacity: open ? 1 : 0 }} />
              </ListItemButton>
            </ListItem>

            <ListItem key="taxanomy" disablePadding sx={{ display: 'block' }}>
              <ListItemButton
                onClick={() => setActiveItem('Taxanomy')}
                component={Link}
                to="/taxanomy"
                sx={{
                  minHeight: 48,
                  justifyContent: open ? 'initial' : 'center',
                  px: 2.5,
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 0,
                    mr: open ? 3 : 'auto',
                    justifyContent: 'center',
                  }}
                >
                <Tooltip title="Taxanomy">
                  <FolderIcon color={activeItem === 'Taxanomy' ? 'primary' : 'inherit'} />
                </Tooltip>                
                </ListItemIcon>
                <ListItemText primary="Taxanomy" sx={{ opacity: open ? 1 : 0 }} />
              </ListItemButton>
            </ListItem>
            <ListItem key="Messages" disablePadding sx={{ display: 'block' }}>
              <ListItemButton
                onClick={() => setActiveItem('Messages')}
                component={Link}
                to="/messages"
                sx={{
                  minHeight: 48,
                  justifyContent: open ? 'initial' : 'center',
                  px: 2.5,
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 0,
                    mr: open ? 3 : 'auto',
                    justifyContent: 'center',
                  }}
                >
                <Tooltip title="Messages">
                  <TextSnippetIcon color={activeItem === 'Messages' ? 'primary' : 'inherit'} />
                </Tooltip>                
                </ListItemIcon>
                <ListItemText primary="Messages" sx={{ opacity: open ? 1 : 0 }} />
              </ListItemButton>
            </ListItem>
            <ListItem key="Events" disablePadding sx={{ display: 'block' }}>
              <ListItemButton
                onClick={() => setActiveItem('Events')}
                component={Link}
                to="/events"
                sx={{
                  minHeight: 48,
                  justifyContent: open ? 'initial' : 'center',
                  px: 2.5,
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 0,
                    mr: open ? 3 : 'auto',
                    justifyContent: 'center',
                  }}
                >
                <Tooltip title="Events">
                  <TextSnippetIcon color={activeItem === 'Events' ? 'primary' : 'inherit'} />
                </Tooltip>                
                </ListItemIcon>
                <ListItemText primary="Events" sx={{ opacity: open ? 1 : 0 }} />
              </ListItemButton>
            </ListItem>
            <ListItem key="Meta Events" disablePadding sx={{ display: 'block' }}>
              <ListItemButton
                onClick={() => setActiveItem('Meta Events')}
                component={Link}
                to="/metaevents"
                sx={{
                  minHeight: 48,
                  justifyContent: open ? 'initial' : 'center',
                  px: 2.5,
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 0,
                    mr: open ? 3 : 'auto',
                    justifyContent: 'center',
                  }}
                >
                <Tooltip title="Meta Events">
                  <TextSnippetIcon color={activeItem === 'Meta Events' ? 'primary' : 'inherit'} />
                </Tooltip>                
                </ListItemIcon>
                <ListItemText primary="Meta Events" sx={{ opacity: open ? 1 : 0 }} />
              </ListItemButton>
            </ListItem>
        </List>

      </Drawer>
      <Box component="main" sx={{ flexGrow: 1 , paddingTop: 2}}>
        <DrawerHeader />
          <MainContent />
      </Box>
      {renderMenu}
    </Box>
  );
}