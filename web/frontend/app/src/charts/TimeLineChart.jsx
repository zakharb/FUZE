import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { useNavigate } from 'react-router-dom';
import { memo } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

var gridLine;

const TimelineChart = ({ fetchApi, timelineData, 
                         setTimelineData, 
                         name, filter, link, color }) => {
  const navigate = useNavigate();
  const [timeframe, setTimeframe] = useState('1h');

  useEffect(() => {
    fetchApi(setTimelineData, timeframe);
  }, []);

  // useEffect(() => {
  //   const interval = setInterval(() => {
  //     fetchApi(setTimelineData, '0');
  //   }, 60000);
  //   return () => clearInterval(interval);
  // }, []);

  const handleTimeframeChange = (event) => {
    setTimeframe(event.target.value);
    fetchApi(setTimelineData, event.target.value);
  }

  const borderColor = {
    primary: 'rgba(0, 127, 255, 1)',
    warning: 'rgba(255, 182, 72, 1)',
    secondary: 'rgba(128, 128, 128, 1)'
  }
  
  const backgroundColor = {
    primary: 'rgba(0, 127, 255, 0.7)',
    warning: 'rgba(255, 142, 72, 0.7)',
    secondary: 'rgba(128, 128, 128, 0.7)'
  }
  
  const data = {
    labels: timelineData.labels,
    datasets: [
      {
        data: timelineData.dataset3_data,
        label: timelineData.dataset3_label,
        cubicInterpolationMode: 'monotone',
        tension: 0.4,
        backgroundColor: ['rgba(220, 20, 60, 0.7)'],
        borderColor: ['rgba(220, 20, 60, 0.7)'],
        borderWidth: 2,
        fill: true,
      },
      ...(timelineData.dataset2_data
        ? [
            {
              label: timelineData.dataset2_label,
              data: timelineData.dataset2_data,
              cubicInterpolationMode: 'monotone',
              tension: 0.4,
              backgroundColor: backgroundColor[color],
              borderColor: borderColor[color],
              borderWidth: 2,
              fill: true,
            },
          ]
        : []),
      {
        label: timelineData.dataset1_label,
        data: timelineData.dataset1_data,
        cubicInterpolationMode: 'monotone',
        tension: 2,
        backgroundColor: ['rgba(190, 243, 95, 0.5)'],
        borderColor: ['rgba(190, 243, 95, 0.5)'],
        borderWidth: 2,
        fill: true,
      },
    ],
  };

  const options = {
    onClick: function (evt, element) {
      if (element.length > 0) {
        const selectedIndex = element[0].index;
        const selectedValue = data.labels[selectedIndex];
        const queryParams = new URLSearchParams({ [filter]: selectedValue }).toString();
        navigate(`${link}?${queryParams}`);
      }
    },
    maintainAspectRatio: false,
    scales: {
      y: {
        min: 0,
        ticks: {
          stepSize: 25
        },
        grid: {
          display: false
        }
      },
      x: {
        grid: {
          color: gridLine,
          display: false
        },
        ticks: {
          display: false
        }
        
      }
    },
    elements: {
      point: {
        radius: 0
      }
    },
    plugins: {
      legend: {
        position: 'top',
        align: 'end',
        labels: {
          boxWidth: 8,
          boxHeight: 8,
          usePointStyle: true,
          font: {
            size: 12,
            weight: '500'
          }
        }
      },
      title: {
        display: false,
      }
    },
    tooltips: {
      mode: 'index',
      intersect: false,
      callbacks: {
        label: function(tooltipItem, data) {
        const datasetLabel = data.datasets[tooltipItem.datasetIndex].label || '';
        const value = tooltipItem.yLabel.toFixed(2);
        return `${datasetLabel}: ${value}%`;
        }
      }
    },
    hover: {
      mode: 'index',
      intersect: false
    },
    interaction: {
      mode: "index",
      intersect: false,
    }
  };

  return (
    <div className="chart">
      <div className="chart-title">
        {name}
      </div>
      <div className="chart-time">
        <select value={timeframe} onChange={handleTimeframeChange}>
          <option value="1h">1h</option>
          <option value="8h">8h</option>
          <option value="24h">24h</option>
        </select>
      </div>
      <Line data={data} options={options} />
    </div>  
  );
};


export default TimelineChart;