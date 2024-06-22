import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';

const TotalCard = ({ data, icon, totalText, lastMinuteText }) => {
  return (
    <Card sx={{ minWidth: 275, display: 'flex' }}>
      <Box sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', paddingLeft: 3 }}>
        <Typography sx={{ mb: 1.5 }}>
          {icon}
        </Typography>
      </Box>
      <CardContent sx={{ flex: '1 0 auto' }}>
        <Typography variant="h5" component="div">
          {data.total}
        </Typography>
        <Typography sx={{ mb: 1.5 }} color="text.secondary">
          {totalText}
        </Typography>
      </CardContent>
      <CardContent sx={{ flex: '1 0 auto' }}>
        {data.change > 0 ?
          <Typography variant="h5">
            <TrendingUpIcon color="error"/> {Math.floor(data.change)}%
          </Typography> :
          <Typography variant="h5">
            <TrendingDownIcon color="success"/> {Math.floor(data.change)}%
          </Typography>
        }
        <Typography color="text.secondary">
          {lastMinuteText}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default TotalCard;
