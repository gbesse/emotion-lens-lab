# Emotion Lens Lab

[English](README.en.md) · [Español](README.es.md)

**Comparer ce qu’un texte exprime, ce qu’un personnage ressent et ce que plusieurs lecteurs déclarent ressentir — sans les confondre.**

Un même passage peut faire sursauter un personnage, rire un lecteur et en agacer un autre. Ce carnet garde les couches séparées, mesure leur couverture et montre le désaccord entre lecteurs. Chaque annotation reste liée à un passage exact, à un observateur et à l’empreinte du texte.

## Essayer en trente secondes

Python 3.11+ ; la démo ne nécessite aucune clé ni requête distante.

```sh
git clone https://github.com/gbesse/emotion-lens-lab
cd emotion-lens-lab
python3 -m emotion_lens serve --lang fr
```

Ouvrir `http://127.0.0.1:8771/?lang=fr`. Le court récit original et les **réactions synthétiques** sont un exercice, pas des annotations humaines collectées. Au passage 2, le personnage a peur ; les deux lecteurs fictifs divergent. Leur écart absolu moyen sur quatre émotions vaut **0,65**. Sept observations sont présentes sur huit cellules possibles ; le trou reste visible.

Cliquer un passage, saisir ses propres intensités entre 0 et 1 et enregistrer une observation. Changer la langue de l’interface conserve le texte et sa langue ; charger explicitement un autre exercice crée un autre carnet. Le navigateur conserve le carnet localement. Créer un nouveau carnet retire ses anciennes annotations.

Exporter le carnet JSON, la courbe SVG et un **carnet Markdown pour Obsidian**, avec passages exacts, empreinte et ancres de blocs stables. L’export fonctionne sans plugin Obsidian. Le Markdown et le SVG sont générés par le programme ; aucun modèle ne réécrit le texte de l’auteur.

Importer un carnet JSON permet aussi d’afficher les annotations issues de Jev ; le carnet importé remplace explicitement le précédent.

![Carnet](docs/preview-en.png)

## Ce qui est calculé

Quatre intensités déclarées : joie, peur, tristesse, colère. Elles ne sont pas obligées de sommer à un. La moyenne concerne uniquement les déclarations de lecteurs ; les couches texte et personnage restent à part. Le désaccord est la moyenne des écarts absolus, sur les quatre émotions et toutes les paires de lecteurs d’un passage. Avec moins de deux lecteurs, il reste inconnu. Les identifiants ne vérifient ni identité, ni indépendance, ni sincérité.

Le découpage se fait aux paragraphes. Les offsets sont des **points de code Unicode**, pas des octets ni des unités UTF-16 ; les accents et emojis sont testés. Une modification du texte ou de ses passages invalide les annotations précédentes au lieu de les déplacer silencieusement. Aucun lissage ne relie deux passages séparés par une absence d’annotation.

```sh
python3 -m emotion_lens demo --lang fr
python3 -m emotion_lens analyze emotion_lens/examples/fr.json
python3 -m emotion_lens markdown emotion_lens/examples/fr.json --lang fr > carnet.md
python3 -m emotion_lens svg emotion_lens/examples/fr.json --lang fr > courbe.svg
```

`pip install .` fournit aussi `emotion-lens`. UI, erreurs, exemples et exports FR/EN/ES ; aucune traduction automatique des textes utilisateur.

## Classer avec Jev, explicitement

```sh
pip install .
# Fournir TYPESAFE_API_KEY dans l’environnement, sans l’inscrire dans le code.
python3 -m emotion_lens classify emotion_lens/examples/fr.json > carnet-modele.json
```

Cette commande envoie au plus trois passages à `api.typesafe.ai`, **une requête payante**, modèle `jev-1.13.0`, une question `choice` par passage. La bibliothèque `classify(..., perspective="character", target="Mira", max_segments=3)` accepte aussi les perspectives personnage et hypothèse de lecteur. La limite explicite est de six passages et 18 000 caractères de requête. Timeout 30 s, TLS vérifié, redirections et relances désactivées. Aucun appel payant depuis le navigateur.

Les sept choix sont joie, peur, tristesse, colère, neutre, mêlé, incertain. **Une probabilité de choix n’est pas une intensité émotionnelle.** Les distributions et la confiance restent dans une couche modèle distincte, jamais comme déclaration d’un lecteur. Une réponse invalide est refusée ; l’appel ne remplace pas les annotations humaines ou synthétiques.

Un essai réel sur trois passages originaux français est conservé dans [live-text-annotations.json](docs/live-text-annotations.json) : une requête, 911 tokens d’entrée et 206 de sortie, sans modification des sept déclarations synthétiques. Ce test valide l’intégration, pas l’exactitude émotionnelle. Aucune clé n’est publiée. Projet indépendant, sans affiliation à TypeSafe AI. [Documentation TypeSafe](https://docs.typesafe.ai/primitives/choice).

## Comparaisons et limites

[EmotionArcs](https://aclanthology.org/2024.latechclfl-1.7/) publie déjà des arcs sur des milliers de romans. [read-with-jev](https://github.com/carlaiau/read-with-jev) propose déjà un lecteur, des associations émotionnelles Jev et une carte de personnages. Nous ne revendiquons ni le premier lecteur émotionnel, ni une meilleure classification. L’angle de ce dépôt est **le carnet de perspectives attribuées, les réactions comparables de lecteurs, les trous de couverture et les passages exportables**.

Le modèle n’établit pas ce qu’un lecteur réel ressent. Les noms de personnages sont déclarés, sans résolution automatique des pronoms. La portée d’un paragraphe peut manquer de contexte. Pas de validation psychométrique, d’évaluation sur un corpus annoté humain, de diagnostic, de mesure de qualité littéraire ou de supériorité SOTA. Serveur local uniquement ; pas de comptes, synchronisation multiutilisateur, PDF ou EPUB.

## Vérifier

```sh
python3 -m unittest discover -s tests -v
npm ci
npx playwright install chromium
npm run test:browser
npm run format:check
```

Treize tests : offsets Unicode, empreintes périmées, séparation des perspectives, oracle arithmétique du désaccord, trous, observations idempotentes, export exact et réponse modèle bornée. Navigateur FR/EN/ES, édition, exports, conservation du texte, injection et mobile. CI Python 3.11/3.12, roue installée hors sources et navigateur. Les tests n’appellent pas Jev. Licence MIT ; alpha publique.
