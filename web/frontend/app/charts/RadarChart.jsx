import React, { useState, useEffect } from 'react';
import { Radar } from 'react-chartjs-2';
import { useNavigate } from 'react-router-dom';
import { memo } from 'react';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

const RadarChart = ({ fetchApi, radarData, setRadarData, name, filter, link }) => {
  const navigate = useNavigate();
  const [timeframe, setTimeframe] = useState('1d');

  useEffect(() => {
    fetchApi(setRadarData, timeframe);
  }, []);

  const handleTimeframeChange = (event) => {
    setTimeframe(event.target.value);
    fetchApi(setRadarData, event.target.value);
  }

  const data = {
    labels: radarData.labels,
    datasets: [{
      data: radarData.dataset1_data,
      label: radarData.dataset1_label,
      backgroundColor: [
        'rgba(220, 20, 60, 0.8)',
      ],
      borderColor: [
        'rgba(220, 20, 60, 1)',
      ],
      borderWidth: 1
    },
    ...(radarData.dataset2_data
        ? [
            {
              data: radarData.dataset2_data,
              label: radarData.dataset2_label,
              backgroundColor: [
                'rgba(0, 127, 255, 0.8)',
              ],
              borderColor: [
                'rgba(0, 127, 255, 1)',
              ],
              borderWidth: 1
            },
          ]
        : []),
    ...(radarData.dataset3_data
        ? [
            {
              data: radarData.dataset3_data,
              label: radarData.dataset3_label,
              backgroundColor: [
                'rgba(190, 243, 95, 0.8)',
              ],
              borderColor: [
                'rgba(190, 243, 95, 1)',
              ],
              borderWidth: 1
            },
          ]
        : []),
    ]
  };

  const options = {
    responsive: true,
    onClick: function (evt, element) {
      if (element.length > 0) {
        const selectedIndex = element[0].index;
        const selectedValue = data.labels[selectedIndex];
        const queryParams = new URLSearchParams({ [filter]: selectedValue }).toString();
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
    },    
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
      <Radar data={data} options={options} />
    </div>
  );
};


export default RadarChart;