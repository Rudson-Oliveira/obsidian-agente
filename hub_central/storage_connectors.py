#!/usr/bin/env python3
"""
CONECTORES DE ARMAZENAMENTO
Suporte a múltiplos destinos: Obsidian, Google Drive, OneDrive, MySQL
Criado por Manus para Rudson Oliveira
"""

import os
import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List, Optional
import requests

logger = logging.getLogger('StorageConnectors')


class StorageConnector(ABC):
    """Interface base para conectores de armazenamento"""
    
    @abstractmethod
    def connect(self) -> bool:
        """Estabelece conexão com o serviço"""
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """Encerra conexão com o serviço"""
        pass
    
    @abstractmethod
    def save(self, data: Dict[str, Any], path: str = None) -> Dict[str, Any]:
        """Salva dados no serviço"""
        pass
    
    @abstractmethod
    def load(self, path: str) -> Dict[str, Any]:
        """Carrega dados do serviço"""
        pass
    
    @abstractmethod
    def delete(self, path: str) -> bool:
        """Remove dados do serviço"""
        pass
    
    @abstractmethod
    def list(self, path: str = None) -> List[str]:
        """Lista itens no serviço"""
        pass
    
    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Verifica saúde da conexão"""
        pass


class ObsidianConnector(StorageConnector):
    """
    Conector para Obsidian via Local REST API e COMET Bridge
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.api_url = self.config.get("api_url", "https://localhost:27124")
        self.bridge_url = self.config.get("bridge_url", "http://localhost:5000")
        self.api_key = self.config.get("api_key", "")
        self.connected = False
    
    def connect(self) -> bool:
        """Verifica conexão com Obsidian"""
        try:
            response = requests.get(
                f"{self.bridge_url}/health",
                timeout=5
            )
            self.connected = response.status_code == 200
            logger.info(f"[OBSIDIAN] Conexão: {'OK' if self.connected else 'FALHOU'}")
            return self.connected
        except Exception as e:
            logger.error(f"[OBSIDIAN] Erro de conexão: {e}")
            self.connected = False
            return False
    
    def disconnect(self) -> bool:
        """Obsidian não requer desconexão explícita"""
        self.connected = False
        return True
    
    def save(self, data: Dict[str, Any], path: str = None) -> Dict[str, Any]:
        """Salva nota no Obsidian"""
        if not path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = f"Hub Central/data_{timestamp}.md"
        
        # Preparar conteúdo
        if isinstance(data.get("content"), str):
            content = data["content"]
        else:
            content = f"# {data.get('title', 'Dados')}\n\n"
            content += f"**Criado em:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            content += "```json\n"
            content += json.dumps(data, indent=2, ensure_ascii=False, default=str)
            content += "\n```"
        
        try:
            response = requests.post(
                f"{self.bridge_url}/obsidian/vault/{path}",
                json={"content": content},
                timeout=10
            )
            
            return {
                "success": response.status_code in [200, 201],
                "path": path,
                "status_code": response.status_code
            }
        except Exception as e:
            logger.error(f"[OBSIDIAN] Erro ao salvar: {e}")
            return {"success": False, "error": str(e)}
    
    def load(self, path: str) -> Dict[str, Any]:
        """Carrega nota do Obsidian"""
        try:
            response = requests.get(
                f"{self.bridge_url}/obsidian/vault/{path}",
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "content": response.json().get("content", ""),
                    "path": path
                }
            else:
                return {"success": False, "error": f"Status {response.status_code}"}
        except Exception as e:
            logger.error(f"[OBSIDIAN] Erro ao carregar: {e}")
            return {"success": False, "error": str(e)}
    
    def delete(self, path: str) -> bool:
        """Remove nota do Obsidian"""
        try:
            response = requests.delete(
                f"{self.bridge_url}/obsidian/vault/{path}",
                timeout=10
            )
            return response.status_code in [200, 204]
        except Exception as e:
            logger.error(f"[OBSIDIAN] Erro ao deletar: {e}")
            return False
    
    def list(self, path: str = None) -> List[str]:
        """Lista arquivos no vault"""
        try:
            endpoint = f"{self.bridge_url}/obsidian/vault/"
            if path:
                endpoint += path
            
            response = requests.get(endpoint, timeout=10)
            
            if response.status_code == 200:
                return response.json().get("files", [])
            return []
        except Exception as e:
            logger.error(f"[OBSIDIAN] Erro ao listar: {e}")
            return []
    
    def health_check(self) -> Dict[str, Any]:
        """Verifica saúde da conexão"""
        try:
            start = datetime.now()
            response = requests.get(f"{self.bridge_url}/health", timeout=5)
            latency = (datetime.now() - start).total_seconds() * 1000
            
            return {
                "status": "online" if response.status_code == 200 else "offline",
                "latency_ms": latency,
                "api_url": self.api_url,
                "bridge_url": self.bridge_url
            }
        except Exception as e:
            return {"status": "offline", "error": str(e)}
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """Pesquisa no vault"""
        try:
            response = requests.post(
                f"{self.bridge_url}/obsidian/search",
                json={"query": query},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("results", [])
            return []
        except Exception as e:
            logger.error(f"[OBSIDIAN] Erro na pesquisa: {e}")
            return []


class GoogleDriveConnector(StorageConnector):
    """
    Conector para Google Drive
    Requer: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.credentials_path = self.config.get("credentials_path", "")
        self.token_path = self.config.get("token_path", os.path.expanduser("~/.hub_central/gdrive_token.json"))
        self.folder_id = self.config.get("folder_id", "")
        self.service = None
        self.connected = False
    
    def connect(self) -> bool:
        """Estabelece conexão com Google Drive"""
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            
            SCOPES = ['https://www.googleapis.com/auth/drive.file']
            
            creds = None
            
            # Carregar token existente
            if os.path.exists(self.token_path):
                creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
            
            # Renovar ou criar credenciais
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(self.credentials_path):
                        logger.error("[GDRIVE] Arquivo de credenciais não encontrado")
                        return False
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                
                # Salvar token
                os.makedirs(os.path.dirname(self.token_path), exist_ok=True)
                with open(self.token_path, 'w') as token:
                    token.write(creds.to_json())
            
            self.service = build('drive', 'v3', credentials=creds)
            self.connected = True
            logger.info("[GDRIVE] Conectado com sucesso")
            return True
            
        except ImportError:
            logger.error("[GDRIVE] Bibliotecas do Google não instaladas")
            logger.info("Execute: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
            return False
        except Exception as e:
            logger.error(f"[GDRIVE] Erro de conexão: {e}")
            return False
    
    def disconnect(self) -> bool:
        """Encerra conexão"""
        self.service = None
        self.connected = False
        return True
    
    def save(self, data: Dict[str, Any], path: str = None) -> Dict[str, Any]:
        """Salva arquivo no Google Drive"""
        if not self.connected or not self.service:
            return {"success": False, "error": "Não conectado"}
        
        try:
            from googleapiclient.http import MediaFileUpload
            import tempfile
            
            # Criar arquivo temporário
            filename = path or f"hub_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
                temp_path = f.name
            
            # Upload
            file_metadata = {
                'name': filename,
                'mimeType': 'application/json'
            }
            
            if self.folder_id:
                file_metadata['parents'] = [self.folder_id]
            
            media = MediaFileUpload(temp_path, mimetype='application/json')
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink'
            ).execute()
            
            # Limpar arquivo temporário
            os.unlink(temp_path)
            
            return {
                "success": True,
                "file_id": file.get('id'),
                "name": file.get('name'),
                "link": file.get('webViewLink')
            }
            
        except Exception as e:
            logger.error(f"[GDRIVE] Erro ao salvar: {e}")
            return {"success": False, "error": str(e)}
    
    def load(self, path: str) -> Dict[str, Any]:
        """Carrega arquivo do Google Drive"""
        if not self.connected or not self.service:
            return {"success": False, "error": "Não conectado"}
        
        try:
            # path pode ser file_id ou nome do arquivo
            file_id = path
            
            # Se não for um ID, buscar pelo nome
            if not path.startswith('1') or len(path) < 20:
                results = self.service.files().list(
                    q=f"name='{path}'",
                    fields="files(id, name)"
                ).execute()
                
                files = results.get('files', [])
                if not files:
                    return {"success": False, "error": "Arquivo não encontrado"}
                
                file_id = files[0]['id']
            
            # Download
            content = self.service.files().get_media(fileId=file_id).execute()
            
            return {
                "success": True,
                "content": json.loads(content.decode('utf-8')),
                "file_id": file_id
            }
            
        except Exception as e:
            logger.error(f"[GDRIVE] Erro ao carregar: {e}")
            return {"success": False, "error": str(e)}
    
    def delete(self, path: str) -> bool:
        """Remove arquivo do Google Drive"""
        if not self.connected or not self.service:
            return False
        
        try:
            self.service.files().delete(fileId=path).execute()
            return True
        except Exception as e:
            logger.error(f"[GDRIVE] Erro ao deletar: {e}")
            return False
    
    def list(self, path: str = None) -> List[str]:
        """Lista arquivos no Google Drive"""
        if not self.connected or not self.service:
            return []
        
        try:
            query = ""
            if self.folder_id:
                query = f"'{self.folder_id}' in parents"
            
            results = self.service.files().list(
                q=query,
                pageSize=100,
                fields="files(id, name, mimeType, modifiedTime)"
            ).execute()
            
            return results.get('files', [])
        except Exception as e:
            logger.error(f"[GDRIVE] Erro ao listar: {e}")
            return []
    
    def health_check(self) -> Dict[str, Any]:
        """Verifica saúde da conexão"""
        if not self.connected:
            return {"status": "disconnected"}
        
        try:
            about = self.service.about().get(fields="user").execute()
            return {
                "status": "online",
                "user": about.get('user', {}).get('emailAddress', 'unknown')
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}


class OneDriveConnector(StorageConnector):
    """
    Conector para OneDrive
    Requer: pip install msal requests
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.client_id = self.config.get("client_id", "")
        self.client_secret = self.config.get("client_secret", "")
        self.folder_path = self.config.get("folder_path", "/HubCentral")
        self.token_path = self.config.get("token_path", os.path.expanduser("~/.hub_central/onedrive_token.json"))
        self.access_token = None
        self.connected = False
    
    def connect(self) -> bool:
        """Estabelece conexão com OneDrive"""
        try:
            import msal
            
            # Configuração MSAL
            authority = "https://login.microsoftonline.com/common"
            scope = ["Files.ReadWrite.All"]
            
            # Criar aplicação
            app = msal.PublicClientApplication(
                self.client_id,
                authority=authority
            )
            
            # Tentar token em cache
            accounts = app.get_accounts()
            if accounts:
                result = app.acquire_token_silent(scope, account=accounts[0])
            else:
                # Fluxo interativo
                result = app.acquire_token_interactive(scopes=scope)
            
            if "access_token" in result:
                self.access_token = result["access_token"]
                self.connected = True
                logger.info("[ONEDRIVE] Conectado com sucesso")
                return True
            else:
                logger.error(f"[ONEDRIVE] Erro de autenticação: {result.get('error_description')}")
                return False
                
        except ImportError:
            logger.error("[ONEDRIVE] Biblioteca MSAL não instalada")
            logger.info("Execute: pip install msal")
            return False
        except Exception as e:
            logger.error(f"[ONEDRIVE] Erro de conexão: {e}")
            return False
    
    def disconnect(self) -> bool:
        """Encerra conexão"""
        self.access_token = None
        self.connected = False
        return True
    
    def _get_headers(self) -> Dict[str, str]:
        """Retorna headers de autenticação"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def save(self, data: Dict[str, Any], path: str = None) -> Dict[str, Any]:
        """Salva arquivo no OneDrive"""
        if not self.connected:
            return {"success": False, "error": "Não conectado"}
        
        try:
            filename = path or f"hub_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            full_path = f"{self.folder_path}/{filename}"
            
            content = json.dumps(data, indent=2, ensure_ascii=False, default=str)
            
            response = requests.put(
                f"https://graph.microsoft.com/v1.0/me/drive/root:{full_path}:/content",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json"
                },
                data=content.encode('utf-8'),
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                return {
                    "success": True,
                    "id": result.get("id"),
                    "name": result.get("name"),
                    "webUrl": result.get("webUrl")
                }
            else:
                return {"success": False, "error": response.text}
                
        except Exception as e:
            logger.error(f"[ONEDRIVE] Erro ao salvar: {e}")
            return {"success": False, "error": str(e)}
    
    def load(self, path: str) -> Dict[str, Any]:
        """Carrega arquivo do OneDrive"""
        if not self.connected:
            return {"success": False, "error": "Não conectado"}
        
        try:
            full_path = f"{self.folder_path}/{path}" if not path.startswith("/") else path
            
            response = requests.get(
                f"https://graph.microsoft.com/v1.0/me/drive/root:{full_path}:/content",
                headers=self._get_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "content": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                }
            else:
                return {"success": False, "error": response.text}
                
        except Exception as e:
            logger.error(f"[ONEDRIVE] Erro ao carregar: {e}")
            return {"success": False, "error": str(e)}
    
    def delete(self, path: str) -> bool:
        """Remove arquivo do OneDrive"""
        if not self.connected:
            return False
        
        try:
            full_path = f"{self.folder_path}/{path}" if not path.startswith("/") else path
            
            response = requests.delete(
                f"https://graph.microsoft.com/v1.0/me/drive/root:{full_path}",
                headers=self._get_headers(),
                timeout=30
            )
            
            return response.status_code == 204
        except Exception as e:
            logger.error(f"[ONEDRIVE] Erro ao deletar: {e}")
            return False
    
    def list(self, path: str = None) -> List[str]:
        """Lista arquivos no OneDrive"""
        if not self.connected:
            return []
        
        try:
            folder = path or self.folder_path
            
            response = requests.get(
                f"https://graph.microsoft.com/v1.0/me/drive/root:{folder}:/children",
                headers=self._get_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("value", [])
            return []
        except Exception as e:
            logger.error(f"[ONEDRIVE] Erro ao listar: {e}")
            return []
    
    def health_check(self) -> Dict[str, Any]:
        """Verifica saúde da conexão"""
        if not self.connected:
            return {"status": "disconnected"}
        
        try:
            response = requests.get(
                "https://graph.microsoft.com/v1.0/me",
                headers=self._get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                user = response.json()
                return {
                    "status": "online",
                    "user": user.get("userPrincipalName", "unknown")
                }
            return {"status": "error", "code": response.status_code}
        except Exception as e:
            return {"status": "error", "error": str(e)}


class MySQLConnector(StorageConnector):
    """
    Conector para MySQL/MariaDB
    Requer: pip install mysql-connector-python
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.host = self.config.get("host", "localhost")
        self.port = self.config.get("port", 3306)
        self.database = self.config.get("database", "hub_central")
        self.user = self.config.get("user", "root")
        self.password = self.config.get("password", "")
        self.connection = None
        self.connected = False
    
    def connect(self) -> bool:
        """Estabelece conexão com MySQL"""
        try:
            import mysql.connector
            
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            
            self.connected = self.connection.is_connected()
            
            if self.connected:
                # Criar tabelas se não existirem
                self._init_tables()
                logger.info("[MYSQL] Conectado com sucesso")
            
            return self.connected
            
        except ImportError:
            logger.error("[MYSQL] mysql-connector-python não instalado")
            logger.info("Execute: pip install mysql-connector-python")
            return False
        except Exception as e:
            logger.error(f"[MYSQL] Erro de conexão: {e}")
            return False
    
    def _init_tables(self):
        """Cria tabelas necessárias"""
        cursor = self.connection.cursor()
        
        # Tabela principal de dados
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hub_data (
                id VARCHAR(50) PRIMARY KEY,
                category VARCHAR(50),
                data JSON,
                metadata JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_category (category),
                INDEX idx_created (created_at)
            )
        """)
        
        # Tabela de eventos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hub_events (
                id VARCHAR(50) PRIMARY KEY,
                event_type VARCHAR(50),
                source VARCHAR(100),
                data JSON,
                processed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_type (event_type),
                INDEX idx_processed (processed)
            )
        """)
        
        # Tabela de logs de IA
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                provider VARCHAR(50),
                model VARCHAR(100),
                prompt TEXT,
                response TEXT,
                latency_ms INT,
                success BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_provider (provider),
                INDEX idx_created (created_at)
            )
        """)
        
        self.connection.commit()
        cursor.close()
    
    def disconnect(self) -> bool:
        """Encerra conexão"""
        if self.connection:
            self.connection.close()
        self.connected = False
        return True
    
    def save(self, data: Dict[str, Any], path: str = None) -> Dict[str, Any]:
        """Salva dados no MySQL"""
        if not self.connected:
            return {"success": False, "error": "Não conectado"}
        
        try:
            cursor = self.connection.cursor()
            
            data_id = path or f"data_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
            category = data.get("category", "general")
            metadata = data.get("metadata", {})
            
            # Remover campos especiais
            clean_data = {k: v for k, v in data.items() if k not in ["category", "metadata"]}
            
            cursor.execute("""
                INSERT INTO hub_data (id, category, data, metadata)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    data = VALUES(data),
                    metadata = VALUES(metadata)
            """, (
                data_id,
                category,
                json.dumps(clean_data, ensure_ascii=False, default=str),
                json.dumps(metadata, ensure_ascii=False, default=str)
            ))
            
            self.connection.commit()
            cursor.close()
            
            return {"success": True, "id": data_id}
            
        except Exception as e:
            logger.error(f"[MYSQL] Erro ao salvar: {e}")
            return {"success": False, "error": str(e)}
    
    def load(self, path: str) -> Dict[str, Any]:
        """Carrega dados do MySQL"""
        if not self.connected:
            return {"success": False, "error": "Não conectado"}
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM hub_data WHERE id = %s", (path,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return {
                    "success": True,
                    "id": row["id"],
                    "category": row["category"],
                    "data": json.loads(row["data"]) if row["data"] else {},
                    "metadata": json.loads(row["metadata"]) if row["metadata"] else {},
                    "created_at": row["created_at"].isoformat() if row["created_at"] else None
                }
            else:
                return {"success": False, "error": "Não encontrado"}
                
        except Exception as e:
            logger.error(f"[MYSQL] Erro ao carregar: {e}")
            return {"success": False, "error": str(e)}
    
    def delete(self, path: str) -> bool:
        """Remove dados do MySQL"""
        if not self.connected:
            return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM hub_data WHERE id = %s", (path,))
            self.connection.commit()
            affected = cursor.rowcount
            cursor.close()
            return affected > 0
        except Exception as e:
            logger.error(f"[MYSQL] Erro ao deletar: {e}")
            return False
    
    def list(self, path: str = None) -> List[str]:
        """Lista dados no MySQL"""
        if not self.connected:
            return []
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            if path:
                cursor.execute(
                    "SELECT id, category, created_at FROM hub_data WHERE category = %s ORDER BY created_at DESC",
                    (path,)
                )
            else:
                cursor.execute(
                    "SELECT id, category, created_at FROM hub_data ORDER BY created_at DESC LIMIT 100"
                )
            
            rows = cursor.fetchall()
            cursor.close()
            
            return rows
        except Exception as e:
            logger.error(f"[MYSQL] Erro ao listar: {e}")
            return []
    
    def health_check(self) -> Dict[str, Any]:
        """Verifica saúde da conexão"""
        if not self.connected:
            return {"status": "disconnected"}
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            
            return {
                "status": "online",
                "host": self.host,
                "database": self.database
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def query(self, sql: str, params: tuple = None) -> List[Dict]:
        """Executa query SQL customizada"""
        if not self.connected:
            return []
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(sql, params or ())
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            logger.error(f"[MYSQL] Erro na query: {e}")
            return []
    
    def log_ai_interaction(
        self,
        provider: str,
        model: str,
        prompt: str,
        response: str,
        latency_ms: int,
        success: bool
    ):
        """Registra interação com IA"""
        if not self.connected:
            return
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO ai_logs (provider, model, prompt, response, latency_ms, success)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (provider, model, prompt[:5000], response[:10000], latency_ms, success))
            self.connection.commit()
            cursor.close()
        except Exception as e:
            logger.error(f"[MYSQL] Erro ao registrar log: {e}")


# ==================== GERENCIADOR DE CONECTORES ====================

class StorageManager:
    """
    Gerenciador unificado de conectores de armazenamento
    """
    
    def __init__(self):
        self.connectors: Dict[str, StorageConnector] = {}
        self.default_connector = "obsidian"
    
    def register(self, name: str, connector: StorageConnector):
        """Registra um conector"""
        self.connectors[name] = connector
        logger.info(f"[STORAGE] Conector registrado: {name}")
    
    def get(self, name: str) -> Optional[StorageConnector]:
        """Obtém um conector pelo nome"""
        return self.connectors.get(name)
    
    def connect_all(self) -> Dict[str, bool]:
        """Conecta todos os conectores"""
        results = {}
        for name, connector in self.connectors.items():
            results[name] = connector.connect()
        return results
    
    def disconnect_all(self):
        """Desconecta todos os conectores"""
        for connector in self.connectors.values():
            connector.disconnect()
    
    def save_to_all(self, data: Dict[str, Any], path: str = None) -> Dict[str, Any]:
        """Salva em todos os conectores ativos"""
        results = {}
        for name, connector in self.connectors.items():
            if connector.connected:
                results[name] = connector.save(data, path)
        return results
    
    def health_check_all(self) -> Dict[str, Any]:
        """Verifica saúde de todos os conectores"""
        results = {}
        for name, connector in self.connectors.items():
            results[name] = connector.health_check()
        return results


# ==================== INSTÂNCIA GLOBAL ====================

storage_manager = StorageManager()

# Registrar conectores padrão
storage_manager.register("obsidian", ObsidianConnector())
storage_manager.register("google_drive", GoogleDriveConnector())
storage_manager.register("onedrive", OneDriveConnector())
storage_manager.register("mysql", MySQLConnector())


# ==================== TESTE ====================

if __name__ == "__main__":
    print("=" * 50)
    print("  CONECTORES DE ARMAZENAMENTO - Teste")
    print("=" * 50)
    
    # Testar Obsidian
    print("\n[OBSIDIAN]")
    obsidian = storage_manager.get("obsidian")
    if obsidian.connect():
        print("  Conexão: OK")
        print(f"  Health: {obsidian.health_check()}")
    else:
        print("  Conexão: FALHOU")
    
    # Status geral
    print("\n[STATUS GERAL]")
    print(json.dumps(storage_manager.health_check_all(), indent=2))
