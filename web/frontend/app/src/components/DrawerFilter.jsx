import React from 'react';
import { Drawer, List, ListItem, TextField, Button, Typography } from '@mui/material';
import FilterListIcon from '@mui/icons-material/FilterList';

const DrawerFilter = ({ filters, setFilters, applyFilters, startDate, setStartDate, endDate, setEndDate }) => {
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

  return (
    <React.Fragment>
      <Button variant="text" color="secondary" onClick={handleOpenDrawer}>
        <FilterListIcon />
      </Button>
      <Drawer anchor="right" open={openDrawer} onClose={handleCloseDrawer}>
        <div style={{ width: 300, marginTop: 100 }}>
          <div style={{ display: 'flex', justifyContent: 'center', marginTop: 'auto' }}>
            <Button variant="contained" color="primary" onClick={handleApplyFilters}>
              Apply
            </Button>
          </div>
          <List>
            <ListItem>
              <TextField
                name="startDate"
                type="datetime-local"
                value={startDate || ''}
                onChange={event => setStartDate(event.target.value)}
                variant="outlined"
                fullWidth
              />
            </ListItem>
            <ListItem>
              <TextField
                name="endDate"
                type="datetime-local"
                value={endDate || ''}
                onChange={event => setEndDate(event.target.value)}
                variant="outlined"
                fullWidth
              />
            </ListItem>
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
    </React.Fragment>
  );
};

export default DrawerFilter;
