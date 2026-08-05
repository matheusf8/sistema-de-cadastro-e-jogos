/**
 * Componente do Jogo da Cobrinha
 * Versão clássica do jogo dos celulares antigos
 */

import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Button,
  Typography,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';

// Configurações do jogo (não dependem de state/props, ficam fora do componente)
const CANVAS_SIZE = 400;
const GRID_SIZE = 20;
const GRID_COUNT = CANVAS_SIZE / GRID_SIZE;

// Desenhar o estado atual do jogo no canvas
const draw = (ctx, gameState) => {
  // Limpar canvas
  ctx.fillStyle = '#f0f0f0';
  ctx.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);

  // Desenhar grade
  ctx.strokeStyle = '#ddd';
  ctx.lineWidth = 0.5;
  for (let i = 0; i <= GRID_COUNT; i++) {
    ctx.beginPath();
    ctx.moveTo(i * GRID_SIZE, 0);
    ctx.lineTo(i * GRID_SIZE, CANVAS_SIZE);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(0, i * GRID_SIZE);
    ctx.lineTo(CANVAS_SIZE, i * GRID_SIZE);
    ctx.stroke();
  }

  // Desenhar comida
  ctx.fillStyle = '#FF6B6B';
  ctx.fillRect(
    gameState.food.x * GRID_SIZE + 1,
    gameState.food.y * GRID_SIZE + 1,
    GRID_SIZE - 2,
    GRID_SIZE - 2
  );

  // Desenhar cobra
  gameState.snake.forEach((segment, index) => {
    if (index === 0) {
      ctx.fillStyle = '#4CAF50';
    } else {
      ctx.fillStyle = '#81C784';
    }
    ctx.fillRect(
      segment.x * GRID_SIZE + 1,
      segment.y * GRID_SIZE + 1,
      GRID_SIZE - 2,
      GRID_SIZE - 2
    );
  });
};

const SnakeGame = () => {
  const canvasRef = useRef(null);
  const [gameRunning, setGameRunning] = useState(false);
  const [score, setScore] = useState(0);
  const [gameOver, setGameOver] = useState(false);
  const [openDialog, setOpenDialog] = useState(false);

  // Estado do jogo
  const gameStateRef = useRef({
    snake: [{ x: 10, y: 10 }],
    food: { x: 15, y: 15 },
    direction: { x: 1, y: 0 },
    nextDirection: { x: 1, y: 0 },
    score: 0,
  });

  // Lógica do jogo
  const gameLoop = useRef(() => {
    const gameState = gameStateRef.current;
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    // Mover cobra
    gameState.direction = gameState.nextDirection;
    const head = gameState.snake[0];
    const newHead = {
      x: (head.x + gameState.direction.x + GRID_COUNT) % GRID_COUNT,
      y: (head.y + gameState.direction.y + GRID_COUNT) % GRID_COUNT,
    };

    // Verificar colisão com corpo
    if (gameState.snake.some((seg) => seg.x === newHead.x && seg.y === newHead.y)) {
      setGameOver(true);
      setGameRunning(false);
      setOpenDialog(true);
      return;
    }

    gameState.snake.unshift(newHead);

    // Verificar colisão com comida
    if (newHead.x === gameState.food.x && newHead.y === gameState.food.y) {
      gameState.score += 10;
      setScore(gameState.score);

      // Gerar nova comida
      gameState.food = {
        x: Math.floor(Math.random() * GRID_COUNT),
        y: Math.floor(Math.random() * GRID_COUNT),
      };
    } else {
      gameState.snake.pop();
    }

    draw(ctx, gameState);
  });

  // Iniciar jogo
  const startGame = () => {
    gameStateRef.current = {
      snake: [{ x: 10, y: 10 }],
      food: { x: 15, y: 15 },
      direction: { x: 1, y: 0 },
      nextDirection: { x: 1, y: 0 },
      score: 0,
    };
    setScore(0);
    setGameOver(false);
    setGameRunning(true);
    setOpenDialog(false);
  };

  // Loop do jogo
  useEffect(() => {
    if (!gameRunning) return;

    const interval = setInterval(gameLoop.current, 100);
    return () => clearInterval(interval);
  }, [gameRunning]);

  // Desenho inicial
  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext('2d');
      draw(ctx, gameStateRef.current);
    }
  }, []);

  // Controles
  useEffect(() => {
    const handleKeyPress = (e) => {
      if (!gameRunning) return;

      const gameState = gameStateRef.current;
      const key = e.key.toLowerCase();

      switch (key) {
        case 'arrowup':
        case 'w':
          if (gameState.direction.y === 0) {
            gameState.nextDirection = { x: 0, y: -1 };
          }
          e.preventDefault();
          break;
        case 'arrowdown':
        case 's':
          if (gameState.direction.y === 0) {
            gameState.nextDirection = { x: 0, y: 1 };
          }
          e.preventDefault();
          break;
        case 'arrowleft':
        case 'a':
          if (gameState.direction.x === 0) {
            gameState.nextDirection = { x: -1, y: 0 };
          }
          e.preventDefault();
          break;
        case 'arrowright':
        case 'd':
          if (gameState.direction.x === 0) {
            gameState.nextDirection = { x: 1, y: 0 };
          }
          e.preventDefault();
          break;
        default:
          break;
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [gameRunning]);

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <Typography variant="h5" sx={{ mb: 2, fontWeight: 'bold' }}>
        Jogo da Cobrinha
      </Typography>

      <Paper sx={{ p: 2, mb: 2, backgroundColor: '#f0f0f0' }}>
        <canvas
          ref={canvasRef}
          width={CANVAS_SIZE}
          height={CANVAS_SIZE}
          style={{ border: '2px solid #333' }}
        />
      </Paper>

      <Box sx={{ mb: 2, textAlign: 'center' }}>
        <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
          Pontuação: {score}
        </Typography>
        <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
          Use as setas ou WASD para controlar a cobra
        </Typography>
      </Box>

      <Button
        variant="contained"
        color={gameRunning ? 'warning' : 'success'}
        onClick={() => {
          if (gameRunning) {
            // Pausar
            setGameRunning(false);
          } else if (gameOver) {
            // Reiniciar após game over
            startGame();
          } else {
            // Iniciar pela primeira vez
            setGameRunning(true);
          }
        }}
      >
        {gameRunning ? 'Pausar' : gameOver ? 'Tentar Novamente' : 'Iniciar'}
      </Button>

      {/* Dialog de Game Over */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
        <DialogTitle>Game Over!</DialogTitle>
        <DialogContent sx={{ pt: 2 }}>
          <Typography variant="h6" sx={{ textAlign: 'center' }}>
            Pontuação Final: {score}
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Fechar</Button>
          <Button onClick={startGame} variant="contained">
            Jogar Novamente
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default SnakeGame;
