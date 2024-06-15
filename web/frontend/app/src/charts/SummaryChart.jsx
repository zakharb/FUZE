import React from 'react';
import { Line } from 'react-chartjs-2';
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

var width, height, gradient;

const SummaryChart = ({ summaryData, name}) => {
  
  function getGradient(ctx, chartArea) {
    var chartWidth = chartArea.right - chartArea.left;
    var chartHeight = chartArea.bottom - chartArea.top;
    if (gradient === null || width !== chartWidth || height !== chartHeight) {
      width = chartWidth;
      height = chartHeight;
      gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
      gradient.addColorStop(0, 'rgba(255, 255, 255, 0)');
      gradient.addColorStop(1, 'rgba(255, 255, 255, 0.4)');
    }
    return gradient;
  }

  const data = {
    name: summaryData.name,
    labels: summaryData.labels,
    datasets: [
      {
        label: summaryData.label,
        data: summaryData.data,
        tension: 0.4,
        backgroundColor: function backgroundColor(context) {
          var chart = context.chart;
          var ctx = chart.ctx,
              chartArea = chart.chartArea;
          if (!chartArea) {
            // This case happens on initial chart load
            return null;
          }

          return getGradient(ctx, chartArea);
        },
        borderColor: ['#fff'],
        borderWidth: 2,
        fill: true
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        display: false
      },
      x: {
        display: false
      }
    },
    elements: {
      point: {
        radius: 1
      }
    },
    plugins: {
      legend: {
        position: 'top',
        align: 'end',
        labels: {
          color: '#fff',
          size: 18,
          fontStyle: 800,
          boxWidth: 0
        }
      },
      title: {
        display: true,
        text: [name],
        color: '#fff',
        font: {
          size: 16,
          family: 'Inter',
          weight: '600',
          lineHeight: 1.4
        },
        padding: {
          top: 20
        }
      },
    },
    tooltips: {
      mode: 'index',
      intersect: false,
      callbacks: {
        label: function(tooltipItem, data) {
        const datasetLabel = data.datasets[tooltipItem.datasetIndex].label || '';
        const value = tooltipItem.yLabel.toFixed(2);
        return `1`;
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
    <div>
        <Line data={data} options={options} />
    </div>
  );
};


export default SummaryChart;