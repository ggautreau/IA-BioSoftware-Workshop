# Guide de contribution

Merci de l'intérêt que vous portez à ce projet !

> Le code du projet se trouve dans le dossier [`tp_python/`](../tp_python).

## Signaler un bug

Avant d'ouvrir une issue, vérifiez qu'elle n'existe pas déjà.
Utilisez le template "Bug report" et renseignez :
- La version utilisée
- Les étapes pour reproduire le problème
- Le comportement attendu vs observé

## Proposer une fonctionnalité

Ouvrez une issue avec le template "Feature request" en décrivant
le besoin et le comportement souhaité.

## Soumettre une Pull Request

1. Forkez le dépôt
2. Créez une branche depuis `main` : `git checkout -b feat/ma-fonctionnalite`
3. Faites vos modifications
4. Vérifiez que tous les checks passent : `cd tp_python && pixi run all-checks`
5. Committez avec un message clair (voir Convention de commit ci-dessous)
6. Ouvrez une Pull Request vers `main`

## Convention de commit

Nous utilisons [Conventional Commits](https://www.conventionalcommits.org/) :

- `feat:` nouvelle fonctionnalité
- `fix:` correction de bug
- `docs:` documentation uniquement
- `test:` ajout ou modification de tests
- `chore:` maintenance (dépendances, CI…)

Exemple : `feat: ajouter le support des fichiers CSV compressés`

## Environnement de développement

```bash
git clone https://github.com/ggautreau/IA-BioSoftware-Workshop.git
cd IA-BioSoftware-Workshop/tp_python
pixi install
pixi run all-checks
```
