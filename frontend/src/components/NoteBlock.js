/**
 * Componente de Bloco de Notas
 * CRUD completo de notas com interface intuitiva
 */

import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Button,
  TextField,
  Paper,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Typography,
  CircularProgress,
  Alert,
  Snackbar,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import AddIcon from '@mui/icons-material/Add';
import { notesAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

const NoteBlock = () => {
  const { user } = useAuth();
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [openDialog, setOpenDialog] = useState(false);
  const [noteToDelete, setNoteToDelete] = useState(null);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({ title: '', content: '' });
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  const loadNotes = useCallback(async () => {
    try {
      setLoading(true);
      const response = await notesAPI.getNotes();
      setNotes(response.data);
    } catch (error) {
      console.error('Erro ao carregar notas:', error);
      showSnackbar('Erro ao carregar notas', 'error');
    } finally {
      setLoading(false);
    }
  }, []);

  // Carregar notas sempre que o usuário autenticado mudar
  useEffect(() => {
    loadNotes();
  }, [user, loadNotes]);

  const showSnackbar = (message, severity = 'success') => {
    setSnackbar({ open: true, message, severity });
  };

  const handleCloseSnackbar = () => {
    setSnackbar((prev) => ({ ...prev, open: false }));
  };

  // Abrir dialog para nova nota
  const handleOpenDialog = () => {
    setEditingId(null);
    setFormData({ title: '', content: '' });
    setOpenDialog(true);
  };

  // Abrir dialog para editar nota
  const handleEditNote = (note) => {
    setEditingId(note.id);
    setFormData({ title: note.title, content: note.content });
    setOpenDialog(true);
  };

  // Fechar dialog
  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingId(null);
    setFormData({ title: '', content: '' });
  };

  // Salvar nota
  const handleSaveNote = async () => {
    if (!formData.title.trim()) {
      showSnackbar('O título não pode ser vazio', 'warning');
      return;
    }

    try {
      if (editingId) {
        await notesAPI.updateNote(editingId, formData);
        showSnackbar('Nota atualizada com sucesso');
      } else {
        await notesAPI.createNote(formData);
        showSnackbar('Nota criada com sucesso');
      }
      loadNotes();
      handleCloseDialog();
    } catch (error) {
      console.error('Erro ao salvar nota:', error);
      showSnackbar('Erro ao salvar nota', 'error');
    }
  };

  // Pedir confirmação antes de deletar
  const handleDeleteNote = (note) => {
    setNoteToDelete(note);
  };

  const cancelDeleteNote = () => {
    setNoteToDelete(null);
  };

  const confirmDeleteNote = async () => {
    if (!noteToDelete) return;

    try {
      await notesAPI.deleteNote(noteToDelete.id);
      loadNotes();
      showSnackbar('Nota deletada com sucesso');
    } catch (error) {
      console.error('Erro ao deletar nota:', error);
      showSnackbar('Erro ao deletar nota', 'error');
    } finally {
      setNoteToDelete(null);
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '500px' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
          Bloco de Notas
        </Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={handleOpenDialog}
        >
          Nova Nota
        </Button>
      </Box>

      {/* Lista de Notas */}
      {notes.length === 0 ? (
        <Paper sx={{ p: 3, textAlign: 'center' }}>
          <Typography color="textSecondary">Nenhuma nota criada ainda</Typography>
        </Paper>
      ) : (
        <Paper>
          <List>
            {notes.map((note, index) => (
              <React.Fragment key={note.id}>
                <ListItem
                  sx={{
                    position: 'relative',
                    pr: 12,
                    '&:hover': {
                      backgroundColor: 'action.hover',
                    },
                  }}
                >
                  <ListItemText
                    primary={note.title}
                    secondary={note.content ? note.content.substring(0, 100) + '...' : 'Sem conteúdo'}
                  />
                  <Box
                    sx={{
                      position: 'absolute',
                      right: 8,
                      top: '50%',
                      transform: 'translateY(-50%)',
                      display: 'flex',
                      gap: 1,
                    }}
                  >
                    <IconButton
                      size="small"
                      aria-label="editar"
                      onClick={() => handleEditNote(note)}
                      title="Editar nota"
                    >
                      <EditIcon />
                    </IconButton>
                    <IconButton
                      size="small"
                      aria-label="deletar"
                      onClick={() => handleDeleteNote(note)}
                      color="error"
                      title="Deletar nota"
                    >
                      <DeleteIcon />
                    </IconButton>
                  </Box>
                </ListItem>
                {index < notes.length - 1 && <hr style={{ margin: 0 }} />}
              </React.Fragment>
            ))}
          </List>
        </Paper>
      )}

      {/* Dialog de criar/editar */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingId ? 'Editar Nota' : 'Nova Nota'}
        </DialogTitle>
        <DialogContent sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 2 }}>
          <TextField
            label="Título"
            fullWidth
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            placeholder="Digite o título da nota"
          />
          <TextField
            label="Conteúdo"
            fullWidth
            multiline
            rows={6}
            value={formData.content}
            onChange={(e) => setFormData({ ...formData, content: e.target.value })}
            placeholder="Digite o conteúdo da nota"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancelar</Button>
          <Button onClick={handleSaveNote} variant="contained">
            Salvar
          </Button>
        </DialogActions>
      </Dialog>

      {/* Dialog de confirmação de exclusão */}
      <Dialog open={Boolean(noteToDelete)} onClose={cancelDeleteNote} maxWidth="xs" fullWidth>
        <DialogTitle>Deletar nota?</DialogTitle>
        <DialogContent>
          <Typography>
            Tem certeza que deseja deletar "{noteToDelete?.title}"? Essa ação não pode ser desfeita.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={cancelDeleteNote}>Cancelar</Button>
          <Button onClick={confirmDeleteNote} variant="contained" color="error">
            Deletar
          </Button>
        </DialogActions>
      </Dialog>

      {/* Feedback de ações */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default NoteBlock;
