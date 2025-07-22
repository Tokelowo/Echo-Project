import React, { useState } from 'react';
import {
  Snackbar,
  Alert,
  Badge,
  Menu,
  MenuItem,
  IconButton,
  Typography,
  Box,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Divider,
} from '@mui/material';
import NotificationsIcon from '@mui/icons-material/Notifications';
import CommentIcon from '@mui/icons-material/Comment';
import ShareIcon from '@mui/icons-material/Share';
import DescriptionIcon from '@mui/icons-material/Description';

// Mock notifications
const initialNotifications = [
  {
    id: 1,
    type: 'comment',
    message: 'Alice Chen commented on Q2 2025 Market Analysis',
    timestamp: new Date(Date.now() - 1000 * 60 * 5).toISOString(),
    read: false,
    user: 'Alice Chen',
  },
  {
    id: 2,
    type: 'share',
    message: 'Bob Smith shared Competitor Benchmark Report with you',
    timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
    read: false,
    user: 'Bob Smith',
  },
  {
    id: 3,
    type: 'update',
    message: 'Monthly Product Performance report was updated',
    timestamp: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
    read: true,
    user: 'System',
  },
];

const getNotificationIcon = (type) => {
  switch (type) {
    case 'comment':
      return <CommentIcon color="primary" />;
    case 'share':
      return <ShareIcon color="secondary" />;
    case 'update':
      return <DescriptionIcon color="info" />;
    default:
      return <NotificationsIcon />;
  }
};

const NotificationSystem = () => {
  const [notifications, setNotifications] = useState(initialNotifications);
  const [anchorEl, setAnchorEl] = useState(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  const unreadCount = notifications.filter(n => !n.read).length;

  const handleNotificationClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleNotificationRead = (notificationId) => {
    setNotifications(notifications.map(notification =>
      notification.id === notificationId
        ? { ...notification, read: true }
        : notification
    ));
    handleClose();
  };

  const handleSnackbarClose = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  // Function to add a new notification
  const addNotification = (notification) => {
    const newNotification = {
      id: notifications.length + 1,
      timestamp: new Date().toISOString(),
      read: false,
      ...notification,
    };
    setNotifications([newNotification, ...notifications]);
    setSnackbar({
      open: true,
      message: notification.message,
      severity: 'info',
    });
  };

  return (
    <>
      <IconButton color="inherit" onClick={handleNotificationClick}>
        <Badge badgeContent={unreadCount} color="error">
          <NotificationsIcon />
        </Badge>
      </IconButton>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleClose}
        PaperProps={{
          sx: {
            width: 360,
            maxHeight: 400,
          },
        }}
      >
        <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
          <Typography variant="h6">Notifications</Typography>
        </Box>
        <List sx={{ p: 0 }}>
          {notifications.map((notification, index) => (
            <React.Fragment key={notification.id}>
              <ListItem
                button
                onClick={() => handleNotificationRead(notification.id)}
                sx={{
                  bgcolor: notification.read ? 'transparent' : 'action.hover',
                }}
              >
                <ListItemAvatar>
                  <Avatar>
                    {getNotificationIcon(notification.type)}
                  </Avatar>
                </ListItemAvatar>
                <ListItemText
                  primary={notification.message}
                  secondary={new Date(notification.timestamp).toLocaleString()}
                />
              </ListItem>
              {index < notifications.length - 1 && <Divider />}
            </React.Fragment>
          ))}
        </List>
      </Menu>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleSnackbarClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert onClose={handleSnackbarClose} severity={snackbar.severity}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </>
  );
};

export { NotificationSystem, initialNotifications };
