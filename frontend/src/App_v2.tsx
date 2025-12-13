import { useState, useEffect, useRef } from 'react';
import apiService from './services/api';
import { APP_CONFIG } from './config';
import './App.css';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
  command?: string;
  data?: any;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [apiKey, setApiKey] = useState(apiService.getApiKey() || '');
  const [showApiKeyInput, setShowApiKeyInput] = useState(!apiService.getApiKey());
  const [isLoading, setIsLoading] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

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
      addMessage(
        '🤖 Olá! Sou o Obsidian Agente Inteligente.\n\n' +
        'Tenho conhecimento profundo sobre Obsidian e posso ajudá-lo com:\n' +
        '• Gerenciamento de notas\n' +
        '• Explicações sobre recursos do Obsidian\n' +
        '• Automação de tarefas\n\n' +
        'Digite "ajuda" para ver todos os comandos ou comece a conversar naturalmente!',
        'assistant'
      );
    }
    
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Atualizar sugestões baseadas no texto digitado
    if (inputText.length > 0) {
      const filtered = commandSuggestions.filter(cmd =>
        cmd.toLowerCase().includes(inputText.toLowerCase())
      );
      setSuggestions(filtered.slice(0, 5));
    } else {
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

  const addMessage = (text: string, sender: 'user' | 'assistant', command?: string, data?: any) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      text,
      sender,
      timestamp: new Date(),
      command,
      data,
    };
    setMessages((prev) => [...prev, newMessage]);
  };

  const processIntelligentCommand = async (command: string) => {
    try {
      const result = await apiService.intelligentProcess(command);
      
      if (result.success) {
        addMessage(result.response, 'assistant', result.command, result.data);
      } else {
        addMessage(`❌ Erro: ${result.error}`, 'assistant');
      }
    } catch (error) {
      addMessage('❌ Erro ao processar comando. Verifique se o agente está rodando.', 'assistant');
    }
  };

  const handleSendMessage = async () => {
    if (!inputText.trim() || isLoading) return;

    const userMessage = inputText.trim();
    addMessage(userMessage, 'user');
    setInputText('');
    setIsLoading(true);
    setSuggestions([]);

    try {
      await processIntelligentCommand(userMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInputText(suggestion);
    setSuggestions([]);
  };

  const formatTimestamp = (date: Date) => {
    return date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
  };

  const renderMessageContent = (message: Message) => {
    // Renderizar listas de notas
    if (message.data && Array.isArray(message.data)) {
      return (
        <div>
          <p>{message.text}</p>
          <div className="notes-list">
            {message.data.slice(0, 10).map((note: any, index: number) => (
              <div key={index} className="note-item">
                📝 {note.name || note.title}
                {note.path && <span className="note-path"> ({note.path})</span>}
              </div>
            ))}
            {message.data.length > 10 && (
              <div className="note-item more">
                ... e mais {message.data.length - 10} notas
              </div>
            )}
          </div>
        </div>
      );
    }

    // Renderizar texto com formatação
    return message.text.split('\n').map((line, index) => (
      <p key={index}>{line}</p>
    ));
  };

  if (showApiKeyInput) {
    return (
      <div className="app">
        <div className="api-key-modal">
          <div className="api-key-content">
            <h2>🔐 Configuração da API Key</h2>
            <p>
              Para conectar ao Obsidian Agente, você precisa fornecer a API Key
              gerada pelo agente local.
            </p>
            <p className="info-text">
              A API Key é exibida no terminal quando você inicia o agente com o
              comando <code>.\INICIAR_AGENTE.ps1</code>
            </p>
            <input
              type="text"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Cole a API Key aqui"
              className="api-key-input"
              onKeyPress={(e) => e.key === 'Enter' && handleApiKeySubmit()}
              autoFocus
            />
            <button onClick={handleApiKeySubmit} className="api-key-button">
              Conectar
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-left">
          <h1>🧠 Obsidian Agente</h1>
          <p className="subtitle">Seu assistente inteligente para automação do Obsidian</p>
        </div>
        <div className="header-right">
          <div className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
            <span className="status-dot"></span>
            <span className="status-text">
              {isConnected ? 'Conectado' : 'Desconectado'}
            </span>
          </div>
          <button
            onClick={() => setShowApiKeyInput(true)}
            className="settings-button"
            title="Configurações"
          >
            ⚙️
          </button>
        </div>
      </header>

      <div className="chat-container">
        <div className="messages-container">
          {messages.map((message) => (
            <div key={message.id} className={`message ${message.sender}`}>
              <div className="message-content">
                {renderMessageContent(message)}
              </div>
              <div className="message-timestamp">
                {formatTimestamp(message.timestamp)}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="message assistant">
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-container">
          {suggestions.length > 0 && (
            <div className="suggestions">
              {suggestions.map((suggestion, index) => (
                <button
                  key={index}
                  className="suggestion-button"
                  onClick={() => handleSuggestionClick(suggestion)}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          )}
          <div className="input-wrapper">
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Digite um comando para o Obsidian..."
              className="message-input"
              rows={1}
              disabled={!isConnected || isLoading}
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputText.trim() || !isConnected || isLoading}
              className="send-button"
            >
              🚀
            </button>
          </div>
          <div className="input-footer">
            <span className="agent-info">
              Agent: Connected • Port: 5001
            </span>
            <span className="version-info">
              v2.0 - Intelligent Agent
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
