export const NOTE_FILES=['class-notes.json','order-notes.json','family-notes.json','genus-notes.json','species-notes.json','other-notes.json'];

export function assembleNotes(banks){
 const profiles={},families={},taxa={},entries={};
 for(const bank of banks){
  for(const [key,taxon] of Object.entries(bank.taxa)){
   if(taxa[key])throw Error('Taxón duplicado en las fichas: '+key);
   taxa[key]=taxon;
   if(taxon.rank==='family'&&taxon.note)families[taxon.name]=taxon.note;
  }
  for(const [id,entry] of Object.entries(bank.entries)){
   if(entries[id])throw Error('Entrada duplicada en las fichas: '+id);
   entries[id]=entry;
   if(entry.profile)profiles[id]=entry.profile;
  }
 }
 const profilesByName=new Map();
 for(const entry of Object.values(entries))if(entry.profile&&!profilesByName.has(entry.name))profilesByName.set(entry.name,entry.profile);
 // A generic branch can use a profile of that exact name, never one of its species.
 for(const taxon of Object.values(taxa)){
  const profile=profilesByName.get(taxon.name);
  if(profile&&!taxon.note)taxa[taxon.rank+':'+taxon.name]={...taxon,note:profile};
 }
 return {profiles,families,taxa};
}

export async function loadNotes(fetchJson){
 return assembleNotes(await Promise.all(NOTE_FILES.map(name=>fetchJson('./data/'+name))));
}

export function taxonNote(taxa,rank,name){return taxa?.[rank+':'+name];}

export function taxonGuide(taxa,rank,name){
 const taxon=taxonNote(taxa,rank,name),note=taxon?.note;
 if(taxon?.guide)return taxon.guide;
 if(!note?.description)return undefined;
 return {name,text:note.description,contrast:(note.diagnostics||[]).join(' '),source:note.sources?.[0]?.url||''};
}
