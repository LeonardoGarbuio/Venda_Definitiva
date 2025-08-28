# 🚀 Sistema de Delivery - MotoDelivery

Sistema completo de delivery com área administrativa, cadastro de motoboys e interface para clientes fazerem pedidos.

## ✨ Funcionalidades

### 🏠 **Página Inicial (Menu)**
- Cardápio com categorias de produtos
- Carrinho de compras
- Navegação para cadastro de motoboy e área admin

### 👨‍💼 **Área Administrativa**
- Dashboard com estatísticas completas
- Gerenciamento de motoboys
- Controle de pedidos
- Relatórios e gráficos
- Estatísticas de performance

### 🛵 **Área do Motoboy**
- Cadastro completo com validações
- Dashboard com mapa e localização
- Lista de pedidos disponíveis
- Aceitar/recusar pedidos
- Atualizar status de entregas
- Perfil e configurações

### 👤 **Área do Cliente**
- Fazer pedidos diretamente
- Informações básicas para entrega
- Acompanhamento de pedidos
- Avaliação e feedback

## 🛠️ **Tecnologias**

- **Backend**: Django 5.2.5
- **Frontend**: HTML + CSS (Tailwind CSS)
- **Banco de Dados**: SQLite
- **Autenticação**: Sistema customizado do Django
- **APIs**: Django REST Framework

## 🚀 **Como Executar**

### 1. **Instalação**
```bash
# Clone o repositório
git clone <url-do-repositorio>
cd venda_definitiva

# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 2. **Configuração**
```bash
# Faça as migrações
python manage.py makemigrations
python manage.py migrate

# Crie um superusuário (opcional)
python manage.py createsuperuser
```

### 3. **Executar**
```bash
# Inicie o servidor
python manage.py runserver

# Acesse: http://127.0.0.1:8000/
```

## 📁 **Estrutura do Projeto**

```
venda_definitiva/
├── delivery_system/          # Configurações principais
├── core/                     # App principal e estatísticas
├── users/                    # Gerenciamento de usuários
├── motoboys/                 # Sistema de motoboys
├── orders/                   # Sistema de pedidos
├── templates/                # Templates HTML
│   ├── core/                 # Templates principais
│   ├── users/                # Templates de usuários
│   ├── motoboys/             # Templates de motoboys
│   └── orders/               # Templates de pedidos
├── static/                   # Arquivos estáticos
│   ├── css/                  # Estilos CSS
│   ├── js/                   # JavaScript
│   └── images/               # Imagens
└── manage.py                 # Script de gerenciamento Django
```

## 🔐 **Acessos**

### **Admin**
- URL: `/admin/`
- Usuário: Criar via `createsuperuser`
- Funcionalidades: Gerenciamento completo do sistema

### **Motoboy**
- URL: `/motoboys/register/`
- Funcionalidades: Cadastro e dashboard

### **Cliente**
- URL: `/` (página inicial)
- Funcionalidades: Fazer pedidos

## 📊 **Funcionalidades Administrativas**

### **Dashboard Principal**
- Estatísticas em tempo real
- Gráficos de performance
- Resumo de pedidos e motoboys

### **Gerenciamento de Motoboys**
- Cadastro com validações
- Controle de status (online/offline)
- Performance individual
- Relatórios mensais

### **Controle de Pedidos**
- Visualização de todos os pedidos
- Filtros por status e prioridade
- Atualização de status
- Cálculo automático de preços

### **Relatórios**
- Estatísticas diárias
- Performance dos motoboys
- Receita e satisfação do cliente
- Geração automática de relatórios

## 🗺️ **Fluxo do Sistema**

1. **Cliente acessa** a página inicial (menu)
2. **Faz pedido** com informações básicas
3. **Sistema calcula** preço e distância
4. **Motoboy disponível** aceita o pedido
5. **Acompanhamento** em tempo real
6. **Entrega** e avaliação
7. **Relatórios** automáticos para admin

## 🔧 **Configurações**

### **Variáveis de Ambiente**
- `DEBUG`: True (desenvolvimento)
- `SECRET_KEY`: Chave secreta do Django
- `DATABASE_URL`: Configuração do banco
- `ALLOWED_HOSTS`: Hosts permitidos

### **Banco de Dados**
- **Desenvolvimento**: SQLite
- **Produção**: PostgreSQL/MySQL recomendado

## 📱 **Responsividade**

- Design responsivo para mobile
- Interface otimizada para motoboys
- Dashboard administrativo adaptável

## 🚀 **Deploy**

### **Recomendações para Produção**
- Usar PostgreSQL ou MySQL
- Configurar HTTPS
- Usar servidor WSGI (Gunicorn)
- Configurar CDN para arquivos estáticos
- Implementar backup automático

## 📞 **Suporte**

Para dúvidas ou problemas:
- Verificar logs do Django
- Consultar documentação oficial
- Verificar configurações do banco

## 📄 **Licença**

Este projeto é desenvolvido para fins educacionais e comerciais.

---

**MotoDelivery** - Sistema completo de delivery desenvolvido com Django 🚀
