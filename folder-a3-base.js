// Rede de pontos dos cantos (o motivo dos slides do Canva), desenhada em vetor; some em direção ao centro.
document.querySelectorAll("svg.rede").forEach(function (el) {
  var W = 100, H = 80, s = +el.dataset.seed;
  var rnd = function () { s = s * 16807 % 2147483647; return s / 2147483647; };
  var P = [];
  while (P.length < 30) {
    var x = W * Math.pow(rnd(), 1.5), y = H * Math.pow(rnd(), 1.5);
    if ((x / W) * (x / W) + (y / H) * (y / H) < 1) P.push([x, y]);
  }
  var fade = function (p) { return Math.max(0, 1 - Math.hypot(p[0] / W, p[1] / H)); };
  var seen = {}, out = [];
  P.forEach(function (p, i) {
    P.map(function (q, j) { return [Math.hypot(p[0] - q[0], p[1] - q[1]), j]; })
      .sort(function (a, b) { return a[0] - b[0]; }).slice(1, 4)
      .forEach(function (d) {
        var k = Math.min(i, d[1]) + "-" + Math.max(i, d[1]);
        if (seen[k]) return; seen[k] = 1;
        var q = P[d[1]], o = (0.12 + 0.55 * Math.min(fade(p), fade(q))).toFixed(2);
        out.push('<line x1="' + p[0].toFixed(2) + '" y1="' + p[1].toFixed(2) + '" x2="' + q[0].toFixed(2) + '" y2="' + q[1].toFixed(2) + '" stroke-opacity="' + o + '"/>');
      });
  });
  P.forEach(function (p) { out.push('<circle cx="' + p[0].toFixed(2) + '" cy="' + p[1].toFixed(2) + '" r=".55" fill-opacity="' + (0.2 + 0.7 * fade(p)).toFixed(2) + '"/>'); });
  var c = el.dataset.canto, t = { tl: "", tr: "translate(100 0) scale(-1 1)", bl: "translate(0 80) scale(1 -1)", br: "translate(100 80) scale(-1 -1)" }[c];
  el.setAttribute("viewBox", "0 0 100 80");
  el.setAttribute("preserveAspectRatio", "none");
  el.innerHTML = '<g transform="' + t + '">' + out.join("") + "</g>";
});

// #grafica: as 8 páginas soltas, em ordem de leitura, cada uma com 3 mm de sangria.
if (location.hash === "#grafica") {
  document.getElementById("tamanho").textContent = "@page{size:216mm 303mm;margin:0}";
  var doc = document.getElementById("espelhos"), box = document.createElement("div");
  box.className = "doc";
  [["A", 1], ["B", 0], ["B", 1], ["C", 0], ["C", 1], ["D", 0], ["D", 1], ["A", 0]].forEach(function (p) {
    var f = document.createElement("div"), c = document.getElementById(p[0]).cloneNode(true);
    f.className = "folha"; c.removeAttribute("id");
    c.style.left = (3 - 210 * p[1]) + "mm"; c.style.top = "3mm";
    f.appendChild(c); box.appendChild(f);
  });
  doc.replaceWith(box);
}
