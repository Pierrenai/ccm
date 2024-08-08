# CCM (Certificat Conformité Matière)

## Description

L'application **CCM** est une interface graphique développée en Python, permettant la gestion des certificats de conformité des matières (CCM). Elle permet d'ajouter, de supprimer et d'afficher les informations liées aux certificats, ainsi que de gérer les fournisseurs associés. Les données sont stockées dans une base de données SQLite.

## Fonctionnalités

- **Affichage des CCM** : Affiche tous les certificats de conformité de la base de données.
- **Ajout de CCM** : Ajout d'un nouveau certificat avec le numéro de commande et le fournisseur associé.
- **Suppression de CCM** : Suppression d'un certificat existant en fonction du numéro de commande.
- **Gestion des fournisseurs** : Ajout et suppression des fournisseurs dans la base de données.
- **Ouverture de fichiers associés** : Création et ouverture de répertoires liés aux certificats en fonction du fournisseur et du numéro de commande.

## Installation

1. Téléchargez les fichiers CCM.exe et ccm.db dans [Software](https://github.com/Pierrenai/ccm/tree/main/Software)
2. Lancer CCM.exe

Si vous souhaitez créer vous-même le fichier `.exe`, vous pouvez utiliser la commande Docker suivante :
### Windows :
   ```bash
   docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows
   ```

### Linux :
   ```bash
   docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux
   ```

Source :
https://github.com/cdrx/docker-pyinstaller
