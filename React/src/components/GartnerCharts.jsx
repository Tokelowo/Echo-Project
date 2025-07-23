import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D'];

export const VendorOverviewChart = ({ data }) => (
  <ResponsiveContainer width="100%" height={450}>
    <BarChart 
      data={data}
      margin={{ top: 20, right: 30, left: 20, bottom: 120 }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis 
        dataKey="name" 
        angle={-45}
        textAnchor="end"
        height={140}
        interval={0}
        tick={{ fontSize: 12 }}
      />
      <YAxis />
      <RechartsTooltip />
      <Legend />
      <Bar dataKey="rating" fill="#0088FE" name="Overall Rating (1-5)" />
      <Bar dataKey="recommendation" fill="#00C49F" name="Recommendation Rate %" />
    </BarChart>
  </ResponsiveContainer>
);

export const ReviewerSegmentChart = ({ data }) => (
  <ResponsiveContainer width="100%" height={200}>
    <PieChart>
      <Pie
        data={data}
        cx="50%"
        cy="50%"
        outerRadius={80}
        fill="#8884d8"
        dataKey="value"
        label={({ name, value }) => `${value}%`}
      >
        {data.map((entry, index) => (
          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
        ))}
      </Pie>
      <RechartsTooltip />
      <Legend />
    </PieChart>
  </ResponsiveContainer>
);

const GartnerCharts = {
  VendorOverviewChart,
  ReviewerSegmentChart
};

export default GartnerCharts;
