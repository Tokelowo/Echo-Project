# PowerShell script to start Django backend and fix "Failed to fetch" errors
Write-Host "🚀 Starting Django Backend Server..." -ForegroundColor Green
Write-Host "This will fix all 'Failed to fetch' console errors" -ForegroundColor Yellow

# Navigate to Django backend directory
$djangoPath = "c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend"

if (Test-Path $djangoPath) {
    Write-Host "✅ Found Django backend directory" -ForegroundColor Green
    Set-Location $djangoPath
    
    # Check if manage.py exists
    if (Test-Path "manage.py") {
        Write-Host "✅ Found manage.py - Django project detected" -ForegroundColor Green
        
        # Check Python installation
        try {
            $pythonVersion = python --version 2>&1
            Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
        } catch {
            Write-Host "❌ Python not found. Please install Python first." -ForegroundColor Red
            Read-Host "Press Enter to exit"
            exit 1
        }
        
        # Install requirements if needed
        if (Test-Path "requirements_reviews.txt") {
            Write-Host "📦 Installing Python dependencies..." -ForegroundColor Cyan
            python -m pip install -r requirements_reviews.txt
        }
        
        # Run migrations
        Write-Host "🔄 Running database migrations..." -ForegroundColor Cyan
        python manage.py migrate
        
        # Start Django server
        Write-Host "" -ForegroundColor White
        Write-Host "🌟 STARTING DJANGO SERVER ON 127.0.0.1:8000" -ForegroundColor Green
        Write-Host "🌟 This will fix all 'Failed to fetch' errors in your React app!" -ForegroundColor Green
        Write-Host "🌟 Keep this window open while using the app" -ForegroundColor Yellow
        Write-Host "" -ForegroundColor White
        
        python manage.py runserver 127.0.0.1:8000
        
    } else {
        Write-Host "❌ manage.py not found in Django directory" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Django backend directory not found: $djangoPath" -ForegroundColor Red
}

Read-Host "Press Enter to exit"
