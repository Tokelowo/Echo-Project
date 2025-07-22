import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Autocomplete,
  Chip,
  Typography,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import ShareIcon from '@mui/icons-material/Share';
import PersonAddIcon from '@mui/icons-material/PersonAdd';

// Mock user data
const mockUsers = [
  { id: 1, name: 'Alice Chen', email: 'alice.chen@company.com' },
  { id: 2, name: 'Bob Smith', email: 'bob.smith@company.com' },
  { id: 3, name: 'Carol White', email: 'carol.white@company.com' },
  { id: 4, name: 'David Brown', email: 'david.brown@company.com' },
];

const permissions = [
  { value: 'view', label: 'Can view' },
  { value: 'comment', label: 'Can comment' },
  { value: 'edit', label: 'Can edit' },
];

const SharedUserChip = ({ user, permission, onDelete, onPermissionChange }) => (
  <Box display="flex" alignItems="center" gap={1} mb={1}>
    <Chip
      label={`${user.name} (${user.email})`} // label is a string, not an object
      onDelete={() => onDelete(user)}
    />
    <FormControl size="small" sx={{ minWidth: 120 }}>
      <Select
        value={permission}
        onChange={(e) => onPermissionChange(user, e.target.value)}
        variant="outlined"
      >
        {permissions.map((p) => (
          <MenuItem key={p.value} value={p.value}>
            {p.label}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  </Box>
);

const ShareDialog = ({ open, onClose, report }) => {
  const [selectedUsers, setSelectedUsers] = useState([]);
  const [userPermissions, setUserPermissions] = useState({});
  const handleShare = () => {
    // Share report with selected users
    onClose();
  };

  const handleAddUser = (_, user) => {
    if (user && !selectedUsers.find(u => u.id === user.id)) {
      setSelectedUsers([...selectedUsers, user]);
      setUserPermissions({
        ...userPermissions,
        [user.id]: 'view'
      });
    }
  };

  const handleRemoveUser = (userToRemove) => {
    setSelectedUsers(selectedUsers.filter(user => user.id !== userToRemove.id));
    const newPermissions = { ...userPermissions };
    delete newPermissions[userToRemove.id];
    setUserPermissions(newPermissions);
  };

  const handlePermissionChange = (user, newPermission) => {
    setUserPermissions({
      ...userPermissions,
      [user.id]: newPermission
    });
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Share Report</DialogTitle>
      <DialogContent>
        <Typography variant="subtitle1" gutterBottom>
          {report?.name}
        </Typography>
        
        <Autocomplete
          options={mockUsers.filter(user => 
            !selectedUsers.find(u => u.id === user.id)
          )}
          getOptionLabel={(option) => `${option.name} (${option.email})`}
          onChange={handleAddUser}
          renderInput={(params) => (
            <TextField
              {...params}
              label="Add people"
              variant="outlined"
              fullWidth
              margin="normal"
            />
          )}
        />

        <Box mt={2}>
          <Typography variant="subtitle2" gutterBottom>
            People with access
          </Typography>
          {selectedUsers.map((user) => (
            <SharedUserChip
              key={user.id} // key is a primitive
              user={user}
              permission={userPermissions[user.id]}
              onDelete={handleRemoveUser}
              onPermissionChange={handlePermissionChange}
            />
          ))}
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button
          variant="contained"
          startIcon={<ShareIcon />}
          onClick={handleShare}
          disabled={selectedUsers.length === 0}
        >
          Share
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ShareDialog;
