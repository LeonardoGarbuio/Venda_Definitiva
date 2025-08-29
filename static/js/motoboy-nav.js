// Motoboy Navigation Management
        // Check device status
        function checkDeviceStatus() {
            console.log('🚀 === INICIANDO CHECK_DEVICE_STATUS ===');
            
            // Verifica se já existe um device_id salvo
            let deviceId = localStorage.getItem('device_id');
            
            console.log('🔍 DEBUG FRONTEND:');
            console.log('🔍 Device ID no localStorage:', deviceId);
            console.log('🔍 Tipo do deviceId:', typeof deviceId);
            console.log('🔍 Todas as chaves do localStorage:', Object.keys(localStorage));
            console.log('🔍 Conteúdo completo do localStorage:');
            
            // Log de todas as chaves do localStorage
            Object.keys(localStorage).forEach(key => {
                console.log(`  ${key}:`, localStorage.getItem(key));
            });
            
            // IMPORTANTE: Se não tem device_id no localStorage, mas tem no banco,
            // precisamos descobrir qual é o device_id correto para este dispositivo
            if (!deviceId) {
                console.log('🆕 NENHUM DEVICE_ID NO LOCALSTORAGE');
                console.log('🆕 Enviando requisição SEM device_id para o backend descobrir');
                // Se não tem device_id, envia requisição sem parâmetro
                deviceId = null;
            } else {
                console.log('✅ DEVICE_ID JÁ EXISTIA NO LOCALSTORAGE:', deviceId);
                console.log('✅ Tipo:', typeof deviceId);
                console.log('✅ Tamanho:', deviceId.length);
                console.log('✅ Enviando este device_id para o backend verificar');
            }
            
            console.log('📤 ENVIANDO DEVICE_ID PARA O SERVIDOR:', deviceId);
            
            // Envia o device_id para o servidor
            const url = deviceId ? `/motoboys/check-device/?device_id=${deviceId}` : '/motoboys/check-device/';
            console.log('📤 URL da requisição:', url);
            
            fetch(url)
                .then(response => {
                    console.log('📥 RESPOSTA RECEBIDA:');
                    console.log('📥 Status:', response.status);
                    console.log('📥 OK:', response.ok);
                    console.log('📥 Headers:', response.headers);
                    return response.json();
                })
                .then(data => {
                    console.log('📥 DADOS DA RESPOSTA:');
                    console.log('📥 Resposta completa:', data);
                    console.log('📥 Tipo da resposta:', typeof data);
                    console.log('📥 Chaves da resposta:', Object.keys(data));
                    
                    // Log de cada campo da resposta
                    Object.keys(data).forEach(key => {
                        console.log(`  ${key}:`, data[key], `(tipo: ${typeof data[key]})`);
                    });
                    
                    // SEMPRE usa o device_id que o backend retorna
                    if (data.device_id) {
                        console.log('🔄 DEVICE_ID RECEBIDO DO BACKEND:', data.device_id);
                        console.log('🔄 Atualizando localStorage...');
                        localStorage.setItem('device_id', data.device_id);
                        deviceId = data.device_id;
                        console.log('🔄 localStorage atualizado com:', deviceId);
                    } else {
                        console.log('⚠️ BACKEND NÃO RETORNOU DEVICE_ID');
                    }
                    
                    console.log('📋 RESUMO FINAL:');
                    console.log('📋 is_new_device:', data.is_new_device);
                    console.log('📋 show_register:', data.show_register);
                    console.log('📋 show_login:', data.show_login);
                    console.log('📋 device_id final:', deviceId);
                    
                    // Atualiza a navegação
                    console.log('🔄 CHAMANDO UPDATE_MOTOBOY_NAVIGATION...');
                    updateMotoboyNavigation(data);
                    console.log('✅ UPDATE_MOTOBOY_NAVIGATION CONCLUÍDO');
                })
                .catch(error => {
                    console.error('❌ ERRO AO VERIFICAR STATUS DO DISPOSITIVO:');
                    console.error('❌ Erro completo:', error);
                    console.error('❌ Mensagem:', error.message);
                    console.error('❌ Stack:', error.stack);
                });
                
            console.log('🚀 === FIM CHECK_DEVICE_STATUS ===');
        }

        // Generate device ID
        function generateDeviceId() {
            // Simula a mesma lógica do backend
            const userAgent = navigator.userAgent;
            const language = navigator.language;
            const encoding = 'gzip, deflate, br'; // Simula HTTP_ACCEPT_ENCODING
            const host = window.location.host;
            const referer = document.referrer || '';
            
            // Simula IP (usando uma string fixa para desenvolvimento)
            const ip = '127.0.0.1'; // IP local para desenvolvimento
            
            // Cria a mesma string que o backend usa
            const deviceString = `${ip}|${userAgent}|${language}|${encoding}|${host}|${referer}`;
            
            console.log('🔍 Gerando device_id com string:', deviceString);
            
            // Gera um hash simples que simule o SHA256 do backend
            let hash = 0;
            for (let i = 0; i < deviceString.length; i++) {
                const char = deviceString.charCodeAt(i);
                hash = ((hash << 5) - hash) + char;
                hash = hash & hash; // Converte para 32-bit integer
            }
            
            // Usa um seed fixo para garantir consistência
            const seed = 12345;
            hash = hash ^ seed;
            
            const deviceId = Math.abs(hash).toString(16).substring(0, 16);
            console.log('🔍 Device ID gerado:', deviceId);
            
            return deviceId;
        }

        // Update motoboy navigation
        function updateMotoboyNavigation(data) {
            console.log('🚀 === INICIANDO UPDATE_MOTOBOY_NAVIGATION ===');
            console.log('📥 DADOS RECEBIDOS:', data);
            console.log('📥 Tipo dos dados:', typeof data);
            
            if (!data) {
                console.log('❌ DADOS NULOS OU UNDEFINED!');
                console.log('🚀 === FIM UPDATE_MOTOBOY_NAVIGATION (ERRO) ===');
                return;
            }
            
            console.log('🔍 VERIFICANDO CAMPOS DOS DADOS:');
            console.log('  is_new_device:', data.is_new_device, `(tipo: ${typeof data.is_new_device})`);
            console.log('  show_register:', data.show_register, `(tipo: ${typeof data.show_register})`);
            console.log('  show_login:', data.show_login, `(tipo: ${typeof data.show_login})`);
            console.log('  device_id:', data.device_id, `(tipo: ${typeof data.device_id})`);
            
            // Busca os elementos da navegação (IDs corretos do template)
            const desktopNav = document.getElementById('motoboyNav');
            const mobileNav = document.getElementById('motoboyMobileNav');
            
            console.log('🔍 ELEMENTOS ENCONTRADOS:');
            console.log('  motoboyNav (desktop):', desktopNav);
            console.log('  motoboyMobileNav (mobile):', mobileNav);
            
            if (!desktopNav || !mobileNav) {
                console.log('❌ ELEMENTOS DE NAVEGAÇÃO NÃO ENCONTRADOS!');
                console.log('❌ Verifique se os IDs estão corretos no HTML');
                console.log('🚀 === FIM UPDATE_MOTOBOY_NAVIGATION (ERRO) ===');
                return;
            }
            
            console.log('✅ ELEMENTOS ENCONTRADOS, ATUALIZANDO NAVEGAÇÃO...');
            
            // Cria o HTML da navegação baseado nos dados
            let desktopHtml = '';
            let mobileHtml = '';
            
            // Sempre incluir o link do Cardápio primeiro
            desktopHtml += `
                <a href="/" class="text-text-secondary hover:text-primary transition-colors duration-200">
                    <i class="fas fa-utensils mr-1"></i>Cardápio
                </a>
            `;
            mobileHtml += `
                <a href="/" class="flex items-center text-text-secondary hover:text-primary transition-colors duration-200">
                    <i class="fas fa-utensils mr-3"></i>Cardápio
                </a>
            `;
            
            // Adicionar links de motoboy baseado no status
            if (data.show_login) {
                console.log('🔑 MOSTRANDO LINK DE LOGIN');
                desktopHtml += `
                    <a href="/motoboys/login/" class="text-text-secondary hover:text-primary transition-colors duration-200">
                        <i class="fas fa-sign-in-alt mr-1"></i>Login Motoboy
                    </a>
                `;
                mobileHtml += `
                    <a href="/motoboys/login/" class="flex items-center text-text-secondary hover:text-primary transition-colors duration-200">
                        <i class="fas fa-sign-in-alt mr-3"></i>Login Motoboy
                    </a>
                `;
            }
            
            if (data.show_register) {
                console.log('📝 MOSTRANDO LINK DE CADASTRO');
                desktopHtml += `
                    <a href="/motoboys/register/" class="text-text-secondary hover:text-primary transition-colors duration-200">
                        <i class="fas fa-user-plus mr-1"></i>Cadastro Motoboy
                    </a>
                `;
                mobileHtml += `
                    <a href="/motoboys/register/" class="flex items-center text-text-secondary hover:text-primary transition-colors duration-200">
                        <i class="fas fa-user-plus mr-3"></i>Cadastro Motoboy
                    </a>
                `;
            }
            
            // Sempre incluir o link do Admin por último
            desktopHtml += `
                <a href="/login/" class="text-text-secondary hover:text-primary transition-colors duration-200">
                    <i class="fas fa-shield-alt mr-1"></i>Admin
                </a>
            `;
            mobileHtml += `
                <a href="/login/" class="flex items-center text-text-secondary hover:text-primary transition-colors duration-200">
                    <i class="fas fa-shield-alt mr-3"></i>Admin
                </a>
            `;
            
            console.log('🔍 HTML GERADO:');
            console.log('  Desktop HTML:', desktopHtml);
            console.log('  Mobile HTML:', mobileHtml);
            
            // Atualiza o HTML da navegação
            if (desktopNav) {
                desktopNav.innerHTML = desktopHtml;
                console.log('✅ Navegação desktop atualizada');
                console.log('🔍 Estado após atualização:');
                console.log('  innerHTML:', desktopNav.innerHTML);
                console.log('  children.length:', desktopNav.children.length);
                console.log('  display:', window.getComputedStyle(desktopNav).display);
                console.log('  visibility:', window.getComputedStyle(desktopNav).visibility);
            }
            if (mobileNav) {
                mobileNav.innerHTML = mobileHtml;
                console.log('✅ Navegação mobile atualizada');
                console.log('🔍 Estado após atualização:');
                console.log('  innerHTML:', mobileNav.innerHTML);
                console.log('  children.length:', mobileNav.children.length);
                console.log('  display:', window.getComputedStyle(mobileNav).display);
                console.log('  visibility:', window.getComputedStyle(mobileNav).visibility);
            }
            
            console.log('🔍 RESUMO DA ATUALIZAÇÃO:');
            console.log('  show_register:', data.show_register);
            console.log('  show_login:', data.show_login);
            console.log('  HTML desktop gerado:', desktopHtml.length, 'caracteres');
            console.log('  HTML mobile gerado:', mobileHtml.length, 'caracteres');
            
            console.log('✅ NAVEGAÇÃO ATUALIZADA COM SUCESSO!');
            console.log('🚀 === FIM UPDATE_MOTOBOY_NAVIGATION ===');
        }

        // Initialize when DOM is ready
        document.addEventListener('DOMContentLoaded', function() {
            // NÃO limpa mais o device_id - deixa o sistema funcionar normalmente
            console.log('🚀 INICIANDO SISTEMA DE IDENTIFICAÇÃO DE MOTOBOY...');
            
            checkDeviceStatus();
        });
