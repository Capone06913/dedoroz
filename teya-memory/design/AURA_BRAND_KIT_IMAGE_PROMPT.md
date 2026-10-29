# Brand-kit prompt

Один лист для `gpt-image-2`, когда инструмент появится в MCP KV. Сейчас генерация не запускалась: инструмента нет. Лица этим промптом тоже не заказываются.

## Промпт

```text
A single large brand-kit board for an adult banquet program, 16:9, no people, no faces, no Santa, no Snow Maiden, no children, no cartoon snow, no snowflakes, no emojis, no letters in Russian, no watermark.

Layout as one clean contact sheet on warm ivory #F7F1E8:
1. Five large color swatches labeled in Latin only: NIGHT #141218, CRANBERRY #6E1A28, IVORY #F7F1E8, GOLD LINE #8A6232, CLASSIC BLUE #1E4F86.
2. Typography specimens in Latin: "Cormorant Garamond" as a high-contrast serif headline, "Manrope" as a grotesque price "8 000".
3. One solid cranberry button with ivory label CALL, sharp enough to read, corner radius 12px, not a pill, not transparent.
4. Three ivory price cards with a 1px gold rule on top, radius 12px, soft shadow, no logos.
5. A macro photo inset of red sequin fabric, white fur edge, and a microphone mesh, studio light, no human skin.
6. A dark hall bokeh of warm practical lights, empty, no stage characters.
7. A small mobile frame 375px wide showing a bottom solid cranberry bar, no tiny unreadable text.
8. Two contrast pairs drawn as bars: cranberry with ivory text, ivory with near-black text.

Photography style: real fabric and real light, not 3D, not clay, not illustration, not New Year clipart. No glasses of champagne, no five costume variants, no gold confetti explosion.
```

## Negative

```text
people, faces, children, Ded Moroz, Snow Maiden, beard, cartoon, emoji, snow overlay, 3D scene, neon, transparent button, competitor gold-and-glasses poster, unreadable microtext, watermark, logo of a venue
```

## Куда класть результат

`teya-memory/design/assets/brand-kit.png` после появления URL. До этого файла нет, и это записано как блокер в `AURA_ASSET_REGISTRY.json`.

Style anchor обложек — отдельный промпт в `AURA_BLOG_COVER_CONCEPT.json`. Его тоже не генерировать другой моделью.
