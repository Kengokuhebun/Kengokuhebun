"""Build product.old-pdp-gifts.json: the live old-pdp template with ONE change,
the 4-free-gifts block inside The Ninu Kit card. Optional --fix-dispenser-price
also corrects the Dispenser Only display price ($34.99 -> $39.99, the real Shopify price)."""
import json, re, sys
P = 'https://cdn.shopify.com/s/files/1/1084/3894/6122/files/'
raw = open('theme-original/product.old-pdp.json').read()
m = re.match(r'^\s*(/\*.*?\*/)?\s*', raw, re.S)
head, body = (m.group(1) or ''), raw[m.end():]
tpl = json.loads(body)
sec = tpl['sections']['custom_liquid_QQwhib']['settings']
liq = sec['custom_liquid']

CSS = ('.ninu-gifts{margin:12px 0 4px;padding:12px;border:1.5px solid var(--gold);border-radius:12px;'
 'background:linear-gradient(180deg,#FEFAF3,#F8EEDD)}'
 '.ninu-gifts-h{display:flex;align-items:baseline;justify-content:space-between;gap:8px;margin-bottom:10px}'
 '.ninu-gifts-h b{font-size:14px;letter-spacing:.06em;text-transform:uppercase;font-weight:800;color:var(--acc-2)}'
 '.ninu-gifts-h span{font-size:11.5px;color:var(--muted);font-weight:600}'
 '.ninu-gg{display:grid;grid-template-columns:1fr 1fr;gap:10px}'
 '.ninu-g{position:relative;background:var(--white);border:1px solid var(--line);border-radius:10px;padding:8px 8px 10px}'
 '.ninu-g-i{display:flex;align-items:center;justify-content:center;aspect-ratio:1/.72;border-radius:8px;'
 'background:#F1E7D8;overflow:hidden;margin-bottom:8px}'
 '.ninu-g-i img{width:100%;height:100%;object-fit:cover}'
 '.ninu-g em{position:absolute;top:14px;left:14px;background:var(--sage);color:#fff;font-style:normal;font-size:10px;'
 'font-weight:800;letter-spacing:.1em;padding:3px 7px;border-radius:4px}'
 '.ninu-g b{display:block;font-size:13.5px;line-height:1.25;font-weight:800}'
 '.ninu-g small{display:block;font-size:11.5px;color:var(--muted);line-height:1.3;margin-top:2px}'
 '@media(min-width:901px){.ninu-gg{grid-template-columns:repeat(4,1fr);gap:8px}.ninu-g{padding:6px 6px 9px}'
 '.ninu-g b{font-size:12px}.ninu-g small{font-size:10.5px}.ninu-g em{top:11px;left:11px;font-size:9px}}')

def g(img, alt, style, title, sub):
    return (f'<div class="ninu-g"><span class="ninu-g-i"><img src="{P}{img}" alt="{alt}" loading="lazy" '
            f'style="{style}"></span><em>FREE</em><b>{title}</b><small>{sub}</small></div>')
GIFTS = ('\n              <div class="ninu-gifts"><div class="ninu-gifts-h"><b>+ 4 free gifts</b><span>with every kit</span></div>'
 '<div class="ninu-gg">'
 + g('scalp-massager-tile-cream-removebg-preview.png','Scalp massager','object-fit:contain;transform:translate(6%,5%) scale(1.15)','Scalp massager','For wash day')
 + g('Cosmetic_pouch_product_photograph_a8983e00-removebg-preview.png','Bedside pouch','object-fit:contain;transform:scale(1.12)','Bedside pouch','Your routine, within reach')
 + g('guide-tile.png','Guide','transform:translate(9%,8%) scale(1)','The Scalp Routine That Sticks','Guide, emailed to you')
 + g('tracker-tile.png','Tracker','transform:translate(8%,9%) scale(.9)','Ninu Night Tracker','30-night tracker, emailed to you')
 + '</div></div>')

gifts = '--no-gifts' not in sys.argv
# 1) CSS: append inside the first <style> block
if gifts: assert liq.count('</style>') >= 1
if gifts: liq = liq.replace('</style>', CSS + '</style>', 1)

# 2) HTML: after the Kit card's perks list (the first .ninu-tier-perks, which belongs to data-tier="kit")
if gifts:
  kit = liq.index('data-tier="kit"')
  perks = liq.index('<div class="ninu-tier-perks">', kit)
  end = liq.index('</div>', liq.index('</ul>', perks)) + len('</div>')
  assert perks < liq.index('data-tier="dispenser"'), 'perks not inside kit card'
  liq = liq[:end] + GIFTS + liq[end:]

fix = '--fix-dispenser-price' in sys.argv
if fix:
    n0 = liq.count('34.99') + liq.count('3499')
    liq = liq.replace('data-price="34.99"', 'data-price="39.99"').replace('<span class="ninu-price">$34.99</span>', '<span class="ninu-price">$39.99</span>')
    liq = re.sub(r"(dispenser:\s*\{ title: 'Ninu Dispenser', price: )3499", r'\g<1>3999', liq)
    assert '34.99' not in liq and 'price: 3499' not in liq, 'leftover old dispenser price'

sec['custom_liquid'] = liq
out = (head + '\n' if head else '') + json.dumps(tpl, indent=2, ensure_ascii=False) + '\n'
name = sys.argv[1]
open(name, 'w').write(out)
print('wrote', name, 'gift block added' if gifts else 'no gift block', 'dispenser price fixed' if fix else '')
