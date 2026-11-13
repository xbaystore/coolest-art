# The Lighthouse at the Edge of the Desert Sea

Entry for make.fun's `coolest-art-01`.

A lighthouse stands on the crest of a desert dune shaped like a giant
ocean wave, frozen mid-crash. Its beam cuts across a teal dusk while a
pale sun rises over the sands below: a sea made of sand, patrolled by a
light that has nothing to warn. Flat poster illustration in deep teal,
indigo, burnt orange and gold, with a fine grain — one huge wave, one
tiny lighthouse, one sun, readable across the room and at thumbnail
size alike.

## How it runs

`main.py` (Python 3.13, standard library only) copies the bundled
`art.jpg` (1024×1024, 189 KB) to `entry.png` in the output directory
(`MAKEFUN_OUTPUT_DIR`, default `/output`), after checking the asset's
magic bytes and size against the competition gate. The judge sees
exactly the bytes that ship in this repository; every run produces
identical output.
