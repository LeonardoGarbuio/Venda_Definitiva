// Motoboy Navigation Management
function checkDeviceStatus() {
    // 1. Gera um ID único da máquina localmente também
    const localDeviceId = generateLocalDeviceId();
    
    // 2. Verifica se já temos um device_id salvo
    const savedDeviceId = localStorage.getItem('moto_device_id');
    
    // 3. Se não temos, salva o novo
    if (!savedDeviceId) {
        localStorage.setItem('moto_device_id', localDeviceId);
    }
    
    // 4. Faz a requisição para o servidor
    fetch('/motoboys/check-device/')
        .then(response => response.json())
        .then(data => {
            console.log('Device status response:', data);
            
            // 5. Salva o device_id retornado pelo servidor
            if (data.device_id) {
                localStorage.setItem('moto_device_id', data.device_id);
                console.log('Device ID salvo:', data.device_id);
            }
            
            updateMotoboyNavigation(data);
        })
        .catch(error => {
            console.error('Error checking device status:', error);
            // Fallback: mostrar ambos os links
            updateMotoboyNavigation({
                show_register: true,
                show_login: true
            });
        });
}

// Gera um ID único da máquina baseado em características do navegador
function generateLocalDeviceId() {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    ctx.textBaseline = 'top';
    ctx.font = '14px Arial';
    ctx.fillText('MotoDelivery Device ID', 2, 2);
    
    const canvasFingerprint = canvas.toDataURL();
    
    // Combina múltiplos fatores para criar um ID único
    const factors = [
        navigator.userAgent,
        navigator.language,
        navigator.platform,
        screen.width + 'x' + screen.height,
        new Date().getTimezoneOffset(),
        canvasFingerprint,
        navigator.hardwareConcurrency || 'unknown',
        navigator.deviceMemory || 'unknown'
    ].join('|');
    
    // Cria um hash simples
    let hash = 0;
    for (let i = 0; i < factors.length; i++) {
        const char = factors.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Converte para 32-bit integer
    }
    
    return Math.abs(hash).toString(36);
}

// Update motoboy navigation based on device status
function updateMotoboyNavigation(data) {
    const desktopNav = document.getElementById('motoboyNav');
    const mobileNav = document.getElementById('motoboyMobileNav');
    
    console.log('Updating navigation with data:', data);
    
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
        console.log('Mostrando link de LOGIN');
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
        console.log('Mostrando link de CADASTRO');
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
    
    if (desktopNav) desktopNav.innerHTML = desktopHtml;
    if (mobileNav) mobileNav.innerHTML = mobileHtml;
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    checkDeviceStatus();
});
