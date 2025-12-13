import { useState, useEffect } from 'react';
import apiService from './services/api';
import { APP_CONFIG } from './config';
import './App.css';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [apiKey, setApiKey] = useState(apiService.getApiKey() || '');
  const [showApiKeyInput, setShowApiKeyInput] = useState(!apiService.getApiKey());
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    checkConnection();
    const interval = setInterval(checkConnection, 30000);
    return () => clearInterval(interval);
  }, []);

  const checkConnection = async () => {
    const result = await apiService.health();
    setIsConnected(result.success);
  };

  const handleApiKeySubmit = () => {
    if (apiKey.trim()) {
      apiService.setApiKey(apiKey.trim());
      setShowApiKeyInput(false);
      checkConnection();
      addMessage('API Key configurada com sucesso!', 'assistant');
    }
  };

  const addMessage = (text: string, sender: 'user' | 'assistant') => {
    const newMessage: Message = {
      id: Date.now().toString(),
      text,
      sender,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, newMessage]);
  };

  const processCommand = async (command: string) => {
    const lowerCommand = command.toLowerCase();

    // Comando: Abrir Obsidian
    if (lowerCommand.includes('abrir') || lowerCommand.includes('open')) {
      const result = await apiService.openObsidian();
      if (result.success) {
        addMessage('Obsidian aberto com sucesso! ✅', 'assistant');
      } else {
        addMessage(`Erro ao abrir Obsidian: ${result.error}`, 'assistant');
      }
      return;
    }

    // Comando: Listar notas
    if (lowerCommand.includes('listar') || lowerCommand.includes('list')) {
      const result = await apiService.listNotes();
      if (result.success) {
        addMessage(`Encontrei ${result.data?.length || 0} notas no vault.`, 'assistant');
      } else {
        addMessage(`Erro ao listar notas: ${result.error}`, 'assistant');
      }
      return;
    }

    // Comando: Status
    if (lowerCommand.includes('status') || lowerCommand.includes('health')) {
      const result = await apiService.health();
      if (result.success) {
        addMessage('Agente está online e funcionando perfeitamente! ✅', 'assistant');
      } else {
        addMessage('Agente está offline. Verifique se está rodando.', 'assistant');
      }
      return;
    }

    // Comando genérico
    addMessage(
      'Entendi seu comando. Aqui estão os comandos disponíveis:\n\n' +
      '• "Abrir Obsidian" - Abre a aplicação\n' +
      '• "Listar notas" - Lista todas as notas\n' +
      '• "Status" - Verifica o status do agente\n\n' +
      'Digite um desses comandos para começar!',
      'assistant'
    );
  };

  const handleSendMessage = async () => {
    if (!inputText.trim() || isLoading) return;

    const userMessage = inputText.trim();
    addMessage(userMessage, 'user');
    setInputText('');
    setIsLoading(true);

    try {
      await processCommand(userMessage);
    } catch (error) {
      addMessage('Erro ao processar comando. Tente novamente.', 'assistant');
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

  if (showApiKeyInput) {
    return (
      <div className="app">
        <div className="api-key-modal">
          <div className="api-key-content">
            <h2>🔐 Configurar API Key</h2>
            <p>Para começar, insira a API Key do Obsidian Desktop Agent:</p>
            <input
              type="text"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="BO_..."
              className="api-key-input"
              onKeyPress={(e) => e.key === 'Enter' && handleApiKeySubmit()}
            />
            <button onClick={handleApiKeySubmit} className="api-key-button">
              Conectar
            </button>
            <div className="api-key-help">
              <p>💡 A API Key é exibida quando você inicia o agente:</p>
              <code>python agent.py</code>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>🧠 {APP_CONFIG.APP_NAME}</h1>
          <p>Seu assistente inteligente para automação do Obsidian</p>
        </div>
        <div className="header-status">
          <div className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
            {isConnected ? '🟢 Conectado' : '🔴 Desconectado'}
          </div>
          <button 
            onClick={() => setShowApiKeyInput(true)} 
            className="settings-button"
            title="Configurar API Key"
          >
            ⚙️
          </button>
        </div>
      </header>

      <main className="chat-container">
        <div className="messages-list">
          {messages.length === 0 && (
            <div className="welcome-message">
              <h2>👋 Olá! Sou seu assistente Obsidian.</h2>
              <p>Como posso ajudar você hoje?</p>
              <div className="suggestions">
                <button onClick={() => setInputText('Abrir Obsidian')}>
                  Abrir Obsidian
                </button>
                <button onClick={() => setInputText('Listar notas')}>
                  Listar notas
                </button>
                <button onClick={() => setInputText('Status')}>
                  Verificar status
                </button>
              </div>
            </div>
          )}

          {messages.map((message) => (
            <div key={message.id} className={`message ${message.sender}`}>
              <div className="message-content">
                <div className="message-text">{message.text}</div>
                <div className="message-time">
                  {message.timestamp.toLocaleTimeString('pt-BR', {
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
                </div>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="message assistant">
              <div className="message-content">
                <div className="message-text typing">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="input-container">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Digite um comando para o Obsidian..."
            className="message-input"
            disabled={isLoading || !isConnected}
          />
          <button
            onClick={handleSendMessage}
            disabled={isLoading || !isConnected || !inputText.trim()}
            className="send-button"
          >
            {isLoading ? '⏳' : '🚀'}
          </button>
        </div>
      </main>

      <footer className="app-footer">
        <p>v{APP_CONFIG.VERSION} - Desenvolvido para automação inteligente</p>
      </footer>
    </div>
  );
}

export default App;
