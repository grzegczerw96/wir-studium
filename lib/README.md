# Biblioteki strony (z własnego serwera)

Te same pliki co na cdnjs, unpkg i jsdelivr (sprawdzone sumą MD5), ładowane z `defer`:
`gsap-3.12.5.min.js`, `ScrollTrigger-3.12.5.min.js`, `lenis-1.1.13.min.js`.

`three-0.149.0-wir.min.js`: Three.js r149 tylko z klasami, których używa strona (111 KB po kompresji zamiast 153 KB),
jako `window.THREE` jak pełna wersja. Zbudowane esbuildem z pakietu `three@0.149.0`:

```js
// entry.js
export { WebGLRenderer, Scene, PerspectiveCamera, Color, Mesh, PlaneGeometry, MeshBasicMaterial, DoubleSide, PMREMGenerator,
  Curve, Vector3, TubeGeometry, MeshPhysicalMaterial, Group, DirectionalLight, sRGBEncoding, ACESFilmicToneMapping } from 'three';
```

```
npm i three@0.149.0 esbuild@0.17.19
npx esbuild entry.js --bundle --minify --format=iife --global-name=THREE --target=es2018 --legal-comments=none --outfile=three-wir.min.js
```

Potem na początek pliku z powrotem nagłówek licencji MIT Three.js (jest w pliku).

Nowa klasa `THREE.X` w `index.html` = dopisać ją do `entry.js` i zbudować od nowa (inaczej `THREE.X` jest `undefined`).
Lista użytych klas: `grep -o "THREE\.[A-Za-z0-9]*" index.html | sort -u`.
