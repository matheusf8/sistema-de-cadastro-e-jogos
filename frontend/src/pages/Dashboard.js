/**
 * Página de Dashboard
 * Interface principal com as três abas (Calculadora, Bloco de Notas, Jogo)
 */

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  AppBar,
  Toolbar,
  Typography,
  Button,
  Tabs,
  Tab,
} from '@mui/material';
import LogoutIcon from '@mui/icons-material/Logout';
import { useAuth } from '../context/AuthContext';
import Calculator from '../components/Calculator';
import NoteBlock from '../components/NoteBlock';
import SnakeGame from '../components/SnakeGame';

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`tabpanel-${index}`}
      aria-labelledby={`tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const Dashboard = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      {/* App Bar */}
      <AppBar position="sticky">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1, fontWeight: 'bold' }}>
            Sistema de Funcionais
          </Typography>
          <Typography sx={{ mr: 2 }}>
            Bem-vindo, {user?.full_name || user?.username}!
          </Typography>
          <Button
            color="inherit"
            onClick={handleLogout}
            startIcon={<LogoutIcon />}
          >
            Sair
          </Button>
        </Toolbar>
      </AppBar>

      {/* Conteúdo Principal */}
      <Container maxWidth="lg" sx={{ flex: 1, py: 2 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="abas de funcionalidades">
            <Tab label="Calculadora" id="tab-0" aria-controls="tabpanel-0" />
            <Tab label="Bloco de Notas" id="tab-1" aria-controls="tabpanel-1" />
            <Tab label="Jogo da Cobrinha" id="tab-2" aria-controls="tabpanel-2" />
          </Tabs>
        </Box>

        {/* Aba 1: Calculadora */}
        <TabPanel value={tabValue} index={0}>
          <Calculator />
        </TabPanel>

        {/* Aba 2: Bloco de Notas */}
        <TabPanel value={tabValue} index={1}>
          <NoteBlock />
        </TabPanel>

        {/* Aba 3: Jogo da Cobrinha */}
        <TabPanel value={tabValue} index={2}>
          <SnakeGame />
        </TabPanel>
      </Container>
    </Box>
  );
};

export default Dashboard;
