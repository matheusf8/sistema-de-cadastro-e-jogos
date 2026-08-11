/**
 * Página de Dashboard
 * Lista de documentos, upload e chat com o documento selecionado
 */

import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Box, AppBar, Toolbar, Typography, Button, Grid } from '@mui/material';
import LogoutIcon from '@mui/icons-material/Logout';
import { useAuth } from '../context/AuthContext';
import { documentsAPI, chatAPI } from '../services/api';
import DocumentUpload from '../components/DocumentUpload';
import ChatInterface from '../components/ChatInterface';

const Dashboard = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const [documents, setDocuments] = useState([]);
  const [loadingDocuments, setLoadingDocuments] = useState(true);
  const [activeSession, setActiveSession] = useState(null); // { id, document }

  const loadDocuments = useCallback(async () => {
    try {
      setLoadingDocuments(true);
      const response = await documentsAPI.list();
      setDocuments(response.data);
    } catch (error) {
      console.error('Erro ao carregar documentos:', error);
    } finally {
      setLoadingDocuments(false);
    }
  }, []);

  useEffect(() => {
    loadDocuments();
  }, [loadDocuments]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleUploaded = (document) => {
    setDocuments((prev) => [document, ...prev]);
  };

  const handleDelete = async (documentId) => {
    await documentsAPI.remove(documentId);
    setDocuments((prev) => prev.filter((doc) => doc.id !== documentId));
    setActiveSession((prev) => (prev?.document.id === documentId ? null : prev));
  };

  const handleOpenChat = async (document) => {
    // Reaproveita uma sessão existente para o documento, se houver; senão cria uma nova.
    const { data: sessions } = await chatAPI.listSessions();
    const existing = sessions.find((s) => s.document_id === document.id);
    const session = existing || (await chatAPI.createSession(document.id, document.filename)).data;
    setActiveSession({ id: session.id, document });
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="sticky">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1, fontWeight: 'bold' }}>
            Chat com Documentos
          </Typography>
          <Typography sx={{ mr: 2 }}>Olá, {user?.full_name || user?.username}!</Typography>
          <Button color="inherit" onClick={handleLogout} startIcon={<LogoutIcon />}>
            Sair
          </Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ flex: 1, py: 3 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <DocumentUpload
              documents={documents}
              loading={loadingDocuments}
              activeDocumentId={activeSession?.document.id}
              onUploaded={handleUploaded}
              onDelete={handleDelete}
              onOpenChat={handleOpenChat}
            />
          </Grid>
          <Grid item xs={12} md={8}>
            {activeSession ? (
              <ChatInterface session={activeSession} />
            ) : (
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  minHeight: 400,
                  border: '1px dashed',
                  borderColor: 'divider',
                  borderRadius: 2,
                  color: 'text.secondary',
                }}
              >
                <Typography>Envie um documento e clique em "Conversar" para começar</Typography>
              </Box>
            )}
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default Dashboard;
