net share vix=c:\vix
Add-PSSnapin Microsoft.Exchange.Management.PowerShell.E2010
New-MailboxImportRequest -Mailbox administrator -FilePath \\dc12\vix\TestMessagePST.pst
Start-Sleep -s 300
net stop MSExchangeMailboxReplication
net start MSExchangeMailboxReplication