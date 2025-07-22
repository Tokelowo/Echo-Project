Write-Host "Starting React Development Server on Port 3001..." -ForegroundColor Green
Set-Location "c:\Users\t-tokelowo\OneDrive - Microsoft\Attachments\React"
Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Installing dependencies (if needed)..." -ForegroundColor Cyan
npm install
Write-Host ""
Write-Host "Starting development server..." -ForegroundColor Cyan
npm run dev
Write-Host ""
Write-Host "Server should now be running at http://localhost:3001" -ForegroundColor Green
Read-Host "Press Enter to exit"
