"""
Enhanced Security Middleware for Django Research Agent
Implements additional security layers beyond Django defaults
"""
import logging
import time
from django.http import HttpResponseForbidden, JsonResponse
from django.core.cache import cache
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import ipaddress
import re

logger = logging.getLogger('security')

class EnhancedSecurityMiddleware(MiddlewareMixin):
    """
    Enhanced security middleware with rate limiting, IP filtering, and request validation
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.blocked_ips = set()
        self.rate_limit_cache = {}
        self.async_mode = False  # Required for Django compatibility
        
        # Security patterns to block
        self.malicious_patterns = [
            r'<script[^>]*>.*?</script>',  # XSS attempts
            r'javascript:',               # JavaScript injection
            r'on\w+\s*=',                # Event handlers
            r'union\s+select',           # SQL injection
            r'drop\s+table',             # SQL injection
            r'exec\s*\(',                # Code execution
            r'eval\s*\(',                # Code execution
            r'system\s*\(',              # System calls
        ]
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.malicious_patterns]
        
    def process_request(self, request):
        """Process incoming requests for security validation"""
        
        # Get client IP
        client_ip = self.get_client_ip(request)
        
        # 1. IP Blocking Check
        if self.is_ip_blocked(client_ip):
            logger.warning(f"Blocked request from blacklisted IP: {client_ip}")
            return HttpResponseForbidden("Access denied")
        
        # 2. Rate Limiting
        if self.is_rate_limited(client_ip, request):
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return JsonResponse({'error': 'Rate limit exceeded'}, status=429)
        
        # 3. Request Size Validation
        if self.is_request_too_large(request):
            logger.warning(f"Request too large from IP: {client_ip}")
            return HttpResponseForbidden("Request too large")
        
        # 4. Malicious Pattern Detection
        if self.contains_malicious_patterns(request):
            logger.warning(f"Malicious pattern detected from IP: {client_ip}")
            self.block_ip(client_ip)
            return HttpResponseForbidden("Malicious request detected")
        
        # 5. Header Validation
        if not self.validate_headers(request):
            logger.warning(f"Invalid headers from IP: {client_ip}")
            return HttpResponseForbidden("Invalid request headers")
        
        return None
    
    def process_response(self, request, response):
        """Add security headers to response"""
        
        # Add comprehensive security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Cross-Origin-Opener-Policy'] = 'same-origin'
        response['Cross-Origin-Embedder-Policy'] = 'require-corp'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Content Security Policy
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        response['Content-Security-Policy'] = csp
        
        # Remove server information
        if 'Server' in response:
            del response['Server']
        
        return response
    
    def get_client_ip(self, request):
        """Get real client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_ip_blocked(self, ip):
        """Check if IP is in blocklist"""
        return ip in self.blocked_ips
    
    def block_ip(self, ip):
        """Add IP to blocklist"""
        self.blocked_ips.add(ip)
        cache.set(f'blocked_ip_{ip}', True, 3600)  # Block for 1 hour
        logger.error(f"IP blocked for malicious activity: {ip}")
    
    def is_rate_limited(self, ip, request):
        """Check rate limiting per IP"""
        # Skip rate limiting for localhost in development
        if ip in ['127.0.0.1', 'localhost', '::1'] and getattr(settings, 'DEBUG', False):
            return False
            
        now = time.time()
        key = f'rate_limit_{ip}'
        
        # Get current request count
        requests = cache.get(key, [])
        
        # Remove old requests (older than 1 minute)
        requests = [req_time for req_time in requests if now - req_time < 60]
        
        # Check if limit exceeded
        limit = getattr(settings, 'API_RATE_LIMIT_PER_MINUTE', 60)
        if len(requests) >= limit:
            return True
        
        # Add current request
        requests.append(now)
        cache.set(key, requests, 60)
        
        return False
    
    def is_request_too_large(self, request):
        """Check if request size exceeds limit"""
        max_size = getattr(settings, 'MAX_REQUEST_SIZE', 10485760)  # 10MB default
        content_length = request.META.get('CONTENT_LENGTH')
        
        if content_length:
            try:
                if int(content_length) > max_size:
                    return True
            except ValueError:
                return True
        
        return False
    
    def contains_malicious_patterns(self, request):
        """Check for malicious patterns in request"""
        
        # Check GET parameters
        for key, value in request.GET.items():
            if self._check_string_for_patterns(value):
                return True
        
        # Check POST data
        try:
            if hasattr(request, 'body') and request.body:
                body_str = request.body.decode('utf-8', errors='ignore')
                if self._check_string_for_patterns(body_str):
                    return True
        except:
            pass
        
        # Check headers
        for header, value in request.META.items():
            if header.startswith('HTTP_') and self._check_string_for_patterns(str(value)):
                return True
        
        return False
    
    def _check_string_for_patterns(self, text):
        """Check string against malicious patterns"""
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                return True
        return False
    
    def validate_headers(self, request):
        """Validate request headers"""
        
        # Check for required headers in POST requests
        if request.method == 'POST':
            content_type = request.META.get('CONTENT_TYPE', '')
            if not content_type:
                return False
        
        # Check User-Agent header
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if not user_agent or len(user_agent) < 10:
            return False
        
        # Block known bad user agents (but allow python-requests for development)
        bad_agents = ['sqlmap', 'nikto', 'nmap', 'masscan']
        user_agent_lower = user_agent.lower()
        for bad_agent in bad_agents:
            if bad_agent in user_agent_lower:
                return False
        
        return True


class APIKeyAuthenticationMiddleware(MiddlewareMixin):
    """
    API Key authentication middleware for sensitive endpoints
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.async_mode = False  # Required for Django compatibility
        self.protected_paths = [
            '/api/research/',
            '/api/admin/',
            '/api/reports/',
        ]
    
    def process_request(self, request):
        """Check API key for protected endpoints"""
        
        # Skip authentication for non-protected paths
        if not any(request.path.startswith(path) for path in self.protected_paths):
            return None
        
        # Get API key from header
        api_key = request.META.get('HTTP_X_API_KEY')
        expected_key = getattr(settings, 'API_SECRET_KEY', '')
        
        if not api_key or not expected_key:
            logger.warning(f"Missing API key for protected endpoint: {request.path}")
            return JsonResponse({'error': 'API key required'}, status=401)
        
        if api_key != expected_key:
            logger.warning(f"Invalid API key for protected endpoint: {request.path}")
            return JsonResponse({'error': 'Invalid API key'}, status=401)
        
        return None


class SecurityEventLogger:
    """
    Security event logging utility
    """
    
    @staticmethod
    def log_security_event(event_type, details, request=None):
        """Log security events"""
        
        event_data = {
            'event_type': event_type,
            'details': details,
            'timestamp': time.time(),
        }
        
        if request:
            event_data.update({
                'ip_address': SecurityEventLogger.get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'path': request.path,
                'method': request.method,
            })
        
        logger.error(f"SECURITY_EVENT: {event_data}")
    
    @staticmethod
    def get_client_ip(request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
