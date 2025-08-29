# 🚀 MotoDelivery - Sistema de Delivery

Sistema completo de delivery com cadastro de motoboys, pedidos e gestão administrativa.

## 🛠️ Tecnologias

- **Backend:** Django 5.2.5
- **Frontend:** HTML, CSS, JavaScript
- **Banco de Dados:** SQLite (desenvolvimento) / PostgreSQL (produção)
- **Deploy:** Render

## 🚀 Deploy no Render

### 1. Configuração Automática

O projeto já está configurado para deploy automático no Render:

1. **Fork/Clone** este repositório
2. **Conecte** ao Render
3. **Configure** as variáveis de ambiente:
   - `SECRET_KEY`: Gerada automaticamente
   - `DEBUG`: `false`
   - `ALLOWED_HOSTS`: `venda-definitiva.onrender.com`

### 2. Variáveis de Ambiente

```bash
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=false
ALLOWED_HOSTS=venda-definitiva.onrender.com
```

### 3. Comandos de Build

O Render executará automaticamente:
```bash
pip install -r requirements.txt
bash start.sh
```

## 📁 Estrutura do Projeto

```
├── core/                 # App principal (produtos, categorias)
├── users/               # Gestão de usuários
├── motoboys/            # Sistema de motoboys
├── orders/              # Sistema de pedidos
├── static/              # Arquivos estáticos
├── templates/           # Templates HTML
├── delivery_system/     # Configurações Django
├── requirements.txt     # Dependências Python
├── start.sh            # Script de inicialização
├── setup_render.py     # Setup automático
└── render.yaml         # Configuração Render
```

## 🔧 Funcionalidades

### 👥 Sistema de Motoboys
- ✅ Cadastro com device_id único
- ✅ Login/Logout
- ✅ Dashboard do motoboy
- ✅ Identificação automática de dispositivo

### 🛒 Sistema de Pedidos
- ✅ Carrinho de compras
- ✅ Checkout completo
- ✅ Cálculo de taxa de entrega
- ✅ Resumo do pedido

### 🏪 Gestão Administrativa
- ✅ Dashboard admin
- ✅ Gestão de produtos
- ✅ Gestão de pedidos
- ✅ Gestão de motoboys

## 🚀 Como Usar

1. **Acesse** a aplicação
2. **Navegue** pelo cardápio
3. **Adicione** itens ao carrinho
4. **Finalize** o pedido
5. **Cadastre-se** como motoboy (se necessário)
6. **Acesse** o painel administrativo

## 🔒 Segurança

- ✅ CSRF Protection
- ✅ CORS configurado
- ✅ WhiteNoise para arquivos estáticos
- ✅ Variáveis de ambiente seguras

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório.

---

**MotoDelivery** - Sistema completo de delivery! 🚀
