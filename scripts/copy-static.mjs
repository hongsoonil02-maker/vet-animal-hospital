import { cpSync, mkdirSync, existsSync } from "fs";
import { join } from "path";

const root = process.cwd();
const dist = join(root, "dist");

function copy(src, dest) {
  const s = join(root, src);
  const d = join(dist, dest || src);
  if (!existsSync(s)) { console.warn(`skip missing: ${src}`); return; }
  mkdirSync(join(d, ".."), { recursive: true });
  cpSync(s, d, { recursive: true });
  console.log(`copied ${src} -> ${dest || src}`);
}

copy("assets", "assets");
copy("config", "config");
copy("sitemap.xml");
copy("robots.txt");
// public/_headers already copied by vite, but ensure
copy("public/_headers", "_headers");
console.log("static copy done");
