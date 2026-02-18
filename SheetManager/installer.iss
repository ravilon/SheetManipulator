; ============================================
; SheetManager - Instalador Profissional
; ============================================

#define MyAppName "SheetManager"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Developer - Rávilon Aguiar"
#define MyAppURL "https://github.com/ravilon/SheetManipulator"
#define MyAppExeName "SheetManager.exe"

[Setup]
; Identificador único (gere um novo GUID com: [guid]::NewGuid())
AppId={{A7B3C9D2-E4F1-4A5B-8C6D-9E2F1A3B4C5D}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Diretórios
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Ícones
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

; Saída
OutputDir=installer_output
OutputBaseFilename=SheetManager_Setup_v{#MyAppVersion}
Compression=lzma2/max
SolidCompression=yes

; Aparência
WizardStyle=modern
WizardImageFile=compiler:WizModernImage-IS.bmp
WizardSmallImageFile=compiler:WizModernSmallImage-IS.bmp

; Privilégios
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; Informações de versão
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=Ferramenta para dividir arquivos CSV grandes
VersionInfoCopyright=Copyright (C) 2026 {#MyAppPublisher}
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Atalhos adicionais:"

[Files]
; Todos os arquivos da pasta dist\SheetManager
Source: "dist\SheetManager\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; README
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Menu Iniciar
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Leia-me"; Filename: "{app}\README.md"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

; Área de Trabalho
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Opção de executar após instalação
Filename: "{app}\{#MyAppExeName}"; Description: "Executar {#MyAppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Limpar arquivos temporários criados pelo app
Type: filesandordirs; Name: "{app}\*.log"
Type: filesandordirs; Name: "{localappdata}\{#MyAppName}"