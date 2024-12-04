
:: Pour la sauvegarde incrémentielle
@echo off
setlocal

:: Définir les variables sans guillemets autour du chemin
set MYSQL_PATH=C:\Program Files\MySQL\MySQL Server 8.0\bin
set BACKUP_PATH=C:\backups
set BIN_LOG_PATH=C:\ProgramData\MySQL\MySQL Server 8.0\data
set LAST_BACKUP_LOG=C:\backups\last_backup_position.txt

:: Vérifier si le fichier de position existe, sinon le créer avec une valeur par défaut
if not exist "%LAST_BACKUP_LOG%" echo 4 > "%LAST_BACKUP_LOG%"

:: Lire la dernière position du journal binaire
set /p LAST_LOG=<%LAST_BACKUP_LOG%

:: Afficher la position actuelle du journal binaire pour débogage
echo Dernière position lue: %LAST_LOG%

:: Vérifier si la position lue est valide
if "%LAST_LOG%"=="" (
    echo La position lue est vide, utilisation de la position de départ 4.
    set LAST_LOG=4
) else (
    echo La position lue est: %LAST_LOG%
)

:: Exécuter mysqlbinlog pour récupérer les transactions après la dernière position
echo Sauvegarde incrémentielle en cours...
"%MYSQL_PATH%\mysqlbinlog" --start-position=%LAST_LOG% --stop-never "%BIN_LOG_PATH%\mysql-bin.000001" > "%BACKUP_PATH%\sauvegarde_incrementielle.sql"

:: Vérifier si la commande a produit des résultats
if exist "%BACKUP_PATH%\sauvegarde_incrementielle.sql" (
    echo Sauvegarde incrémentielle réussie.
) else (
    echo Aucune transaction enregistrée dans le journal binaire.
)

:: Extraire la nouvelle position du journal binaire
:: Nous utilisons findstr pour trouver la ligne contenant la position
set NEW_POSITION=

for /f "tokens=2 delims= " %%A in ('"%MYSQL_PATH%\mysqlbinlog" --start-position=%LAST_LOG% --stop-never "%BIN_LOG_PATH%\mysql-bin.000001" ^| findstr /i "Position"') do (
    set NEW_POSITION=%%A
)

:: Afficher la nouvelle position récupérée pour débogage
echo Nouvelle position extraite: %NEW_POSITION%

:: Vérifier si la nouvelle position est valide (numérique)
if "%NEW_POSITION%"=="" (
    echo Aucune nouvelle position trouvée, en utilisant la dernière position connue.
    set NEW_POSITION=%LAST_LOG%
) else (
    :: Vérifier si la nouvelle position est un nombre
    echo %NEW_POSITION% | findstr "^[0-9]*$" >nul
    if errorlevel 1 (
        echo La nouvelle position n'est pas un nombre valide, en utilisant la dernière position connue.
        set NEW_POSITION=%LAST_LOG%
    ) else (
        echo La nouvelle position est valide: %NEW_POSITION%
    )
)

:: Enregistrer la nouvelle position du journal binaire
echo %NEW_POSITION% > "%LAST_BACKUP_LOG%"

:: Message de confirmation
echo Sauvegarde incrémentielle terminée. Nouvelle position : %NEW_POSITION%

endlocal








