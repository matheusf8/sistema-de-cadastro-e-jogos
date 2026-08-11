/**
 * Componente de upload e lista de documentos
 */

import React, { useState, useRef } from 'react';
import {
  Box,
  Button,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Chip,
  CircularProgress,
  Alert,
  Snackbar,
} from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import DeleteIcon from '@mui/icons-material/Delete';
import ChatIcon from '@mui/icons-material/Chat';
import { documentsAPI } from '../services/api';

const STATUS_CONFIG = {
  processing: { label: 'Processando', color: 'warning' },
  ready: { label: 'Pronto', color: 'success' },
  error: { label: 'Erro', color: 'error' },
};

const DocumentUpload = ({ documents, loading, activeDocumentId, onUploaded, onDelete, onOpenChat }) => {
  const fileInputRef = useRef(null);
  const [uploading, setUploading] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  const showSnackbar = (message, severity = 'success') => {
    setSnackbar({ open: true, message, severity });
  };

  const handleFileSelect = async (event) => {
    const file = event.target.files?.[0];
    event.target.value = ''; // permite reenviar o mesmo arquivo depois, se precisar
    if (!file) return;

    try {
      setUploading(true);
      const response = await documentsAPI.upload(file);
      onUploaded(response.data);
      if (response.data.status === 'ready') {
        showSnackbar(`"${file.name}" processado com sucesso`);
      } else {
        showSnackbar(
          `Falha ao processar "${file.name}": ${response.data.error_message || 'erro desconhecido'}`,
          'error'
        );
      }
    } catch (error) {
      showSnackbar(error.response?.data?.detail || 'Erro ao enviar o documento', 'error');
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (documentId) => {
    try {
      await onDelete(documentId);
    } catch (error) {
      showSnackbar('Erro ao remover o documento', 'error');
    }
  };

  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
        Seus documentos
      </Typography>

      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,.txt,.md"
        hidden
        onChange={handleFileSelect}
      />
      <Button
        fullWidth
        variant="contained"
        startIcon={uploading ? <CircularProgress size={18} color="inherit" /> : <UploadFileIcon />}
        onClick={() => fileInputRef.current?.click()}
        disabled={uploading}
        sx={{ mb: 2 }}
      >
        {uploading ? 'Processando...' : 'Enviar documento (PDF, .txt, .md)'}
      </Button>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 3 }}>
          <CircularProgress size={24} />
        </Box>
      ) : documents.length === 0 ? (
        <Typography color="text.secondary" sx={{ textAlign: 'center', py: 3 }}>
          Nenhum documento enviado ainda
        </Typography>
      ) : (
        <List disablePadding>
          {documents.map((doc) => {
            const status = STATUS_CONFIG[doc.status] || STATUS_CONFIG.processing;
            const isActive = doc.id === activeDocumentId;
            return (
              <ListItem
                key={doc.id}
                sx={{
                  border: '1px solid',
                  borderColor: isActive ? 'primary.main' : 'divider',
                  borderRadius: 1,
                  mb: 1,
                  pr: 12,
                }}
                secondaryAction={
                  <Box sx={{ display: 'flex', gap: 0.5 }}>
                    <IconButton
                      size="small"
                      color="primary"
                      title="Conversar com este documento"
                      disabled={doc.status !== 'ready'}
                      onClick={() => onOpenChat(doc)}
                    >
                      <ChatIcon fontSize="small" />
                    </IconButton>
                    <IconButton
                      size="small"
                      color="error"
                      title="Remover documento"
                      onClick={() => handleDelete(doc.id)}
                    >
                      <DeleteIcon fontSize="small" />
                    </IconButton>
                  </Box>
                }
              >
                <ListItemText
                  primary={doc.filename}
                  secondaryTypographyProps={{ component: 'div' }}
                  secondary={
                    <Chip label={status.label} color={status.color} size="small" sx={{ mt: 0.5 }} />
                  }
                />
              </ListItem>
            );
          })}
        </List>
      )}

      <Snackbar
        open={snackbar.open}
        autoHideDuration={5000}
        onClose={() => setSnackbar((prev) => ({ ...prev, open: false }))}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Paper>
  );
};

export default DocumentUpload;
