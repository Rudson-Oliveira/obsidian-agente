import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect, useRef } from 'react';
import './App.css';
function App() {
    const [messages, setMessages] = useState([
        {
            id: '1',
            text: 'Olá! Sou o Obsidian Agente Inteligente v2.0. 🟠\n\nEstou conectado ao seu vault e pronto para ajudar. Posso criar notas, buscar informações, explicar conceitos ou automatizar tarefas.\n\nComo posso ser útil hoje?',
            sender: 'assistant',
            timestamp: new Date(),
            type: 'text'
        }
    ]);
    const [inputText, setInputText] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [isConnected, setIsConnected] = useState(true);
    const [activeNav, setActiveNav] = useState('chat');
    const messagesEndRef = useRef(null);
    const messagesAreaRef = useRef(null);
    const apiKey = 'heDuf3s4Y_EXwISRm2q2O1UPgi0zWbskf4_suT3cdus';
    const quickActions = ['📝 Criar nota', '🔍 Buscar', '📊 Status', '❓ Ajuda'];
    useEffect(() => {
        scrollToBottom();
    }, [messages]);
    useEffect(() => {
        checkConnection();
        const interval = setInterval(checkConnection, 30000);
        return () => clearInterval(interval);
    }, []);
    const scrollToBottom = () => {
        if (messagesAreaRef.current) {
            messagesAreaRef.current.scrollTop = messagesAreaRef.current.scrollHeight;
        }
    };
    const checkConnection = async () => {
        try {
            const response = await fetch('http://localhost:5001/health', {
                method: 'GET',
                headers: { 'Authorization': 'Bearer ' + apiKey }
            });
            setIsConnected(response.ok);
        }
        catch {
            setIsConnected(false);
        }
    };
    const handleSendMessage = async () => {
        if (!inputText.trim() || isLoading)
            return;
        const userMessage = {
            id: Date.now().toString(),
            text: inputText,
            sender: 'user',
            timestamp: new Date(),
            type: 'text'
        };
        setMessages(prev => [...prev, userMessage]);
        const messageText = inputText;
        setInputText('');
        setIsLoading(true);
        try {
            // CORREÇÃO: Usar o endpoint correto /intelligent/process com parâmetro "text"
            const response = await fetch('http://localhost:5001/intelligent/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + apiKey
                },
                body: JSON.stringify({ text: messageText }) // CORREÇÃO: usar "text" em vez de "message"
            });
            const data = await response.json();
            const assistantMessage = {
                id: (Date.now() + 1).toString(),
                text: data.response || data.message || 'Resposta recebida',
                sender: 'assistant',
                timestamp: new Date(),
                type: data.type || 'text',
                data: data.data
            };
            setMessages(prev => [...prev, assistantMessage]);
        }
        catch (error) {
            console.error('Erro ao enviar mensagem:', error);
            const errorMessage = {
                id: (Date.now() + 1).toString(),
                text: 'Erro ao processar sua mensagem. Verifique se o agente está rodando.',
                sender: 'assistant',
                timestamp: new Date(),
                type: 'error'
            };
            setMessages(prev => [...prev, errorMessage]);
        }
        finally {
            setIsLoading(false);
        }
    };
    const handleQuickAction = (action) => {
        let command = '';
        switch (action) {
            case '📝 Criar nota':
                command = 'criar nota';
                break;
            case '🔍 Buscar':
                command = 'buscar';
                break;
            case '📊 Status':
                command = 'status';
                break;
            case '❓ Ajuda':
                command = 'ajuda';
                break;
            default:
                command = action;
        }
        setInputText(command);
    };
    const formatTime = (date) => {
        return date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
    };
    return (_jsxs("div", { className: "app-container", children: [_jsxs("aside", { className: "sidebar", children: [_jsx("div", { className: "sidebar-header", children: _jsxs("div", { className: "logo", children: [_jsx("span", { className: "logo-icon", children: "OA" }), _jsxs("div", { className: "logo-text", children: [_jsx("span", { className: "logo-title", children: "Obsidian" }), _jsx("span", { className: "logo-subtitle", children: "AGENTE v2.0" })] })] }) }), _jsxs("nav", { className: "sidebar-nav", children: [_jsxs("div", { className: 'nav-item' + (activeNav === 'chat' ? ' active' : ''), onClick: () => setActiveNav('chat'), children: [_jsx("span", { className: "icon", children: "\uD83D\uDCAC" }), _jsx("span", { className: "label", children: "Chat" })] }), _jsxs("div", { className: 'nav-item' + (activeNav === 'status' ? ' active' : ''), onClick: () => setActiveNav('status'), children: [_jsx("span", { className: "icon", children: "\uD83D\uDCCA" }), _jsx("span", { className: "label", children: "Status" }), _jsx("span", { className: 'status-badge ' + (isConnected ? 'online' : 'offline'), children: isConnected ? 'Online' : 'Offline' })] }), _jsxs("div", { className: 'nav-item' + (activeNav === 'config' ? ' active' : ''), onClick: () => setActiveNav('config'), children: [_jsx("span", { className: "icon", children: "\u2699\uFE0F" }), _jsx("span", { className: "label", children: "Configura\u00E7\u00F5es" })] }), _jsxs("div", { className: 'nav-item' + (activeNav === 'help' ? ' active' : ''), onClick: () => setActiveNav('help'), children: [_jsx("span", { className: "icon", children: "\u2753" }), _jsx("span", { className: "label", children: "Ajuda" })] })] }), _jsxs("div", { className: "sidebar-footer", children: [_jsxs("div", { className: "security-badge", children: [_jsx("span", { className: "icon", children: "\uD83D\uDD12" }), _jsxs("span", { className: "text", children: [_jsx("strong", { children: "Seguro" }), "Conex\u00E3o criptografada SHA-256"] })] }), _jsxs("button", { className: "disconnect-btn", children: [_jsx("span", { children: "\uD83D\uDD0C" }), "Desconectar"] })] })] }), _jsxs("main", { className: "main-content", children: [_jsxs("header", { className: "main-header", children: [_jsxs("div", { className: "header-status", children: [_jsx("span", { className: 'status-dot ' + (isConnected ? 'online' : 'offline') }), _jsx("span", { children: "Sistema Online" })] }), _jsx("span", { className: "header-version", children: "v2.0.0" })] }), _jsxs("div", { className: "chat-container", children: [_jsxs("div", { className: "messages-area", ref: messagesAreaRef, children: [messages.map((message) => (_jsxs("div", { className: 'message ' + message.sender, children: [_jsx("div", { className: "message-avatar", children: message.sender === 'user' ? '👤' : '🤖' }), _jsxs("div", { className: "message-bubble", children: [message.text.split('\n').map((line, i) => (_jsx("p", { children: line }, i))), _jsx("div", { className: "message-time", children: formatTime(message.timestamp) })] })] }, message.id))), isLoading && (_jsxs("div", { className: "message assistant", children: [_jsx("div", { className: "message-avatar", children: "\uD83E\uDD16" }), _jsx("div", { className: "message-bubble", children: _jsxs("div", { className: "typing-indicator", children: [_jsx("span", {}), _jsx("span", {}), _jsx("span", {})] }) })] })), _jsx("div", { ref: messagesEndRef })] }), _jsxs("div", { className: "input-area", children: [_jsx("div", { className: "quick-actions", children: quickActions.map((action, index) => (_jsx("button", { className: "quick-action-btn", onClick: () => handleQuickAction(action), children: action }, index))) }), _jsxs("div", { className: "input-container", children: [_jsx("div", { className: "input-wrapper", children: _jsx("textarea", { value: inputText, onChange: (e) => setInputText(e.target.value), onKeyPress: (e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage(), placeholder: "Digite um comando ou pergunta...", className: "message-input", rows: 1, disabled: !isConnected || isLoading }) }), _jsx("button", { onClick: handleSendMessage, disabled: !inputText.trim() || !isConnected || isLoading, className: "send-button", children: "\u27A4" })] }), _jsxs("div", { className: "input-footer", children: [_jsx("span", { children: "\uD83D\uDCCB Comandos dispon\u00EDveis" }), _jsxs("span", { className: "made-with", children: ["Made with ", _jsx("a", { href: "https://manus.im", target: "_blank", rel: "noopener noreferrer", children: "Manus" })] })] })] })] })] })] }));
}
export default App;
