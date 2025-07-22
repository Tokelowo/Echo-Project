import React, { useState } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  IconButton,
  Menu,
  MenuItem,
  Divider,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';

const Comment = ({ comment, onEdit, onDelete }) => {
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <ListItem
      alignItems="flex-start"
      secondaryAction={
        <>
          <IconButton edge="end" onClick={handleClick}>
            <MoreVertIcon />
          </IconButton>
          <Menu
            anchorEl={anchorEl}
            open={open}
            onClose={handleClose}
          >
            <MenuItem onClick={() => { onEdit(comment.id); handleClose(); }}>
              <EditIcon sx={{ mr: 1 }} /> Edit
            </MenuItem>
            <MenuItem onClick={() => { onDelete(comment.id); handleClose(); }}>
              <DeleteIcon sx={{ mr: 1 }} /> Delete
            </MenuItem>
          </Menu>
        </>
      }
    >
      <ListItemAvatar>
        <Avatar src={comment.author.avatar}>{comment.author.name[0]}</Avatar>
      </ListItemAvatar>
      <ListItemText
        primary={
          <Box display="flex" alignItems="center" gap={1}>
            <Typography variant="subtitle2">{comment.author.name}</Typography>
            <Typography variant="caption" color="text.secondary">
              {new Date(comment.timestamp).toLocaleString()}
            </Typography>
          </Box>
        }
        secondary={comment.content}
      />
    </ListItem>
  );
};

const CommentSection = ({ reportId }) => {
  const [newComment, setNewComment] = useState('');
  const [comments, setComments] = useState([
    {
      id: 1,
      content: 'Great analysis on the market trends section!',
      author: {
        name: 'Alice Chen',
        avatar: '',
      },
      timestamp: new Date().toISOString(),
    },
    {
      id: 2,
      content: 'We should add more competitor benchmarking data.',
      author: {
        name: 'Bob Smith',
        avatar: '',
      },
      timestamp: new Date(Date.now() - 3600000).toISOString(),
    },
  ]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;

    const comment = {
      id: comments.length + 1,
      content: newComment,
      author: {
        name: 'Current User',
        avatar: '',
      },
      timestamp: new Date().toISOString(),
    };

    setComments([...comments, comment]);
    setNewComment('');
  };

  const handleEdit = (commentId) => {
    // Implement edit functionality
    // Edit comment functionality
  };

  const handleDelete = (commentId) => {
    setComments(comments.filter(comment => comment.id !== commentId));
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Comments
      </Typography>
      <List>
        {comments.map((comment) => (
          <React.Fragment key={comment.id}>
            <Comment
              comment={comment}
              onEdit={handleEdit}
              onDelete={handleDelete}
            />
            <Divider variant="inset" component="li" />
          </React.Fragment>
        ))}
      </List>
      <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
        <TextField
          fullWidth
          multiline
          rows={2}
          placeholder="Add a comment..."
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          variant="outlined"
          sx={{ mb: 1 }}
        />
        <Button
          variant="contained"
          endIcon={<SendIcon />}
          type="submit"
          disabled={!newComment.trim()}
        >
          Post Comment
        </Button>
      </Box>
    </Box>
  );
};

export default CommentSection;
