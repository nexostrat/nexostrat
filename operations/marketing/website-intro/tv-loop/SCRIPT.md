# Intro V3 — Spoken Script + SPACE Cues

> **Total SPACE presses on shoot day:** 5
> **Estimated final cut:** 45s (raw take ~55-60s with pre/post-roll buffer)
> **Language:** Spanish, neutral LATAM. *Tú* register (not *usted*).
> **Tone:** *Tranquilidad y competencia.* Consultant who has already solved this — not a motivator. Hands steady, lower in frame. No fist, no pointing.

---

## How to use this file on shoot day

1. Open the TV deck at `tv-loop/index.html` (see `tv-loop/README` cues below).
2. Open this script on a teleprompter app (Elegant Prompter, or any web-based prompter). Mirror it to a phone or tablet placed near the camera at eye level.
3. **Press SPACE ~0.3 seconds *before* you start the next line.** The slide animates on; your first word lands as it settles.

---

## Script

```
═══════════════════════════════════════════════════════════
NEXOSTRAT INTRO V3 · 5 SPACES TOTAL
═══════════════════════════════════════════════════════════

────── PRE-ROLL ─────────────────────────────────────────────
TV está en SLIDE 0 (logo Nexostrat a la izquierda).
Mira a cámara. Sonrisa neutra. 5 segundos en silencio.

⟨SPACE 1⟩ ◄─────── PRESIONA AQUÍ
              ↓
        Slide cambia → SLIDE 1 (Hook)
        El número "1" anima a "20" durante 6 segundos.
        La barra de progreso se llena en paralelo.
              ↓
"¿Cuántas horas pierde tu equipo cada semana
 en tareas repetitivas?
 De esas que te quitan tiempo para crecer."

[respira 0.5s — el número llega a 20 aquí]

⟨SPACE 2⟩ ◄─────── PRESIONA AQUÍ
              ↓
        Slide cambia → SLIDE 2 (4-Stair reveal)
        DaVinci workflow: 4 PNG keyframes in
        overlays/slide-2_stairs/ crossfaded
        at each spoken verb:
          • state-1_estudiamos.png      at "estudiamos…"
          • state-2_est_ident.png       at "identificamos…"
          • state-3_plus_disena.png     at "diseño…"
          • state-4_all.png             at "implementación…"
              ↓
"En Nexostrat estudiamos tu operación,
 identificamos oportunidades y posibles procesos
 a automatizar.

 Apoyándonos de inteligencia artificial te acompañamos
 en el diseño y la implementación de soluciones
 a la medida de tu negocio."

[respira 0.5s]

⟨SPACE 3⟩ ◄─────── PRESIONA AQUÍ
              ↓
        Slide cambia → SLIDE 3 (Proof: 8–20 hrs)
              ↓
"La meta:
 que recuperes entre ocho y veinte horas a la semana…

 que puedas utilizar ese tiempo para decidir,
 vender, y crecer."

[respira 0.5s]

⟨SPACE 4⟩ ◄─────── PRESIONA AQUÍ
              ↓
        Slide cambia → SLIDE 4 (Diferencia)
              ↓
"Sin plantillas.
 Cada solución se construye sobre cómo funciona tu empresa."

[respira 0.5s]

⟨SPACE 5⟩ ◄─────── PRESIONA AQUÍ
              ↓
        Slide cambia → SLIDE 5 (CTA · WhatsApp)
              ↓
"Agenda una llamada de treinta minutos
 y te mostramos dónde están las oportunidades.

 Sin costo.
 Hablemos."

────── POST-ROLL ────────────────────────────────────────────
TV sigue en SLIDE 5 (WhatsApp + número).
Mira a cámara. Leve asentimiento. 5-10 segundos en silencio.
[CORTE]

═══════════════════════════════════════════════════════════
```

---

## Pace check

| Slide | Spoken word count | Estimated duration | Auto-reveal cues inside slide |
|---|---|---|---|
| 1 — Hook | ~18 | 6–7s | Number 1→20 anim runs 6s |
| 2 — Stairs | ~38 | 13–16s | 4 pills crossfaded at "estudiamos / identificamos / diseño / implementación" |
| 3 — Proof | ~23 | 8–9s | (static) |
| 4 — Diferencia | ~12 | 4–5s | (static) |
| 5 — CTA | ~17 | 6–7s | (static) |
| **Total speech** | **~108** | **~38–45s** | |

If after a real-TV dry-run the Slide-2 pill delays feel late/early, edit the three `animation-delay` values inside `tv-loop/index.html` (search for `@keyframes stairIn` then the three `.stage[data-slide="2"] .stair--*` rules immediately below it).

---

## On set — quick reminders

- **Press SPACE 0.3s before the next line.** Slide settles as your first word lands.
- **Pre-roll silence:** 5s minimum, neutral smile. Don't talk yet.
- **Post-roll silence:** 5-10s on Slide 5, then cut. Gives edit room.
- **Do 6+ full takes**, then isolated takes of each beat (just the hook, just the CTA, etc.) as cutaway insurance.
- **Slate aloud each take:** "Take N — full" before you start. Makes the edit 10× faster.
