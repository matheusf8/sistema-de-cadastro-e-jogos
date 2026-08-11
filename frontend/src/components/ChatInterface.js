/**
 * Componente de chat com um documento
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  IconButton,
  CircularProgress,
  Alert,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { chatAPI } from '../services/api';

const ChatInterface = ({ session }) => {
  const [messages, setMessages] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(true);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [error, setError] = useState('');
  const bottomRef = useRef(null);

  const loadMessages = useCallback(async () => {
    try {
      setLoadingHistory(true);
      const response = await chatAPI.listMessages(session.id);
      setMessages(response.data);
    } catch (err) {
      setError('Erro ao carregar o histórico da conversa');
    } finally {
      setLoadingHistory(false);
    }
  }, [session.id]);

  useEffect(() => {
    loadMessages();
  }, [loadMessages]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, sending]);

  const handleSend = async (event) => {
    event.preventDefault();
    const content = input.trim();
    if (!content || sending) return;

    setError('');
    setInput('');
    setSending(true);

    // Otimista: mostra a pergunta do usuário na hora, sem esperar a IA responder
    const optimisticId = `temp-${Date.now()}`;
    setMessages((prev) => [...prev, { id: optimisticId, role: 'user', content }]);

    try {
      const response = await chatAPI.sendMessage(session.id, content);
      setMessages((prev) => [...prev, response.data]);
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao consultar a IA. Tente novamente.');
      setMessages((prev) => prev.filter((m) => m.id !== optimisticId));
      setInput(content);
    } finally {
      setSending(false);
    }
  };

  return (
    <Paper sx={{ display: 'flex', flexDirection: 'column', height: '70vh' }}>
      <Box sx={{ p: 2, borderBottom: '1px solid', borderColor: 'divider' }}>
        <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
          {session.document.filename}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          As respostas são baseadas apenas no conteúdo deste documento
        </Typography>
      </Box>

      <Box sx={{ flex: 1, overflowY: 'auto', p: 2 }}>
        {loadingHistory ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', py: 3 }}>
            <CircularProgress size={24} />
          </Box>
        ) : messages.length === 0 ? (
          <Typography color="text.secondary" sx={{ textAlign: 'center', py: 3 }}>
            Faça a primeira pergunta sobre o documento
          </Typography>
        ) : (
          messages.map((message) => (
            <Box
              key={message.id}
              sx={{
                display: 'flex',
                justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
                mb: 1.5,
              }}
            >
              <Box
                sx={{
                  maxWidth: '75%',
                  px: 2,
                  py: 1,
                  borderRadius: 2,
                  bgcolor: message.role === 'user' ? 'primary.main' : 'grey.100',
                  color: message.role === 'user' ? 'primary.contrastText' : 'text.primary',
                  whiteSpace: 'pre-wrap',
                }}
              >
                <Typography variant="body2">{message.content}</Typography>
              </Box>
            </Box>
          ))
        )}
        {sending && (
          <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 1.5 }}>
            <Box sx={{ px: 2, py: 1, borderRadius: 2, bgcolor: 'grey.100' }}>
              <CircularProgress size={16} />
            </Box>
          </Box>
        )}
        <div ref={bottomRef} />
      </Box>

      {error && (
        <Alert severity="error" sx={{ mx: 2, mb: 1 }}>
          {error}
        </Alert>
      )}

      <Box
        component="form"
        onSubmit={handleSend}
        sx={{ display: 'flex', gap: 1, p: 2, borderTop: '1px solid', borderColor: 'divider' }}
      >
        <TextField
          fullWidth
          size="small"
          placeholder="Pergunte algo sobre o documento..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={sending}
        />
        <IconButton type="submit" color="primary" disabled={sending || !input.trim()}>
          <SendIcon />
        </IconButton>
      </Box>
    </Paper>
  );
};

export default ChatInterface;
