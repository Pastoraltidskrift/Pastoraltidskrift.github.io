# Bonitas Foundation

Hugo-sajt för **https://bonitasfoundation.org/** med ett eget tema, `bonitas`.
Startsidan är en “Coming soon”-sida och `/about/` beskriver stiftelsens värdegrund.

## Arbeta lokalt

Installera [Hugo](https://gohugo.io/installation/) **0.166.0 eller senare**.
Sajten behöver varken Node.js, npm, Hugo Extended eller externa teman.

```sh
hugo server --disableFastRender
```

Öppna adressen som Hugo visar, normalt http://localhost:1313/.

```sh
hugo --gc --minify --panicOnWarning
python3 scripts/check-site.py
```

Byggresultatet hamnar i `public/` och ska inte checkas in.

## Innehåll och form

- `content/_index.md`: rubrik, ingress, text och länk på startsidan.
- `content/about.md`: About-sidans text, värdeord och avslutning.
- `hugo.toml`: domän, sidtitel, beskrivning, sidfot och meny.
- `themes/bonitas/layouts/`: Hugo-mallar, inklusive en egen 404-sida.
- `themes/bonitas/assets/css/main.css`: responsiv layout och färgpalett.
- `assets/images/wheat-field.png`: originalbild; Hugo skapar optimerade WebP-varianter.
- `themes/bonitas/static/fonts/`: lokala Calendas Plus-fonter i WOFF2.
- `docs/Bonitas Graphic Quick Guide.webp`: grafisk profil.

Calendas Plus används genomgående enligt uppdraget. Färgerna och korsets form
utgår från den grafiska guiden. Fontfilerna kommer från projektets medföljande
`Calendas-Plus-Webfont/`; licensen finns i `docs/calendas-plus-webfont-license.pdf`. Inga fonter eller skript laddas
från externa tjänster. Se `docs/image-source.md` för bildens ursprung och prompt.

## GitHub Pages

Repo: https://github.com/Pastoraltidskrift/Pastoraltidskrift.github.io

Workflow: `.github/workflows/hugo.yml`.

Push till `main` bygger, kontrollerar och publicerar sajten. Pull requests bygger
och kontrolleras utan publicering. Flödet kan även startas manuellt från Actions.
Hugo och Actions-versioner är låsta; Hugo-arkivets SHA-256 kontrolleras vid hämtning.

I repots **Settings → Pages → Build and deployment** ska Source vara
**GitHub Actions**. Custom domain ska vara **bonitasfoundation.org** och
**Enforce HTTPS** ska vara aktiverat. Befintliga DNS-poster för GitHub Pages kan
användas vidare. `static/CNAME` följer med vid varje bygge; rotens `CNAME` behålls
också för att göra domänen tydlig i repot. Ändra båda filerna och `baseURL` i
`hugo.toml` om domänen ska bytas.
