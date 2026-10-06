import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = process.env.OUTPUT_DIR || HERE;
const figPath = path.join(OUT, 'figures', 'occupancy-networks-figure-1.png');
const ppt = Presentation.create({ slideSize: { width: 1280, height: 720 } });
const slide = ppt.slides.add();
slide.background.fill = '#FFFFFF';
const ink = '#17212B', secondary = '#52616D', accent = '#1478A5', pale = '#F0F6F8', rule = '#D5DCE1';
const font = 'Hiragino Sans';

function box(name, x, y, w, h, fill='none', stroke='none', strokeWidth=0, geometry='rect') {
  return slide.shapes.add({ geometry, name,
    position: { left:x, top:y, width:w, height:h }, fill,
    line: { style:'solid', fill:stroke, width:strokeWidth } });
}
function label(name, value, x, y, w, h, size, color=ink, bold=false, alignment='left') {
  const s=box(name,x,y,w,h,'none','none',0,'textbox');
  s.text=value;
  s.text.style={ fontSize:size, typeface:font, color, bold, alignment,
    verticalAlignment:'middle', wrap:'square', autoFit:'none',
    insets:{top:0,right:0,bottom:0,left:0} };
  return s;
}

// Takeaway title and subtitle preserve the Codex Grid #5 title + two-column structure.
label('title','形を点・格子で出力せず、関数の境界で表す',56,38,1168,60,48,ink,true);
label('subtitle','Occupancy Networks：占有確率の境界を3D表面とし、必要時にメッシュ化する',58,108,1160,36,23,secondary);

// Source figure is the original Figure 1, cropped from the CVF Open Access paper at 300 dpi.
const bytes=await fs.readFile(figPath);
const imageBytes=bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength);
slide.images.add({
  blob:imageBytes, contentType:'image/png', alt:'原論文 Figure 1：Voxel・Point・Mesh・Occupancy Network の表現比較',
  fit:'contain', position:{left:54,top:186,width:675,height:372},
});
label('figure-source','原図：Mescheder et al., Fig. 1（CVPR 2019, p. 4460）',56,560,666,24,15,secondary);

// Explanation column.
box('column-divider',754,184,1.5,372,rule,'none',0);
label('mechanism-heading','表現の切替',790,187,425,40,32,accent,true);
label('function-equation','fθ(p, x) → 占有確率',790,246,425,42,32,ink,true);
label('query-description','入力：3D座標 p ＋ 観測 x\n出力：その点が形状の内側にある確率',790,298,421,82,22,secondary);
label('boundary-heading','分類境界 ＝ 3D表面',790,396,425,39,32,ink,true);
label('boundary-description','固定した格子の値ではなく、連続関数の境界として形状を表す。',790,441,421,67,22,secondary);
label('extraction-note','利用時は関数を評価し、MISEで等値面をメッシュ抽出。',790,516,421,58,22,secondary);

// Boundary and key nuance: implicit representation changes when/how a mesh is produced.
box('takeaway-band',56,603,1168,48,pale,'none',0);
box('takeaway-accent',56,603,5,48,accent,'none',0);
label('takeaway','変わるのは形の持ち方。Occupancy Networks も、推論時にはメッシュを抽出できる。',75,610,1135,34,22,ink,true);
label('source-footer','Mescheder, Oechsle, Niemeyer, Nowozin & Geiger · “Occupancy Networks” · CVPR 2019 · Fig. 1, §3.1, §3.3',56,664,1168,24,13,secondary);

slide.speakerNotes.textFrame.setText([
  '[Sources]',
  'Lars Mescheder, Michael Oechsle, Michael Niemeyer, Sebastian Nowozin, and Andreas Geiger. “Occupancy Networks: Learning 3D Reconstruction in Function Space.” CVPR 2019, pp. 4460–4470. DOI: 10.1109/CVPR.2019.00459.',
  'https://openaccess.thecvf.com/content_CVPR_2019/papers/Mescheder_Occupancy_Networks_Learning_3D_Reconstruction_in_Function_Space_CVPR_2019_paper.pdf',
  'Figure: original Fig. 1, p. 4460. Claims on fθ(p,x), occupancy probability, and decision boundary: §3.1. Mesh extraction with MISE: §3.3. The visible figure is cropped only to remove the surrounding article text; its panels, labels, and contents are unchanged.',
  '[/Sources]',
]);

const pptx=await PresentationFile.exportPptx(ppt);
await pptx.save(path.join(OUT,'occupancy-network-transition.pptx'));
const preview=await ppt.export({slide,format:'png',scale:2});
await fs.writeFile(path.join(OUT,'occupancy-network-transition.png'),new Uint8Array(await preview.arrayBuffer()));
const inspection=await ppt.inspect({kind:'slide,textbox,shape,image,notes',maxChars:20000});
await fs.writeFile(path.join(OUT,'inspection.ndjson'),inspection.ndjson);
