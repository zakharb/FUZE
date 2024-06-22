import React, { useState, useEffect } from 'react';
import { PolarArea } from 'react-chartjs-2';
import { useNavigate } from 'react-router-dom';
import { memo } from 'react';
import { 
  Chart as ChartJS, 
  RadialLinearScale, 
  ArcElement, 
  Tooltip, 
  Legend 
} from 'chart.js';

ChartJS.register(
  RadialLinearScale, 
  ArcElement, 
  Tooltip, 
  Legend
);

const PolarChart = ({ fetchApi, polarData, setPolarData, name, filter, link }) => {
  const navigate = useNavigate();
  const [timeframe, setTimeframe] = useState('1d');

  useEffect(() => {
    fetchApi(setPolarData, timeframe);
  }, []);

  const handleTimeframeChange = (event) => {
    setTimeframe(event.target.value);
    fetchApi(setPolarData, event.target.value);
  }

  const data = {
    labels: polarData.labels,
    datasets: [{
      data: polarData.data,
      backgroundColor: [
        'rgba(220, 20, 60, 0.7)',
        'rgba(255, 182, 72, 0.7)',
        'rgba(0, 127, 255, 0.7)',
        'rgba(190, 243, 95, 0.7)',
        'rgba(128, 128, 128, 0.7)',
        'rgba(255, 99, 132, 0.7)',
        'rgba(54, 162, 235, 0.7)',
        'rgba(255, 206, 86, 0.7)',
      ],
      borderColor: [
        'rgba(220, 20, 60, 1)',
        'rgba(255, 182, 72, 1)',
        'rgba(0, 127, 255, 1)',
        'rgba(165, 206, 0, 1)',
        'rgba(128, 128, 128, 1)',
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
      ],
      borderWidth: 1
    }]
  };

  const options = {
    responsive: true,
    onClick: function (evt, element) {
      if (element.length > 0) {
        const selectedIndex = element[0].index;
        const selectedValue = data.labels[selectedIndex];
        const queryParams = new URLSearchParams({ [filter]: selectedValue }).toString();
        console.log(`${link}?${queryParams.toLowerCase()}`)
        navigate(`${link}?${queryParams.toLowerCase()}`);
      }
    },
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'bottom',
      },
      title: {
        display: false,
      }
    },
    scales: {
      r: {
        ticks: {
          display: false
        }
      }
    },
    elements: {
      point: {
        radius: 0,
        pointHitRadius: 10
      }
    }
  };

  return (
    <div className="chart">
      <div className="chart-title">
        {name}
      </div>
      <div className="chart-time">
        <select value={timeframe} onChange={handleTimeframeChange}>
          <option value="1d">1d</option>
          <option value="8h">8h</option>
          <option value="1h">1h</option>
        </select>
      </div>
      <PolarArea data={data} options={options} />
    </div>
  );
};

export default PolarChart;
