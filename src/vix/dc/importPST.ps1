net share vix=c:\vix
Start-Sleep -s 300
Add-PSSnapin Microsoft.Exchange.Management.PowerShell.E2010
New-MailboxImportRequest -Mailbox administrator -FilePath \\dc08\vix\TestMessagePST.pst