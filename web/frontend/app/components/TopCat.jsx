import './TopCat.css';

import React, { useState, useEffect } from 'react';

import Card from '@mui/material/Card';

import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

function TopCatList({categories, setCategories, name}) {

  const [hoverM, setHover] = useState(0);
  
  useEffect(() => {
    const intervalId = setInterval(() => {
      if (hoverM != 1) {
        setCategories((prevList) => {
          const newData = [...prevList];
          const firstItem = newData.shift();
          newData.push(firstItem);
          return newData;
        });
      };
    }, 3000);
    return () => clearInterval(intervalId);
  }, [hoverM]);

  const getColorClass = (count) => {
    if (count == 0) {
      return "gray";
    } else if (count <= 5) {
      return "warning";
    } else {
      return "danger";
    }
  };

  const handleHoverOn = () => {
    setHover(1);
  }

  const handleHoverOff = () => {
    setHover(0);
  }
  return (
    <div>
      <Card sx={{ minWidth: 275, maxHeight: 310, display: 'flex' }} onMouseOver={handleHoverOn} onMouseLeave={handleHoverOff}>
        <CardContent sx={{ flex: '1 0 auto', paddingTop: 0 }}>
          <Typography variant="h6" component="div" color="text.secondary">
            {name}
          </Typography>
          <ul style={{ listStyleType: 'none' }}>
            {categories.map(({ id, title, count, subtitle, delta, href }) => (
              <li key={id} style={{ margin: '1em'}}>
                <a href={href} target="_blank">
                  <div className="top-cat-list__title">
                    {title} <span>{count}</span>
                  </div>
                  <div className="top-cat-list__subtitle">
                    {subtitle} 
                    <span className={getColorClass(delta)}>+{delta}</span>
                  </div>
                </a>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}

export default TopCatList;
