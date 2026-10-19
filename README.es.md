# Emotion Lens Lab

[Français](README.md) · [English](README.en.md)

**Comparar emociones del texto, del personaje y reacciones declaradas por varios lectores sin mezclar perspectivas.**

Un pasaje puede asustar a un personaje, divertir a un lector e irritar a otro. El cuaderno separa capas atribuidas, muestra huecos de cobertura y compara desacuerdos. Cada anotación conserva pasaje exacto, observador y huella del texto.

## Probar

Python 3.11+; la demostración no necesita clave ni petición remota.

```sh
git clone https://github.com/gbesse/emotion-lens-lab
cd emotion-lens-lab
python3 -m emotion_lens serve --lang es
```

Abrir `http://127.0.0.1:8771/?lang=es`. El relato original y las **reacciones sintéticas** son un ejercicio, no etiquetas humanas recopiladas. En el pasaje 2, el personaje tiene miedo mientras dos lectores ficticios discrepan: diferencia absoluta media de **0,65** entre cuatro emociones. Hay siete observaciones entre ocho celdas posibles; el hueco permanece visible.

Seleccionar un pasaje, introducir intensidades entre 0 y 1 y guardar una observación. Cambiar el idioma de interfaz conserva texto e idioma del documento. Cargar otro ejercicio crea explícitamente otro cuaderno. El navegador guarda el cuaderno localmente. Crear un cuaderno nuevo elimina anotaciones anteriores.

Exportar JSON, curva SVG y **Markdown para Obsidian**, con citas exactas, huella y anclas de bloques estables. No requiere plugin Obsidian. El programa genera Markdown y SVG; ningún modelo reescribe el texto del autor.

Importar un cuaderno JSON también muestra anotaciones Jev; la importación sustituye explícitamente el cuaderno anterior.

![Cuaderno](docs/preview-en.png)

## Cálculo

Cuatro intensidades declaradas: alegría, miedo, tristeza e ira; no necesitan sumar uno. Las medias de lectores excluyen capas de texto y personaje. El desacuerdo es la diferencia absoluta media por emoción y pareja de lectores de un pasaje. Con menos de dos lectores queda desconocido. Los identificadores no verifican identidad, independencia ni sinceridad.

Los offsets de párrafos usan **puntos de código Unicode**, no bytes ni unidades UTF-16; se prueban acentos y emojis. Modificar texto o pasajes invalida anotaciones anteriores en vez de desplazarlas silenciosamente. Las curvas no unen pasajes separados por huecos sin anotar.

```sh
python3 -m emotion_lens demo --lang es
python3 -m emotion_lens analyze emotion_lens/examples/es.json
python3 -m emotion_lens markdown emotion_lens/examples/es.json --lang es > cuaderno.md
python3 -m emotion_lens svg emotion_lens/examples/es.json --lang es > curva.svg
```

`pip install .` también instala `emotion-lens`. Interfaz, errores, ejemplos y exportaciones FR/EN/ES; nunca traduce automáticamente textos del usuario.

## Clasificación Jev explícita

```sh
pip install .
# Proporcionar TYPESAFE_API_KEY mediante el entorno, nunca en código.
python3 -m emotion_lens classify emotion_lens/examples/es.json > cuaderno-modelo.json
```

Envía como máximo tres pasajes a `api.typesafe.ai`: **una petición de pago**, modelo `jev-1.13.0`, una pregunta `choice` por pasaje. La biblioteca `classify(..., perspective="character", target="Mira", max_segments=3)` admite personaje e hipótesis de lector. Límites: seis pasajes y 18 000 caracteres de petición. TLS verificado, timeout de 30 s, sin redirecciones ni reintentos. El navegador no hace llamadas de pago.

Opciones: alegría, miedo, tristeza, ira, neutro, mezclado e incierto. **Las probabilidades de elección no son intensidades emocionales.** Distribuciones y confianza quedan en una capa de modelo separada, nunca como reacciones declaradas del lector. Respuestas inválidas se rechazan; las anotaciones humanas o sintéticas no se sustituyen.

[live-text-annotations.json](docs/live-text-annotations.json) guarda una prueba real con tres pasajes originales franceses: una petición, 911 tokens de entrada y 206 de salida, siete declaraciones sintéticas sin cambios. Valida la integración, no la exactitud emocional. No se publica ninguna clave. Proyecto independiente, no afiliado a TypeSafe AI. [Documentación TypeSafe](https://docs.typesafe.ai/primitives/choice).

## Comparaciones y límites

[EmotionArcs](https://aclanthology.org/2024.latechclfl-1.7/) ya publica curvas de miles de novelas. [read-with-jev](https://github.com/carlaiau/read-with-jev) ya ofrece lector, asociaciones Jev y mapa de personajes. No se afirma ser el primer lector emocional ni mejorar su clasificación. El enfoque es **perspectivas atribuidas, reacciones comparables, huecos de cobertura y pasajes exactos exportables**.

El modelo no establece qué siente un lector real. Los nombres de personajes son declarados; no resuelve pronombres. Un párrafo puede carecer de contexto. Sin validación psicométrica, evaluación sobre corpus humano anotado, diagnóstico, medida de calidad literaria ni superioridad SOTA. Servidor local; sin cuentas, sincronización multiusuario, PDF ni EPUB.

## Verificar

```sh
python3 -m unittest discover -s tests -v
npm ci
npx playwright install chromium
npm run test:browser
npm run format:check
```

Trece pruebas cubren Unicode, huellas obsoletas, separación de perspectivas, oráculo aritmético del desacuerdo, huecos, observaciones idempotentes, exportación exacta y validación del proveedor. Navegador FR/EN/ES, edición, exportaciones, conservación del texto, inyección y móvil; CI Python 3.11/3.12 y rueda fuera de fuentes. Las pruebas no llaman a Jev. MIT; alfa pública.
