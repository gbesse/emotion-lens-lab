const translations = {
  fr: {
    eyebrow: 'TEXTE · PERSONNAGE · LECTEURS',
    title: 'Même passage. Deux lectures opposées.',
    lede: 'Un personnage a peur ; un lecteur rit, un autre s’agace. Gardez ces perspectives séparées et retrouvez chaque observation dans le texte exact.',
    notebook: 'Votre carnet local',
    input: 'Texte original',
    doclang: 'Langue du texte',
    replace: 'Créer un nouveau carnet',
    demo: 'Charger l’exercice dans cette langue',
    import: 'Importer un carnet JSON (remplace le carnet)',
    replaceWarning:
      'Un nouveau carnet retire les annotations précédentes. Changer la langue de l’interface conserve votre texte.',
    add: 'Annoter le passage sélectionné',
    observer: 'Identifiant du lecteur / annotateur',
    perspective: 'Perspective',
    reader: 'Réaction déclarée du lecteur',
    text: 'Émotion du texte',
    character: 'Émotion du personnage',
    reader_hypothesis: 'Hypothèse de réaction du lecteur',
    target: 'Personnage concerné',
    save: 'Enregistrer cette observation',
    local:
      'Texte et carnet restent dans ce navigateur et le serveur local. Aucune classification distante depuis cette interface.',
    provenance: 'PASSAGES VÉRIFIÉS',
    readers: 'lecteurs déclarés',
    coverage: 'observations / cellules possibles',
    disagreement: 'désaccord au passage 2',
    fixture:
      'Les réactions du scénario fourni sont des exemples synthétiques, pas des lecteurs mesurés.',
    real: 'Carnet contenant des observations saisies localement ; identité et sincérité non vérifiées.',
    gaps: 'Courbes : moyenne des intensités déclarées, de 0 à 1. Un passage non annoté reste un trou ; aucun lissage. Désaccord : écart absolu moyen par émotion et paire de lecteurs, entre 0 et 1.',
    markdown: 'Exporter pour Obsidian',
    svg: 'Exporter la courbe SVG',
    json: 'Exporter le carnet JSON',
    limits:
      'Outil d’annotation et de comparaison. Les sentiments du lecteur ne se déduisent pas du texte comme des faits. Les probabilités de choix d’un modèle restent distinctes des intensités déclarées. Pas de validation psychométrique ni de supériorité SOTA.',
    joy: 'Joie',
    fear: 'Peur',
    sadness: 'Tristesse',
    anger: 'Colère',
    selected: 'Passage sélectionné',
    missing: 'Non annoté',
    reports: 'déclarations',
    pairDistance: 'désaccord',
    saved: 'Observation enregistrée.',
    error: 'Entrée non valide.',
    synthetic_fixture: 'Exemple synthétique',
    self_report: 'Déclaration locale',
    human_annotation: 'Annotation locale',
    model_choice: 'Choix du modèle',
    probability: 'Probabilités de choix, pas intensités',
  },
  en: {
    eyebrow: 'TEXT · CHARACTER · READERS',
    title: 'Same passage. Two opposite readings.',
    lede: 'A character is afraid; one reader laughs, another feels annoyed. Keep these perspectives separate and trace every observation to the exact text.',
    notebook: 'Your local notebook',
    input: 'Original text',
    doclang: 'Text language',
    replace: 'Create a new notebook',
    demo: 'Load the exercise in this language',
    import: 'Import notebook JSON (replaces notebook)',
    replaceWarning:
      'A new notebook removes previous annotations. Changing the interface language preserves your text.',
    add: 'Annotate the selected passage',
    observer: 'Reader / annotator identifier',
    perspective: 'Perspective',
    reader: 'Reader self-report',
    text: 'Text emotion',
    character: 'Character emotion',
    reader_hypothesis: 'Reader reaction hypothesis',
    target: 'Character concerned',
    save: 'Save this observation',
    local:
      'Text and notebook remain in this browser and local server. No remote classification from this interface.',
    provenance: 'VERIFIED PASSAGES',
    readers: 'declared readers',
    coverage: 'observations / possible cells',
    disagreement: 'disagreement at passage 2',
    fixture: 'The supplied scenario’s reactions are synthetic examples, not measured readers.',
    real: 'Notebook contains locally entered observations; identity and sincerity are not verified.',
    gaps: 'Curves: mean self-reported intensities, from 0 to 1. Unannotated passages remain gaps; no smoothing. Disagreement: mean absolute difference per emotion and reader pair, between 0 and 1.',
    markdown: 'Export for Obsidian',
    svg: 'Export SVG arc',
    json: 'Export notebook JSON',
    limits:
      'Annotation and comparison tool. Reader feelings cannot be inferred from text as facts. Model choice probabilities remain separate from self-reported intensities. No psychometric validation or SOTA superiority.',
    joy: 'Joy',
    fear: 'Fear',
    sadness: 'Sadness',
    anger: 'Anger',
    selected: 'Selected passage',
    missing: 'Unannotated',
    reports: 'self-reports',
    pairDistance: 'disagreement',
    saved: 'Observation saved.',
    error: 'Invalid input.',
    synthetic_fixture: 'Synthetic example',
    self_report: 'Local self-report',
    human_annotation: 'Local annotation',
    model_choice: 'Model choice',
    probability: 'Choice probabilities, not intensities',
  },
  es: {
    eyebrow: 'TEXTO · PERSONAJE · LECTORES',
    title: 'Mismo pasaje. Dos lecturas opuestas.',
    lede: 'Un personaje tiene miedo; un lector ríe y otro se irrita. Mantenga separadas estas perspectivas y vincule cada observación al texto exacto.',
    notebook: 'Su cuaderno local',
    input: 'Texto original',
    doclang: 'Idioma del texto',
    replace: 'Crear un cuaderno nuevo',
    demo: 'Cargar el ejercicio en este idioma',
    import: 'Importar cuaderno JSON (sustituye el cuaderno)',
    replaceWarning:
      'Un cuaderno nuevo elimina las anotaciones anteriores. Cambiar el idioma de la interfaz conserva su texto.',
    add: 'Anotar el pasaje seleccionado',
    observer: 'Identificador del lector / anotador',
    perspective: 'Perspectiva',
    reader: 'Reacción declarada del lector',
    text: 'Emoción del texto',
    character: 'Emoción del personaje',
    reader_hypothesis: 'Hipótesis de reacción del lector',
    target: 'Personaje afectado',
    save: 'Guardar esta observación',
    local:
      'Texto y cuaderno permanecen en este navegador y servidor local. Sin clasificación remota desde esta interfaz.',
    provenance: 'PASAJES VERIFICADOS',
    readers: 'lectores declarados',
    coverage: 'observaciones / celdas posibles',
    disagreement: 'desacuerdo en el pasaje 2',
    fixture: 'Las reacciones del escenario son ejemplos sintéticos, no lectores medidos.',
    real: 'Cuaderno con observaciones introducidas localmente; identidad y sinceridad no verificadas.',
    gaps: 'Curvas: media de intensidades declaradas, de 0 a 1. Los pasajes sin anotar dejan huecos; sin suavizado. Desacuerdo: diferencia absoluta media por emoción y pareja de lectores, entre 0 y 1.',
    markdown: 'Exportar para Obsidian',
    svg: 'Exportar curva SVG',
    json: 'Exportar cuaderno JSON',
    limits:
      'Herramienta de anotación y comparación. Los sentimientos del lector no se infieren del texto como hechos. Las probabilidades del modelo se separan de las intensidades declaradas. Sin validación psicométrica ni superioridad SOTA.',
    joy: 'Alegría',
    fear: 'Miedo',
    sadness: 'Tristeza',
    anger: 'Ira',
    selected: 'Pasaje seleccionado',
    missing: 'Sin anotar',
    reports: 'declaraciones',
    pairDistance: 'desacuerdo',
    saved: 'Observación guardada.',
    error: 'Entrada no válida.',
    synthetic_fixture: 'Ejemplo sintético',
    self_report: 'Declaración local',
    human_annotation: 'Anotación local',
    model_choice: 'Elección del modelo',
    probability: 'Probabilidades de elección, no intensidades',
  },
};
const lang = new URLSearchParams(location.search).get('lang') || 'en',
  t = translations[lang] || translations.en;
document.documentElement.lang = translations[lang] ? lang : 'en';
document.querySelectorAll('[data-i18n]').forEach((el) => (el.textContent = t[el.dataset.i18n]));
const $ = (id) => document.getElementById(id),
  emotions = ['joy', 'fear', 'sadness', 'anger'];
let bundle,
  report,
  selected = 'p2';
for (const e of emotions) {
  const label = document.createElement('label');
  label.textContent = t[e];
  const input = document.createElement('input');
  input.type = 'range';
  input.min = '0';
  input.max = '1';
  input.step = '.05';
  input.value = '.5';
  input.id = `score-${e}`;
  label.append(input);
  $('scores').append(label);
}
async function post(path, data, raw = false) {
  const response = await fetch(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...data, lang: document.documentElement.lang }),
  });
  if (!response.ok) throw Error(t.error);
  return raw ? response.text() : response.json();
}
function element(tag, text, cls) {
  const e = document.createElement(tag);
  e.textContent = text;
  if (cls) e.className = cls;
  return e;
}
async function render() {
  report = await post('/api/analyze', { bundle });
  localStorage.setItem('emotion-lens-v1', JSON.stringify(bundle));
  $('input').value = bundle.document.text;
  $('document-language').value = bundle.document.language;
  $('story-title').textContent = bundle.document.title || t.notebook;
  $('source-hash').textContent = report.source_sha256;
  $('readers').textContent = report.reader_count;
  $('coverage').textContent = `${report.observed_reader_cells}/${report.possible_reader_cells}`;
  $('disagreement').textContent = report.segments[1]?.reader_disagreement?.toFixed(2) ?? '—';
  $('fixture').textContent = report.all_reader_reports_synthetic ? t.fixture : t.real;
  // SVG is generated server-side from validated numbers and translated constants only.
  const drawing = await post('/api/svg', { bundle }, true);
  $('chart').replaceChildren(
    new DOMParser().parseFromString(drawing, 'image/svg+xml').documentElement,
  );
  $('passages').replaceChildren();
  for (const row of report.segments) {
    const card = element('section', '', `passage${row.id === selected ? ' selected' : ''}`);
    card.dataset.segment = row.id;
    card.append(element('h3', `${row.id} · ${row.start}–${row.end}`), element('p', row.text));
    const layers = element('div', '', 'layers');
    for (const a of row.annotations) {
      let detail = `${t[a.perspective]} · ${a.observer}${a.target ? ' / ' + a.target : ''}\n${t[a.method]}\n`;
      detail +=
        a.method === 'model_choice'
          ? `${t.probability}: ${a.choice}`
          : emotions.map((e) => `${t[e]} ${a.scores[e].toFixed(2)}`).join(' · ');
      layers.append(element('div', detail, 'layer'));
    }
    card.append(
      layers,
      element(
        'p',
        `${row.reader_count} ${t.reports} · ${t.pairDistance} ${row.reader_disagreement?.toFixed(2) ?? '—'}`,
        'hint',
      ),
    );
    card.onclick = () => {
      selected = row.id;
      document
        .querySelectorAll('.passage')
        .forEach((e) => e.classList.toggle('selected', e.dataset.segment === selected));
      $('selected').textContent = `${t.selected}: ${selected}`;
    };
    $('passages').append(card);
  }
  $('selected').textContent = `${t.selected}: ${selected}`;
}
function fail() {
  $('status').textContent = t.error;
}
$('import').onchange = async () => {
  try {
    const file = $('import').files[0];
    if (!file || file.size > 500000) throw Error();
    const next = JSON.parse(await file.text());
    await post('/api/analyze', { bundle: next });
    bundle = next;
    selected = bundle.document.segments[0].id;
    await render();
  } catch {
    fail();
  }
};
$('replace').onclick = async () => {
  try {
    bundle = await post('/api/document', {
      text: $('input').value,
      language: $('document-language').value,
    });
    selected = 'p1';
    await render();
  } catch {
    fail();
  }
};
$('demo').onclick = async () => {
  bundle = await (await fetch(`/api/example?lang=${document.documentElement.lang}`)).json();
  selected = 'p2';
  await render();
};
$('save').onclick = async () => {
  try {
    const perspective = $('perspective').value,
      observer = $('observer').value,
      target = perspective === 'character' ? $('target').value : undefined;
    const next = structuredClone(bundle);
    next.annotations = next.annotations.filter(
      (a) =>
        !(
          a.segment === selected &&
          a.perspective === perspective &&
          a.observer === observer &&
          a.target === target
        ),
    );
    next.annotations.push({
      source_sha256: bundle.document.sha256,
      segment: selected,
      perspective,
      observer,
      ...(target ? { target } : {}),
      method: perspective === 'reader' ? 'self_report' : 'human_annotation',
      scores: Object.fromEntries(emotions.map((e) => [e, Number($(`score-${e}`).value)])),
    });
    await post('/api/analyze', { bundle: next });
    bundle = next;
    await render();
    $('status').textContent = t.saved;
  } catch {
    fail();
  }
};
function download(text, name, type) {
  const url = URL.createObjectURL(new Blob([text], { type }));
  const a = document.createElement('a');
  a.href = url;
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
$('markdown').onclick = async () =>
  download(await post('/api/markdown', { bundle }, true), 'emotion-notebook.md', 'text/markdown');
$('svg').onclick = async () =>
  download(await post('/api/svg', { bundle }, true), 'emotion-arc.svg', 'image/svg+xml');
$('json').onclick = () =>
  download(JSON.stringify(bundle, null, 2), 'emotion-notebook.json', 'application/json');
try {
  bundle = JSON.parse(localStorage.getItem('emotion-lens-v1'));
  if (!bundle)
    bundle = await (await fetch(`/api/example?lang=${document.documentElement.lang}`)).json();
  await render();
} catch {
  fail();
}
