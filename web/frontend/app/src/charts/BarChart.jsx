import React, { useState, useEffect } from 'react';
import { Bar } from 'react-chartjs-2';
import { useNavigate } from 'react-router-dom';
import { memo } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const BarChart = ({ fetchApi, barData, setBarData, name, filter, link }) => {
  const navigate = useNavigate();
  const [timeframe, setTimeframe] = useState('1w');

  useEffect(() => {
    fetchApi(setBarData, timeframe);
  }, []);

  const handleTimeframeChange = (event) => {
    setTimeframe(event.target.value);
    fetchApi(setBarData, event.target.value);
  }

  const data = {
    labels: barData.labels,
    datasets: [{
      label: barData.dataset1_label,
      data: barData.dataset1_data,
      backgroundColor: [
          'rgba(220, 20, 60, 0.7)',
        ],
      barPercentage: 0.5
      },
      ...(barData.dataset2_data
        ? [
            {
              label: barData.dataset2_label,
              data: barData.dataset2_data,
              backgroundColor: [
                  'rgba(255, 182, 72, 0.9)',
                ],
              barPercentage: 0.5
            },
          ]
      : []),
      ...(barData.dataset3_data
        ? [
            {
              label: barData.dataset3_label,
              data: barData.dataset3_data,
              backgroundColor: [
                  'rgba(0, 127, 255, 0.7)',
                ],
              barPercentage: 0.5
            },
          ]
      : []),
      ...(barData.dataset4_data
        ? [
            {
              label: barData.dataset4_label,
              data: barData.dataset4_data,
              backgroundColor: [
                  'rgba(190, 243, 95, 0.9)',
                ],
              barPercentage: 0.5
            },
          ]
      : []),
      ...(barData.dataset5_data
        ? [
            {
              label: barData.dataset5_label,
              data: barData.dataset5_data,
              backgroundColor: [
                  'rgba(128, 128, 128, 0.5)',
                ],
              barPercentage: 0.5
            },
          ]
      : [])
  ]}


  const options = {
    onClick: function(evt, element) {
      if (element.length > 0) {
        const selectedIndex = element[0].datasetIndex;
        const selectedValue = data.datasets[selectedIndex].label;
        const queryParams = new URLSearchParams({ [filter]: selectedValue }).toString();
        navigate(`${link}?${queryParams.toLowerCase()}`);
      }
    },    
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        stacked: true,
        grid: {
          display: false
        },
        categoryPercentage: 0.5,
        barPercentage: 0.5
      },
      y: {
        stacked: true,
        grid: {
          display: false
        },
        categoryPercentage: 0.5,
        barPercentage: 0.5
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
{/*          <option value="1d">1d</option>
          <option value="1m">1m</option>
*/}        </select>
      </div>
      <Bar data={data} options={options} />
    </div>    
  );
};


export default BarChart;