// Draws an illustrated item picture. Used only when an item has no real photo.
window.drawItem=(k,bg)=>{const f='#f6f1e7',g='#1f3a2c',s={
bag:`<rect x="50" y="85" width="100" height="75" rx="10" fill="${f}"/><path d="M75 85v-15a25 25 0 0150 0v15" fill="none" stroke="${f}" stroke-width="8"/><rect x="92" y="105" width="16" height="14" fill="${g}"/>`,
keys:`<circle cx="75" cy="95" r="26" fill="none" stroke="${f}" stroke-width="10"/><path d="M96 105l60 40m-18-12l12-12m-30 0l12-12" stroke="${f}" stroke-width="10" fill="none"/>`,
wallet:`<rect x="40" y="75" width="120" height="80" rx="10" fill="${f}"/><rect x="118" y="100" width="42" height="28" rx="6" fill="${g}"/><circle cx="132" cy="114" r="5" fill="${f}"/>`,
phone:`<rect x="68" y="50" width="64" height="115" rx="12" fill="${f}"/><rect x="76" y="62" width="48" height="80" rx="4" fill="${g}"/>`,
ring:`<circle cx="100" cy="105" r="38" fill="none" stroke="${f}" stroke-width="12"/><path d="M86 62l14-14 14 14-14 12z" fill="${f}"/>`,
glasses:`<circle cx="70" cy="105" r="26" fill="none" stroke="${f}" stroke-width="8"/><circle cx="132" cy="105" r="26" fill="none" stroke="${f}" stroke-width="8"/><path d="M96 102h10" stroke="${f}" stroke-width="8"/>`,
umbrella:`<path d="M40 105a60 55 0 01120 0z" fill="${f}"/><path d="M100 105v50a10 10 0 01-20 0" fill="none" stroke="${f}" stroke-width="8"/>`}[k];
return `<svg viewBox="0 0 200 200" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="200" height="200" fill="${bg}"/><circle cx="40" cy="30" r="60" fill="#fff" opacity=".1"/>${s}</svg>`};
