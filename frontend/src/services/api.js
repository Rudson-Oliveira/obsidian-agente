import axios from 'axios';
import { API_CONFIG } from '../config';
class ApiService {
    constructor() {
        Object.defineProperty(this, "client", {
            enumerable: true,
            configurable: true,
            writable: true,
            value: void 0
        });
        Object.defineProperty(this, "apiKey", {
            enumerable: true,
            configurable: true,
            writable: true,
            value: null
        });
        this.client = axios.create({
            baseURL: API_CONFIG.BASE_URL,
            timeout: API_CONFIG.TIMEOUT,
        });
        // Interceptor para adicionar API Key
        this.client.interceptors.request.use((config) => {
            if (this.apiKey) {
                config.headers.Authorization = `Bearer ${this.apiKey}`;
            }
            return config;
        });
        // Interceptor para tratamento de erros
        this.client.interceptors.response.use((response) => response, (error) => {
            console.error('API Error:', error.message);
            return Promise.reject(error);
        });
        // Carregar API Key do localStorage
        const savedApiKey = localStorage.getItem('obsidian_api_key');
        if (savedApiKey) {
            this.apiKey = savedApiKey;
        }
    }
    setApiKey(key) {
        this.apiKey = key;
        localStorage.setItem('obsidian_api_key', key);
    }
    getApiKey() {
        return this.apiKey;
    }
    clearApiKey() {
        this.apiKey = null;
        localStorage.removeItem('obsidian_api_key');
    }
    async health() {
        try {
            const response = await this.client.get(API_CONFIG.ENDPOINTS.HEALTH);
            return {
                success: true,
                data: response.data,
            };
        }
        catch (error) {
            return {
                success: false,
                error: 'Falha ao conectar ao agente',
            };
        }
    }
    async openObsidian() {
        try {
            const response = await this.client.post(API_CONFIG.ENDPOINTS.OBSIDIAN_OPEN);
            return {
                success: response.data.success,
                message: response.data.message,
            };
        }
        catch (error) {
            return {
                success: false,
                error: 'Falha ao abrir Obsidian',
            };
        }
    }
    async listNotes() {
        try {
            const response = await this.client.get(API_CONFIG.ENDPOINTS.OBSIDIAN_NOTES);
            return {
                success: true,
                data: response.data.notes,
            };
        }
        catch (error) {
            return {
                success: false,
                error: 'Falha ao listar notas',
            };
        }
    }
    async readFile(path) {
        try {
            const response = await this.client.post(API_CONFIG.ENDPOINTS.FILE_READ, {
                path,
            });
            return {
                success: response.data.success,
                data: response.data.content,
            };
        }
        catch (error) {
            return {
                success: false,
                error: 'Falha ao ler arquivo',
            };
        }
    }
    async writeFile(path, content) {
        try {
            const response = await this.client.post(API_CONFIG.ENDPOINTS.FILE_WRITE, {
                path,
                content,
            });
            return {
                success: response.data.success,
                message: response.data.message,
            };
        }
        catch (error) {
            return {
                success: false,
                error: 'Falha ao escrever arquivo',
            };
        }
    }
    async executeCommand(command) {
        try {
            const response = await this.client.post(API_CONFIG.ENDPOINTS.COMMAND_EXECUTE, {
                command,
            });
            return {
                success: response.data.success,
                data: response.data.output,
            };
        }
        catch (error) {
            return {
                success: false,
                error: 'Falha ao executar comando',
            };
        }
    }
    async createNote(title, content = '') {
        try {
            const response = await this.client.post('/obsidian/note/create', {
                title,
                content,
            });
            return {
                success: response.data.success,
                message: response.data.message,
                data: response.data.path,
            };
        }
        catch (error) {
            return {
                success: false,
                error: error.response?.data?.error || 'Falha ao criar nota',
            };
        }
    }
    async searchNotes(query) {
        try {
            const response = await this.client.post('/obsidian/note/search', {
                query,
            });
            return {
                success: response.data.success,
                data: response.data.results,
            };
        }
        catch (error) {
            return {
                success: false,
                error: error.response?.data?.error || 'Falha ao buscar notas',
            };
        }
    }
    async configureVault(vaultPath) {
        try {
            const response = await this.client.post('/obsidian/vault/configure', {
                vault_path: vaultPath,
            });
            return {
                success: response.data.success,
                message: response.data.message,
            };
        }
        catch (error) {
            return {
                success: false,
                error: error.response?.data?.error || 'Falha ao configurar vault',
            };
        }
    }
    async intelligentProcess(text) {
        try {
            const response = await this.client.post('/intelligent/process', {
                text,
            });
            return {
                success: response.data.success,
                data: response.data.data,
                message: response.data.response,
                ...response.data,
            };
        }
        catch (error) {
            return {
                success: false,
                error: error.response?.data?.error || 'Falha ao processar comando',
            };
        }
    }
}
export default new ApiService();
