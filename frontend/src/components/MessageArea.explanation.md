# Vertically Centering Text in `MessageArea.tsx`

## The goal

The chat input textarea should show its placeholder/typed text vertically
centered inside its box, while still keeping a fixed minimum height
(`min-h-15`, 60px) so the input bar doesn't look cramped when empty.

## Why the naive approach fails

The first instinct is to just add flexbox utilities directly to the
`<textarea>`:

```tsx
<textarea className="flex flex-col justify-center min-h-15 ..." />
```

This looks reasonable, but **it does nothing**. Here's why:

- `display: flex` changes how an element lays out its **DOM children**.
- A `<textarea>` has no DOM children — its visible text (typed value or
  placeholder) is rendered internally by the browser as part of the form
  control's own "replaced" UA (user-agent) rendering, not as child nodes you
  can flex, align, or otherwise target with layout properties.
- So `justify-content`, `align-items`, etc. applied *to the textarea itself*
  have no effect on where its internal text sits. It will always start at
  the top-left of the content box, regardless of how tall the box is.

This is a well-known CSS limitation shared by other form controls
(`<input>`, `<button>`'s internal label rendering, etc. behave a bit
differently, but `<textarea>` specifically has zero support for aligning its
own text vertically via CSS).

## Why a fixed `min-height` makes it worse

With the original markup:

```tsx
<textarea className="min-h-15 py-2 ..." />
```

- `min-h-15` = 60px minimum box height.
- One line of text (`text-base`, `leading-normal`) is about 24px tall.
- `py-2` adds 8px top + 8px bottom = 16px.
- Content + padding = 40px, but the box is forced to be 60px.
- Result: 20px of unused space, all of it pushed to the *bottom*, because
  text always renders from the top. The text visibly sits above center.

Shrinking `min-h-15` down to match the content height (`min-h-10`, i.e. 40px)
"fixes" the visual symptom, but only by making the minimum height equal to
the content height — at that point there's no free space left to be
off-center in. That's a workaround, not a fix: it can't preserve `min-h-15`
while still centering, which was a requirement.

## The actual fix: separate "the box" from "the text"

Since the textarea itself can never center its internal text, the solution
is to stop asking it to. Instead:

1. Move the border, background, rounding, and `min-h-15` onto a **wrapper
   `<div>`** that *does* support normal flex layout (it has a real DOM
   child: the textarea).
2. Make the wrapper a flex container with `items-center`.
3. Let the `<textarea>` size itself to its **content** (`field-sizing-content`),
   strip its border/outline so it looks invisible, and let it act as a flex
   *item* inside the wrapper.

```tsx
<div className="flex min-h-15 max-h-32 items-center overflow-y-auto rounded-lg border-2 border-gray-300 px-3">
  <textarea
    className="field-sizing-content max-h-full w-full resize-none overflow-y-auto border-none py-2 leading-normal outline-none"
    ...
  />
</div>
```

### Why this works

- `field-sizing-content` (a Tailwind utility for the CSS `field-sizing:
  content` property) makes the **textarea's own box** shrink-wrap to its
  content — one line of text means a ~40px-tall textarea, not a 60px one.
- Flexbox alignment (`items-center` on the wrapper) operates on the
  textarea **as a whole box** — a flex item — not on the text inside it.
  This is the crucial distinction: we're not centering text-in-a-textarea
  anymore, we're centering a small textarea-box inside a taller div, which
  is a completely ordinary, well-supported flex operation.
- Visually, the two are indistinguishable: the wrapper has the same border
  and rounded corners the textarea used to have, so it still reads as "one
  input box." But internally, only the wrapper enforces `min-h-15`; the
  textarea just gets vertically centered inside it like any other flex
  child would.
- As the user types more lines, `field-sizing-content` grows the textarea
  box, which grows the amount of space it occupies inside the flex
  container — eventually filling and then exceeding the wrapper's
  `min-h-15`, up to the `max-h-32` cap (mirrored on the textarea via
  `max-h-full` so it doesn't overflow its own parent).

## Summary

| Layer | Responsibility |
|---|---|
| Outer `<div>` | Visual chrome: border, rounded corners, `min-h-15`/`max-h-32`, and centering its child via `flex items-center` |
| Inner `<textarea>` | Content sizing only (`field-sizing-content`), no visible border/outline, grows with typed text |

The key insight: **you can't vertically center text inside a textarea with
CSS, but you can vertically center a textarea (as a box) inside a flex
container.** Splitting "the box you see" (the div) from "the input that
holds text" (the textarea) sidesteps the limitation entirely.
