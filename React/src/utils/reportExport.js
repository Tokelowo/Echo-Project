import { saveAs } from 'file-saver';
import { jsPDF } from 'jspdf';
import 'jspdf-autotable';

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

export const exportToPDF = (reportData) => {
  const doc = new jsPDF();
  const pageWidth = doc.internal.pageSize.getWidth();

  doc.setFontSize(20);
  doc.text(reportData.name, pageWidth / 2, 20, { align: 'center' });
  
  doc.setFontSize(12);
  doc.text(`Generated on: ${formatDate(new Date())}`, pageWidth / 2, 30, { align: 'center' });

  let yPos = 50;
  reportData.sections.forEach((section) => {
    if (yPos > 250) {
      doc.addPage();
      yPos = 20;
    }
    
    doc.setFontSize(14);
    doc.text(section.title, 20, yPos);
    yPos += 10;
    
    doc.setFontSize(12);
    doc.text(section.content, 20, yPos, {
      maxWidth: pageWidth - 40,
    });
    yPos += 30;
  });

  doc.save(`${reportData.name.replace(/\s+/g, '_')}.pdf`);
};

export const exportToExcel = (reportData) => {
  const rows = [
    ['Report Name', reportData.name],
    ['Generated Date', formatDate(new Date())],
    ['Type', reportData.type],
    [''],
    ['Section', 'Content']
  ];

  reportData.sections.forEach((section) => {
    rows.push([section.title, section.content]);
  });

  const csvContent = rows
    .map(row => row.map(cell => `"${cell}"`).join(','))
    .join('\\n');

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  saveAs(blob, `${reportData.name.replace(/\s+/g, '_')}.csv`);
};

export async function fetchResearchAgentData(endpoint = '', options = {}) {
  const BASE_URL = 'http://localhost:8000/api';
  try {
    const response = await fetch(BASE_URL + endpoint, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });
    if (!response.ok) {
      throw new Error(`Network response was not ok: ${response.status} ${response.statusText}`);
    }
    return response.json();
  } catch (error) {
    // Don't log AbortError - it's expected behavior when components unmount
    if (error.name !== 'AbortError') {
      console.error('fetchResearchAgentData error:', error);
    }
    throw error;
  }
}
