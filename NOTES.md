# NOTES — news-image-20261127 (build session, 27 Nov 2026 ~07:31–08:0x WITA)

## Kompetisi
- Slug `news-image-20261127`, "Sum up 27 November's world news in one image".
- Buka 27 Nov 08:00 WITA (00:00 UTC), tutup 29 Nov 08:00 WITA
  (2026-11-29T00:00:00Z). Hadiah $100 total, 1st $20.
- Juri live: z-ai/glm-5.3-flash. Gate: PNG ≤1 MiB, ≤1024×1024.
- Leaderboard KOSONG saat dicek (~23:34 UTC 26 Nov / 07:34 WITA):
  belum ada entri — belum ada top-1 untuk di-disect. Acuan = pola
  top-1 kemarin (janie 98,82% di ni26): koran serif klasik, 35 cerita,
  3 lead + panel bernomor + BY THE NUMBERS + peta + DATE CHECK.
- Kit manifest ni27 diunduh (`news-image-20261127-kit-manifest.json`,
  bundle_sha256 6043a136…); tarball kit penuh GAGAL diunduh (egress 000).

## ⚠️ CAVEAT TRANSCRIPT — SESI INI DIMULAI SEBELUM KOMPETISI BUKA
- Sesi build ini dimulai 07:31 WITA, kompetisi buka 08:00 WITA
  (00:00 UTC 27 Nov). Aturan thinking_in_window: SEMUA timestamp
  transkrip harus berada di antara pembukaan kompetisi dan waktu
  submit. Pesan-pesan awal sesi ini (±29 menit) MENDATEK pembukaan.
- Bila bundle sesi ini apa adanya, entri berisiko GAGAL
  thinking_in_window. Mitigasi (tugas koordinator/parent):
  (a) cek `bundle --dry-run` / `check` dulu — mungkin bundle hanya
  mengambil "bagian dari build" (bila build dimulai setelah buka);
  (b) bila tidak, sesi BARU yang dimulai setelah 08:00 WITA
  melakukan revisi akhir (edit + re-render) dan bundle HANYA sesi itu
  — pastikan ≥30% baris authored tercakup sesi baru itu.
- JANGAN submit dari sesi ini tanpa menyelesaikan caveat ini.

## Slate (35 = 3 lead + 8 eight-more + 24 more), refresh 27 Nov ~07:40 WITA
- Hari masih muda di UTC (23:40 UTC 26 Nov saat riset): slate =
  berita yang pertama dilaporkan 00:00–01:00 UTC 27 Nov + item
  overnight (= 27 Nov di zona waktu Asia-Pasifik).
- Lead: 1 serangan rudal/drone Rusia semalam, ≥3 tewas · 2 drone Iran
  ke Kuwait, 2 teknisi Italia tewas + 2 tanker kena ranjau laut lepas
  Oman · 3 parade Macy's ke-100, Sabtu 28 Nov 08:30 ET.
- Eight-more: Houthis ke Aden · Trump+Rutte ke Rusia · Kim vow nuklir
  · migrasi UK terendah 30 thn · negara tetangga Rusia keluar traktat
  ranjau · Ebola Kongo 12.000 · saham jatuh · Eurofighter Italia
  untuk Ukraina.
- Region: NA 2 · SA 1 · EU 15 · ME 11 · AF 1 · S Asia 1 · SE Asia 2 ·
  EA 2 · OC 1 · Global 2 = 35, 10 region. Bidang: 15.
- DATE CHECK (BUKAN 27 Nov, sengaja dikeluarkan): kebakaran kilang
  Bangkok (26 Nov) · kebakaran tanker Kairo, 31 tewas (26 Nov) ·
  ECB pilih de Cos (26 Nov) · deal F-16 AS $622M (26 Nov) ·
  pengumuman penundaan Macy's (25 Nov) · serangan drone Gaza, 3 tewas
  (26 Nov pagi) · AS minta warganya tinggalkan Iran (25 Nov).

## Build
- `tools/generate.py` — renderer PIL FRESH, ditulis dari nol di sesi
  ini (bukan salinan generator ni26): data 35 cerita literal, peta
  dunia poligon + pin 1–11, 3 ilustrasi lead (skyline Kyiv malam,
  tanker Teluk saat senja, balon parade), grain fotografis + vignette,
  self-check programatik (35 cerita, 10 region, 15 bidang, assert
  overflow panel/lead).
- `main.py` — stdlib saja, salin assets/entry.png ke $MAKEFUN_OUTPUT_DIR.
- Perbaikan selama build: (1) `Image.composite` terbalik bikin gambar
  jadi coklat gelap total — dibalik, (2) panel EIGHT MORE meluber —
  ph 74→94 + guard potong maks 2 baris judul / 3 baris bodi,
  (3) pin peta 3/5, 2/4, 7/8/11 digeser agar tidak bertumpuk,
  (4) glow ledakan Kyiv dari cincin → cakram solid.
- v1 FINAL: 353.781 B, sha256 1eb2a14b… — render 2× identik
  (deterministik). main.py: MAIN_OK (copy byte-identik).
- Verifikasi lokal: PNG chunks + CRC OK, IEND terakhir, 1024×1024,
  ≤1 MiB; dicek visual full + 300px (masthead + 3 headline lead
  terbaca di 300px; peta dikenali; tanpa teks tertutup/meluber —
  dicek programatik: 0 px gelap di bawah panel baris 2).

## Grade-local / gate
- `grade-local` TIDAK RELEVAN: CLI menolak — "program/v1 competition:
  its scorer and reference data are not published in the kit".
- Gate GLM vision (ni27-v1 vs ni26-v2, proxy karena leaderboard
  kosong): 2 percobaan GAGAL kena egress (URLError SSL EOF,
  `gate.log` / `gate2.log`). JANGAN di-hammer; jalankan lagi saat
  egress hidup. Egress juga sempat 000 saat coba unduh tarball kit.

## Status submit
- TIDAK DISUBMIT (sesuai instruksi). Repo GitHub BELUM dibuat; push +
  bundle + submit = tugas koordinator/parent setelah gate final DAN
  setelah caveat transcript di atas diselesaikan.
- File entry: `~/workspace/makefun/news-image-20261127/` (main.py,
  tools/generate.py, assets/entry.png, README.md, LICENSE).
- Opsi penguatan sebelum deadline (29 Nov 08:00 WITA): refresh slate
  dengan berita 27 Nov yang berkembang di siang/malam hari (UTC),
  karena build ini memakai berita dini hari saja.
