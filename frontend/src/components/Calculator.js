/**
 * Componente de Calculadora
 * Interface simples e bonita para operações matemáticas básicas
 */

import React, { useState } from 'react';
import {
  Box,
  Grid,
  Button,
  TextField,
  Typography,
  Paper,
} from '@mui/material';

const Calculator = () => {
  const [display, setDisplay] = useState('0');
  const [previousValue, setPreviousValue] = useState(null);
  const [operation, setOperation] = useState(null);
  const [newNumber, setNewNumber] = useState(true);

  // Adicionar número ao display
  const handleNumberClick = (number) => {
    if (newNumber) {
      setDisplay(String(number));
      setNewNumber(false);
    } else {
      setDisplay(display === '0' ? String(number) : display + number);
    }
  };

  // Adicionar vírgula
  const handleDecimal = () => {
    if (newNumber) {
      setDisplay('0.');
      setNewNumber(false);
    } else if (!display.includes('.')) {
      setDisplay(display + '.');
    }
  };

  // Selecionar operação
  const handleOperation = (nextOperation) => {
    const inputValue = parseFloat(display);

    if (previousValue === null) {
      setPreviousValue(inputValue);
    } else if (operation) {
      const result = performCalculation(previousValue, inputValue, operation);
      setDisplay(String(result));
      setPreviousValue(result);
    }

    setNewNumber(true);
    setOperation(nextOperation);
  };

  // Executar cálculo
  const performCalculation = (prev, current, op) => {
    switch (op) {
      case '+':
        return prev + current;
      case '-':
        return prev - current;
      case '*':
        return prev * current;
      case '/':
        return prev / current;
      default:
        return current;
    }
  };

  // Calcular resultado
  const handleEquals = () => {
    if (operation && previousValue !== null) {
      const result = performCalculation(previousValue, parseFloat(display), operation);
      setDisplay(String(result));
      setPreviousValue(null);
      setOperation(null);
      setNewNumber(true);
    }
  };

  // Limpar
  const handleClear = () => {
    setDisplay('0');
    setPreviousValue(null);
    setOperation(null);
    setNewNumber(true);
  };

  const buttonStyle = {
    fontSize: '1.5rem',
    padding: '20px',
    fontWeight: 'bold',
  };

  const operationButtonStyle = {
    ...buttonStyle,
    backgroundColor: '#FF9800',
    color: 'white',
    '&:hover': {
      backgroundColor: '#F57C00',
    },
  };

  return (
    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '500px' }}>
      <Paper sx={{ p: 3, width: '100%', maxWidth: '400px' }}>
        <Typography variant="h5" sx={{ mb: 2, fontWeight: 'bold' }}>
          Calculadora
        </Typography>

        {/* Display */}
        <TextField
          fullWidth
          value={display}
          InputProps={{ readOnly: true }}
          variant="outlined"
          sx={{
            mb: 2,
            '& .MuiInputBase-input': {
              fontSize: '2rem',
              textAlign: 'right',
              fontWeight: 'bold',
            },
          }}
        />

        {/* Grid de Botões */}
        <Grid container spacing={1}>
          {/* Linha 1 */}
          <Grid item xs={9}>
            <Button fullWidth variant="contained" color="error" onClick={handleClear} sx={buttonStyle}>
              C
            </Button>
          </Grid>
          <Grid item xs={3}>
            <Button fullWidth variant="contained" sx={operationButtonStyle} onClick={() => handleOperation('/')}>
              ÷
            </Button>
          </Grid>

          {/* Linha 2 */}
          <Grid item xs={3}>
            <Button fullWidth variant="contained" onClick={() => handleNumberClick(7)} sx={buttonStyle}>
              7
            </Button>
          </Grid>
          <Grid item xs={3}>
            <Button fullWidth variant="contained" onClick={() => handleNumberClick(8)} sx={buttonStyle}>
              8
            </Button>
          </Grid>
          <Grid item xs={3}>
            <Button fullWidth variant="contained" onClick={() => handleNumberClick(9)} sx={buttonStyle}>
              9
            </Button>
          </Grid>
          <Grid item xs={3}>
            <Button fullWidth variant="contained" sx={operationButtonStyle} onClick={() => handleOperation('*')}>
              ×
            </Button>
          </Grid>

          {/* Linha 3 */}
          <Grid item xs={3}>
            <Button fullWidth variant="contained" onClick={() => handleNumberClick(4)} sx={buttonStyle}>
              4
            </Button>
          </Grid>
          <Grid item xs={3}>
            <Button fullWidth variant="contained" onClick={() => handleNumberClick(5)} sx={buttonStyle}>
              5
            </Button>
          </Grid>
          <Grid item xs={3}>
            <Button fullWidth variant="contained" onClick={() => handleNumberClick(6)} sx={buttonStyle}>
              6
            </Button>
          </Grid>
          <Grid item xs={3}>
            <Button fullWidth variant="contained" sx={operationButtonStyle} onClick={() => handleOperation('-')}>
              −
            </Button>
          </Grid>

          {/* Linha 4 */}
          <Grid item xs={3}>
            <Button fullWidth variant="contained" onClick={() => handleNumberClick(1)} sx={buttonStyle}>
              1
            </Button>
          </Grid>
          <Grid item xs={3}>
            <Button fullWidth variant="contained" onClick={() => handleNumberClick(2)} sx={buttonStyle}>
              2
            </Button>
          </Grid>
          <Grid item xs={3}>
            <Button fullWidth variant="contained" onClick={() => handleNumberClick(3)} sx={buttonStyle}>
              3
            </Button>
          </Grid>
          <Grid item xs={3}>
            <Button fullWidth variant="contained" sx={operationButtonStyle} onClick={() => handleOperation('+')}>
              +
            </Button>
          </Grid>

          {/* Linha 5 */}
          <Grid item xs={6}>
            <Button fullWidth variant="contained" onClick={() => handleNumberClick(0)} sx={buttonStyle}>
              0
            </Button>
          </Grid>
          <Grid item xs={3}>
            <Button fullWidth variant="contained" onClick={handleDecimal} sx={buttonStyle}>
              .
            </Button>
          </Grid>
          <Grid item xs={3}>
            <Button fullWidth variant="contained" color="success" onClick={handleEquals} sx={buttonStyle}>
              =
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default Calculator;
