import {selectImagePair} from './engine.mjs';
export const PHOTO_USES={unknown:'Sin evaluar para examen',diagnostic:'Rasgos diagnósticos suficientes',detail:'Detalle o parte aislada',context:'Contexto / no apta para identificar',insufficient:'Evaluada · rasgos insuficientes o ambiguos'};
export function photoUse(image,overrides={}){return overrides[image.reviewKey]?.value?.use||image.examUse||'unknown';}
export function eligibleExamPhotos(images,mode,overrides={},detailsOnly=false){return images.filter(im=>mode==='andalucia'?photoUse(im,overrides)==='diagnostic':mode==='madrid'?(detailsOnly?photoUse(im,overrides)==='detail':!['context','insufficient'].includes(photoUse(im,overrides))):true);}
export function selectExamPhotos(images,{mode='general',overrides={},detailsOnly=false,previous=[],rng=Math.random}={}){
 const bank=eligibleExamPhotos(images,mode,overrides,detailsOnly);
 if(mode==='andalucia'&&bank.length<2)return [];
 if(mode==='madrid'){
  const details=bank.filter(im=>photoUse(im,overrides)==='detail');
  if(details.length&&(detailsOnly||rng()<.65))return selectImagePair(details,previous,rng);
  const whole=bank.filter(im=>photoUse(im,overrides)!=='detail');
  return selectImagePair(whole.length?whole:details,previous,rng);
 }
 return selectImagePair(bank,previous,rng);
}
