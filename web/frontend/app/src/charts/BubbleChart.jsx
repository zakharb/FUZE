import React, { useState, useEffect } from 'react';
import { Bubble } from 'react-chartjs-2';
import { useNavigate } from 'react-router-dom';
import { memo } from 'react';
import {
    Chart as ChartJS,
    LinearScale,
    PointElement,
    Tooltip,
    Legend,
  } from 'chart.js';

ChartJS.register(LinearScale, PointElement, Tooltip, Legend);

const BubbleChart = ({ fetchApi, barData, setBarData, name, filter, link }) => {
  const navigate = useNavigate();
  const [timeframe, setTimeframe] = useState('1w');

  useEffect(() => {
    fetchApi(setBarData, timeframe);
  }, []);

  const handleTimeframeChange = (event) => {
    setTimeframe(event.target.value);
    fetchApi(setBarData, event.target.value);
  }
  console.log(barData)
  const data = {
    datasets: [
      {
        labels: ['1','2'],
        label: 'Low',
        // data: [],
        data: [{
          'x': 10,
          'y': 10,
          'r': 10,
        },
        {
            'x': 6,
            'y': 6,
            'r': 25,
        }],
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
      },
      {
        label: 'Medium',
        // data: [],
        data: [{
          'x': 4,
          'y': 4,
          'r': 10,
        },
        {
            'x': 3,
            'y': 7,
            'r': 15,
        }],
        
        backgroundColor: 'rgba(255, 182, 72, 0.7)',
      }
    ]
  };
  const options = {
    onClick: function(evt, element) {
      if (element.length > 0) {
        const selectedIndex = element[0].datasetIndex;
        const selectedValue = data.datasets[selectedIndex].label;
        const queryParams = new URLSearchParams({ [filter]: selectedValue }).toString();
        navigate(`${link}?${queryParams.toLowerCase()}`);
      }
    },
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        display: false,
        grid: {
          display: true
        },
      },
      y: {
        display: false,
        grid: {
          display: true
        },
      }
    },
    plugins: {
      legend: {
        position: 'bottom',
      },
      title: {
        display: false,
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
          <option value="1w">1w</option>
        </select>
      </div>
      <Bubble data={data} options={options} />
    </div>
  );
};

export default BubbleChart;
