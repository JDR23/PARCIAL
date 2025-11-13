// API Helper con JWT y logging
const API_URL = window.location.origin;

// Almacenar token JWT
let authToken = localStorage.getItem('authToken') || null;

// Función para hacer peticiones con logging
async function apiRequest(url, options = {}) {
    const fullUrl = `${API_URL}${url}`;
    
    // Agregar token si existe
    if (authToken && !options.skipAuth) {
        options.headers = options.headers || {};
        options.headers['Authorization'] = `Bearer ${authToken}`;
    }
    
    // Logging en consola
    console.group(`🌐 ${options.method || 'GET'} ${url}`);
    console.log('URL:', fullUrl);
    console.log('Options:', options);
    
    const startTime = performance.now();
    
    try {
        const response = await fetch(fullUrl, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        
        const endTime = performance.now();
        const duration = (endTime - startTime).toFixed(2);
        
        let data;
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            data = await response.json();
        } else {
            data = await response.text();
        }
        
        console.log(`✅ Response (${duration}ms):`, {
            status: response.status,
            statusText: response.statusText,
            data: data
        });
        
        if (!response.ok) {
            console.error('❌ Error:', data);
            throw new Error(data.detail || `Error ${response.status}: ${response.statusText}`);
        }
        
        console.groupEnd();
        return { data, response };
    } catch (error) {
        const endTime = performance.now();
        const duration = (endTime - startTime).toFixed(2);
        console.error(`❌ Error (${duration}ms):`, error);
        console.groupEnd();
        throw error;
    }
}

// Funciones de autenticación
function setAuthToken(token) {
    authToken = token;
    localStorage.setItem('authToken', token);
}

function clearAuthToken() {
    authToken = null;
    localStorage.removeItem('authToken');
}

function getAuthToken() {
    return authToken;
}

// Exportar funciones
window.apiRequest = apiRequest;
window.setAuthToken = setAuthToken;
window.clearAuthToken = clearAuthToken;
window.getAuthToken = getAuthToken;

