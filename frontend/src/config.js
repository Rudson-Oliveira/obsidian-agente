// Configuração da aplicação frontend
export const API_CONFIG = {
    // URL base do agente local
    BASE_URL: 'http://localhost:5001',
    // Timeout para requisições (ms)
    TIMEOUT: 30000,
    // Endpoints disponíveis
    ENDPOINTS: {
        HEALTH: '/health',
        OBSIDIAN_OPEN: '/obsidian/open',
        OBSIDIAN_NOTES: '/obsidian/notes',
        FILE_READ: '/file/read',
        FILE_WRITE: '/file/write',
        COMMAND_EXECUTE: '/command/execute',
    },
};
// Configuração da aplicação
export const APP_CONFIG = {
    APP_NAME: 'Obsidian Agente',
    VERSION: '1.1.0',
    THEME: 'dark',
};
