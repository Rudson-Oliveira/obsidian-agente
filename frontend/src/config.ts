// Configuração da aplicação frontend
// VERSÃO CORRIGIDA v5.0

export const API_CONFIG = {
  // URL base do agente local
  BASE_URL: 'http://localhost:5001',
  
  // Timeout para requisições (ms)
  TIMEOUT: 60000,
  
  // Endpoints disponíveis
  ENDPOINTS: {
    HEALTH: '/health',
    CONFIG: '/config',
    OBSIDIAN_OPEN: '/obsidian/open',
    OBSIDIAN_NOTES: '/obsidian/notes',
    FILE_READ: '/file/read',
    FILE_WRITE: '/file/write',
    COMMAND_EXECUTE: '/command/execute',
    INTELLIGENT_PROCESS: '/intelligent/process',
  },
};

// Configuração da aplicação
export const APP_CONFIG = {
  APP_NAME: 'Obsidian Agente',
  VERSION: '5.0.0',
  THEME: 'dark',
  
  // Configurações de chat
  CHAT: {
    MAX_MESSAGES: 100,
    AUTO_SCROLL: true,
    TYPING_INDICATOR_DELAY: 500,
  },
  
  // Configurações de retry
  RETRY: {
    MAX_ATTEMPTS: 3,
    DELAY_MS: 1000,
  },
};

// API Key padrão (será substituída pela do servidor)
export const DEFAULT_API_KEY = 'heDuf3s4Y_EXwISRm2q2O1UPgi0zWbskf4_suT3cdus';

