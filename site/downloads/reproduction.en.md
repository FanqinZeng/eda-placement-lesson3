# Source and reproduction guide

## Verify in the website first

Return to the interactive lab and load the standard square. Expect HPWL 4, Clique 16, and Star-from-A 8. Switch to the asymmetric preset, change the hub, and compare with the tables in this reading room.

The lab computes locally in your browser and requires no login. Reading Python and JSON requires no software installation. Use the local instructions below when you want to run or modify the project yourself.

## Run Python yourself

The complete exercise template and reference implementation appear on this page. Copy the code into an editor or download the original file.

Save the reference implementation as reference.py and run this example in the same directory:

```python
from reference import evaluate

pins = [
    {"id": "A", "x": 2, "y": 2},
    {"id": "B", "x": 4, "y": 2},
    {"id": "C", "x": 2, "y": 4},
    {"id": "D", "x": 4, "y": 4},
]
print(evaluate(pins, "A"))  # [4, 16, 8]
```

The reference implementation uses only the Python standard library. In examples.json, datasets are grouped by preset name. Pass one preset’s pin list, such as data["golden"], to evaluate, rather than the entire dictionary.

## Run the whole website offline

Download the full course repository, then run from its root:

```bash
python3 scripts/serve.py --port 8000
```

Open http://localhost:8000 in a browser. The local server supports video range requests, so chapter seeking works. The repository includes videos, bilingual captions, transcripts, and experiment assets. Playing the rendered films does not call the speech service again.

## Modify the lesson or remake the film

- Website and algorithms: site/index.html, site/assets/models.mjs, and site/assets/app.mjs.
- Reading room: scripts/build_reading.py generates it from the authored notes, code, data, and transcripts. Run python3 scripts/build_reading.py after changing them.
- Chinese storyboard: video/story.json; English storyboard: video/story.en.json.
- Frozen speech and actual sentence timestamps: video/audio/ and video/audio/en/.
- Speech and rendering: scripts/speech.py and scripts/render-film.py, using --lang zh or --lang en.
- Bilingual captions: run scripts/build-bilingual-captions.py --mux after rendering both films to generate synchronized tracks and embed subtitles in MP4.

See the [course source and README](https://github.com/FanqinZeng/eda-placement-lesson3) for full commands, dependencies, and licenses.

## Check the results

```bash
node --test tests/*.test.mjs
python3 scripts/check-site.py
python3 scripts/build_reading.py --check
```

Media stream, loudness, and caption checks require production dependencies. Run scripts/verify-media.py and scripts/verify-media.py --lang en. Automated tests do not replace full human listening review or verification on every physical device.

New code is MIT; new teaching material is CC BY 4.0. See THIRD_PARTY_NOTICES.md in the repository for teacher material, fonts, and synthesized speech attribution.
