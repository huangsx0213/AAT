net share vix=c:\vix
Add-PSSnapin Microsoft.Exchange.Management.PowerShell.E2010
New-MailboxImportRequest -Mailbox administrator -FilePath \\dc08\vix\TestMessagePST.pst