#!/usr/bin/env pwsh

# Start Django Backend Server
Write-Host "🚀 Starting Django Backend Server..." -ForegroundColor Green
Write-Host "Backend URL: http://127.0.0.1:8000" -ForegroundColor Cyan

# Change to Django directory
Set-Location "c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend"

# Check if Django is properly configured
Write-Host "Checking Django configuration..." -ForegroundColor Yellow
python manage.py check

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Django configuration is valid" -ForegroundColor Green
    Write-Host "Starting Django development server..." -ForegroundColor Yellow
    python manage.py runserver 127.0.0.1:8000
} else {
    Write-Host "❌ Django configuration has errors" -ForegroundColor Red
    Write-Host "Please check the Django backend configuration" -ForegroundColor Red
}
