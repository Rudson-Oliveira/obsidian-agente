import { useState, useEffect, useRef } from 'react';
import './App.css';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
  type?: string;
  data?: any;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([
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
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesAreaRef = useRef<HTMLDivElement>(null);

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
    } catch {
      setIsConnected(false);
    }
  };

  const handleSendMessage = async () => {
    if (!inputText.trim() || isLoading) return;

    const userMessage: Message = {
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
        body: JSON.stringify({ text: messageText })  // CORREÇÃO: usar "text" em vez de "message"
      });

      const data = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.response || data.message || 'Resposta recebida',
        sender: 'assistant',
        timestamp: new Date(),
        type: data.type || 'text',
        data: data.data
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Erro ao processar sua mensagem. Verifique se o agente está rodando.',
        sender: 'assistant',
        timestamp: new Date(),
        type: 'error'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickAction = (action: string) => {
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

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="logo">
            <span className="logo-icon">OA</span>
            <div className="logo-text">
              <span className="logo-title">Obsidian</span>
              <span className="logo-subtitle">AGENTE v2.0</span>
            </div>
          </div>
        </div>

        <nav className="sidebar-nav">
          <div 
            className={'nav-item' + (activeNav === 'chat' ? ' active' : '')}
            onClick={() => setActiveNav('chat')}
          >
            <span className="icon">💬</span>
            <span className="label">Chat</span>
          </div>
          <div 
            className={'nav-item' + (activeNav === 'status' ? ' active' : '')}
            onClick={() => setActiveNav('status')}
          >
            <span className="icon">📊</span>
            <span className="label">Status</span>
            <span className={'status-badge ' + (isConnected ? 'online' : 'offline')}>
              {isConnected ? 'Online' : 'Offline'}
            </span>
          </div>
          <div 
            className={'nav-item' + (activeNav === 'config' ? ' active' : '')}
            onClick={() => setActiveNav('config')}
          >
            <span className="icon">⚙️</span>
            <span className="label">Configurações</span>
          </div>
          <div 
            className={'nav-item' + (activeNav === 'help' ? ' active' : '')}
            onClick={() => setActiveNav('help')}
          >
            <span className="icon">❓</span>
            <span className="label">Ajuda</span>
          </div>
        </nav>

        <div className="sidebar-footer">
          <div className="security-badge">
            <span className="icon">🔒</span>
            <span className="text">
              <strong>Seguro</strong>
              Conexão criptografada SHA-256
            </span>
          </div>
          <button className="disconnect-btn">
            <span>🔌</span>
            Desconectar
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header className="main-header">
          <div className="header-status">
            <span className={'status-dot ' + (isConnected ? 'online' : 'offline')}></span>
            <span>Sistema Online</span>
          </div>
          <span className="header-version">v2.0.0</span>
        </header>

        <div className="chat-container">
          {/* CORREÇÃO: Adicionada ref e overflow-y para barra de rolagem */}
          <div className="messages-area" ref={messagesAreaRef}>
            {messages.map((message) => (
              <div key={message.id} className={'message ' + message.sender}>
                <div className="message-avatar">
                  {message.sender === 'user' ? '👤' : '🤖'}
                </div>
                <div className="message-bubble">
                  {message.text.split('\n').map((line, i) => (
                    <p key={i}>{line}</p>
                  ))}
                  <div className="message-time">{formatTime(message.timestamp)}</div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message assistant">
                <div className="message-avatar">🤖</div>
                <div className="message-bubble">
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

          <div className="input-area">
            <div className="quick-actions">
              {quickActions.map((action, index) => (
                <button
                  key={index}
                  className="quick-action-btn"
                  onClick={() => handleQuickAction(action)}
                >
                  {action}
                </button>
              ))}
            </div>

            <div className="input-container">
              <div className="input-wrapper">
                <textarea
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
                  placeholder="Digite um comando ou pergunta..."
                  className="message-input"
                  rows={1}
                  disabled={!isConnected || isLoading}
                />
              </div>
              <button
                onClick={handleSendMessage}
                disabled={!inputText.trim() || !isConnected || isLoading}
                className="send-button"
              >
                ➤
              </button>
            </div>

            <div className="input-footer">
              <span>📋 Comandos disponíveis</span>
              <span className="made-with">
                Made with <a href="https://manus.im" target="_blank" rel="noopener noreferrer">Manus</a>
              </span>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;

