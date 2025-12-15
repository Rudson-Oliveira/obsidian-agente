import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect, useRef } from 'react';
import apiService from './services/api';
import './App.css';
function App() {
    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');
    const [isConnected, setIsConnected] = useState(false);
    const [apiKey, setApiKey] = useState(apiService.getApiKey() || '');
    const [showApiKeyInput, setShowApiKeyInput] = useState(!apiService.getApiKey());
    const [isLoading, setIsLoading] = useState(false);
    const [suggestions, setSuggestions] = useState([]);
    const messagesEndRef = useRef(null);
    const commandSuggestions = [
        'Abrir Obsidian',
        'Listar notas',
        'Status',
        'Criar nota',
        'Buscar por',
        'Explicar wikilinks',
        'Explicar tags',
        'Explicar frontmatter',
        'Explicar dataview',
        'Ajuda'
    ];
    useEffect(() => {
        checkConnection();
        const interval = setInterval(checkConnection, 30000);
        // Mensagem de boas-vindas
        if (messages.length === 0 && apiService.getApiKey()) {
            addMessage('🤖 Olá! Sou o Obsidian Agente Inteligente.\n\n' +
                'Tenho conhecimento profundo sobre Obsidian e posso ajudá-lo com:\n' +
                '• Gerenciamento de notas\n' +
                '• Explicações sobre recursos do Obsidian\n' +
                '• Automação de tarefas\n\n' +
                'Digite "ajuda" para ver todos os comandos ou comece a conversar naturalmente!', 'assistant');
        }
        return () => clearInterval(interval);
    }, []);
    useEffect(() => {
        scrollToBottom();
    }, [messages]);
    useEffect(() => {
        // Atualizar sugestões baseadas no texto digitado
        if (inputText.length > 0) {
            const filtered = commandSuggestions.filter(cmd => cmd.toLowerCase().includes(inputText.toLowerCase()));
            setSuggestions(filtered.slice(0, 5));
        }
        else {
            setSuggestions([]);
        }
    }, [inputText]);
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };
    const checkConnection = async () => {
        const result = await apiService.health();
        setIsConnected(result.success);
    };
    const handleApiKeySubmit = () => {
        if (apiKey.trim()) {
            apiService.setApiKey(apiKey.trim());
            setShowApiKeyInput(false);
            checkConnection();
            addMessage('✅ API Key configurada com sucesso! Agora você pode usar todos os comandos.', 'assistant');
        }
    };
    const addMessage = (text, sender, command, data) => {
        const newMessage = {
            id: Date.now().toString(),
            text,
            sender,
            timestamp: new Date(),
            command,
            data,
        };
        setMessages((prev) => [...prev, newMessage]);
    };
    const processIntelligentCommand = async (command) => {
        try {
            const result = await apiService.intelligentProcess(command);
            if (result.success) {
                addMessage(result.response, 'assistant', result.command, result.data);
            }
            else {
                addMessage(`❌ Erro: ${result.error}`, 'assistant');
            }
        }
        catch (error) {
            addMessage('❌ Erro ao processar comando. Verifique se o agente está rodando.', 'assistant');
        }
    };
    const handleSendMessage = async () => {
        if (!inputText.trim() || isLoading)
            return;
        const userMessage = inputText.trim();
        addMessage(userMessage, 'user');
        setInputText('');
        setIsLoading(true);
        setSuggestions([]);
        try {
            await processIntelligentCommand(userMessage);
        }
        finally {
            setIsLoading(false);
        }
    };
    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };
    const handleSuggestionClick = (suggestion) => {
        setInputText(suggestion);
        setSuggestions([]);
    };
    const formatTimestamp = (date) => {
        return date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
    };
    const renderMessageContent = (message) => {
        // Renderizar listas de notas
        if (message.data && Array.isArray(message.data)) {
            return (_jsxs("div", { children: [_jsx("p", { children: message.text }), _jsxs("div", { className: "notes-list", children: [message.data.slice(0, 10).map((note, index) => (_jsxs("div", { className: "note-item", children: ["\uD83D\uDCDD ", note.name || note.title, note.path && _jsxs("span", { className: "note-path", children: [" (", note.path, ")"] })] }, index))), message.data.length > 10 && (_jsxs("div", { className: "note-item more", children: ["... e mais ", message.data.length - 10, " notas"] }))] })] }));
        }
        // Renderizar texto com formatação
        return message.text.split('\n').map((line, index) => (_jsx("p", { children: line }, index)));
    };
    if (showApiKeyInput) {
        return (_jsx("div", { className: "app", children: _jsx("div", { className: "api-key-modal", children: _jsxs("div", { className: "api-key-content", children: [_jsx("h2", { children: "\uD83D\uDD10 Configura\u00E7\u00E3o da API Key" }), _jsx("p", { children: "Para conectar ao Obsidian Agente, voc\u00EA precisa fornecer a API Key gerada pelo agente local." }), _jsxs("p", { className: "info-text", children: ["A API Key \u00E9 exibida no terminal quando voc\u00EA inicia o agente com o comando ", _jsx("code", { children: ".\\INICIAR_AGENTE.ps1" })] }), _jsx("input", { type: "text", value: apiKey, onChange: (e) => setApiKey(e.target.value), placeholder: "Cole a API Key aqui", className: "api-key-input", onKeyPress: (e) => e.key === 'Enter' && handleApiKeySubmit(), autoFocus: true }), _jsx("button", { onClick: handleApiKeySubmit, className: "api-key-button", children: "Conectar" })] }) }) }));
    }
    return (_jsxs("div", { className: "app", children: [_jsxs("header", { className: "app-header", children: [_jsxs("div", { className: "header-left", children: [_jsx("h1", { children: "\uD83E\uDDE0 Obsidian Agente" }), _jsx("p", { className: "subtitle", children: "Seu assistente inteligente para automa\u00E7\u00E3o do Obsidian" })] }), _jsxs("div", { className: "header-right", children: [_jsxs("div", { className: `status-indicator ${isConnected ? 'connected' : 'disconnected'}`, children: [_jsx("span", { className: "status-dot" }), _jsx("span", { className: "status-text", children: isConnected ? 'Conectado' : 'Desconectado' })] }), _jsx("button", { onClick: () => setShowApiKeyInput(true), className: "settings-button", title: "Configura\u00E7\u00F5es", children: "\u2699\uFE0F" })] })] }), _jsxs("div", { className: "chat-container", children: [_jsxs("div", { className: "messages-container", children: [messages.map((message) => (_jsxs("div", { className: `message ${message.sender}`, children: [_jsx("div", { className: "message-content", children: renderMessageContent(message) }), _jsx("div", { className: "message-timestamp", children: formatTimestamp(message.timestamp) })] }, message.id))), isLoading && (_jsx("div", { className: "message assistant", children: _jsx("div", { className: "message-content", children: _jsxs("div", { className: "typing-indicator", children: [_jsx("span", {}), _jsx("span", {}), _jsx("span", {})] }) }) })), _jsx("div", { ref: messagesEndRef })] }), _jsxs("div", { className: "input-container", children: [suggestions.length > 0 && (_jsx("div", { className: "suggestions", children: suggestions.map((suggestion, index) => (_jsx("button", { className: "suggestion-button", onClick: () => handleSuggestionClick(suggestion), children: suggestion }, index))) })), _jsxs("div", { className: "input-wrapper", children: [_jsx("textarea", { value: inputText, onChange: (e) => setInputText(e.target.value), onKeyPress: handleKeyPress, placeholder: "Digite um comando para o Obsidian...", className: "message-input", rows: 1, disabled: !isConnected || isLoading }), _jsx("button", { onClick: handleSendMessage, disabled: !inputText.trim() || !isConnected || isLoading, className: "send-button", children: "\uD83D\uDE80" })] }), _jsxs("div", { className: "input-footer", children: [_jsx("span", { className: "agent-info", children: "Agent: Connected \u2022 Port: 5001" }), _jsx("span", { className: "version-info", children: "v2.0 - Intelligent Agent" })] })] })] })] }));
}
export default App;
