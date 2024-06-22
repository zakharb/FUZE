import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

const NoPage = () => {
  return (
    <Card sx={{marginLeft: 15, marginTop: 3, padding: 5}}>
      <CardContent>
        <Typography variant="h5">
          404 - Page Not Found
        </Typography>        
        <Typography  color="text.secondary">
          Sorry, the page you are looking for is unavailable or under development.
        </Typography>
      </CardContent>
      <CardContent>
        <a href="/">
          Go back to the homepage
        </a>
      </CardContent>
    </Card>
  );
}

export default NoPage;
