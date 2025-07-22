import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  IconButton,
  Menu,
  MenuItem,
  Divider,
  Tab,
  Tabs,
} from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';
import ShareIcon from '@mui/icons-material/Share';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import MessageIcon from '@mui/icons-material/Message';
import { exportToPDF, exportToExcel } from '../utils/reportExport';
import CommentSection from './CommentSection';
import ShareDialog from './ShareDialog';

const TabPanel = ({ children, value, index, ...other }) => (
  <div
    role="tabpanel"
    hidden={value !== index}
    {...other}
  >
    {value === index && (
      <Box sx={{ p: 3 }}>
        {children}
      </Box>
    )}
  </div>
);

const ReportPreview = ({ open, onClose, report }) => {
  const [anchorEl, setAnchorEl] = useState(null);
  const [tabValue, setTabValue] = useState(0);
  const [shareDialogOpen, setShareDialogOpen] = useState(false);
  const exportMenuOpen = Boolean(anchorEl);

  const handleExportClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleExportClose = () => {
    setAnchorEl(null);
  };

  const handleExport = (format) => {
    if (format === 'pdf') {
      exportToPDF(report);
    } else if (format === 'excel') {
      exportToExcel(report);
    }
    handleExportClose();
  };

  if (!report) return null;

  return (
    <>
      <Dialog 
        open={open} 
        onClose={onClose}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h6">{report.name}</Typography>
            <Box>
              <IconButton onClick={() => setShareDialogOpen(true)}>
                <ShareIcon />
              </IconButton>
              <IconButton onClick={handleExportClick}>
                <DownloadIcon />
              </IconButton>
              <IconButton>
                <MoreVertIcon />
              </IconButton>
            </Box>
          </Box>
        </DialogTitle>

        <Tabs
          value={tabValue}
          onChange={(_, newValue) => setTabValue(newValue)}
          variant="fullWidth"
          sx={{ 
            borderBottom: 1, 
            borderColor: 'divider',
            '& .MuiTab-root': {
              minHeight: 48,
              textTransform: 'none',
              fontWeight: 500,
            }
          }}
        >
          <Tab 
            label="Report" 
            sx={{ 
              flex: 1,
              minWidth: 0
            }}
          />
          <Tab 
            label="Comments" 
            icon={<MessageIcon />} 
            iconPosition="end"
            sx={{ 
              flex: 1,
              minWidth: 0
            }}
          />
        </Tabs>

        <DialogContent dividers>
          <TabPanel value={tabValue} index={0}>
            {report.sections.map((section, index) => (
              <Box key={index} mb={3}>
                <Typography variant="h6" gutterBottom>
                  {section.title}
                </Typography>
                <Typography variant="body1" paragraph>
                  {section.content}
                </Typography>
                {index < report.sections.length - 1 && <Divider sx={{ my: 2 }} />}
              </Box>
            ))}
          </TabPanel>
          <TabPanel value={tabValue} index={1}>
            <CommentSection reportId={report.id} />
          </TabPanel>
        </DialogContent>

        <DialogActions>
          <Button onClick={onClose}>Close</Button>
          <Button 
            variant="contained" 
            startIcon={<ShareIcon />}
            onClick={() => setShareDialogOpen(true)}
          >
            Share
          </Button>
          <Button 
            variant="contained" 
            startIcon={<DownloadIcon />}
            onClick={handleExportClick}
          >
            Export
          </Button>
        </DialogActions>

        <Menu
          anchorEl={anchorEl}
          open={exportMenuOpen}
          onClose={handleExportClose}
        >
          <MenuItem onClick={() => handleExport('pdf')}>Export as PDF</MenuItem>
          <MenuItem onClick={() => handleExport('excel')}>Export as Excel</MenuItem>
        </Menu>
      </Dialog>

      <ShareDialog
        open={shareDialogOpen}
        onClose={() => setShareDialogOpen(false)}
        report={report}
      />
    </>
  );
};

export default ReportPreview;
