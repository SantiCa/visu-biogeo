from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];D=R/'data'
p=D/'learning-taxonomy-audit.json';a=json.loads(p.read_text(encoding='utf8'));t=json.loads((D/'learning-taxonomy.json').read_text(encoding='utf8'));catalog=json.loads((D/'species.json').read_text(encoding='utf8'));bio=[i for i in catalog if i['kind'] in ['organismo','fosil']];a.update(rankedPhyla=sum(bool(t[i['id']]['ranks'].get('phylum')) for i in bio),commonNames=sum(bool(t[i['id']].get('commonName')) for i in bio),notApplicableIds=[i['id'] for i in bio if t[i['id']].get('nonTaxonomic')],pendingIds=[i['id'] for i in bio if not t[i['id']]['ranks'].get('phylum') and not t[i['id']].get('nonTaxonomic')]);p.write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf8')
text='''

## Clasificación y repaso por campos · versión 8.0

La pestaña **Clasificación**, junto a Catálogo, incluye todas las entradas. Despliega las ramas y después el nombre para ver dos fotos aprobadas y la ficha. Permite buscar nombres científicos o comunes, rangos y fórmulas. Las fichas sin imágenes o datos documentados indican el pendiente; no se ocultan entradas para aparentar cobertura completa.

**Practicar clasificación completa** está activado de inicio. En organismos y fósiles taxonómicos se responde nombre, filo o división, familia y género cuando están documentados. Para géneros sin especie determinada no se inventa un epíteto. Puedes contestar el nombre binomial o, si escribes el género por separado, el epíteto específico. Los nombres comunes documentados aparecen como pista, según lo solicitado. Después se muestra también clase y orden, con la fuente de la clasificación.

En minerales se pregunta la clase principal de Nickel–Strunz 9 y la fórmula cuando hay una fórmula evaluable. La ecuación acepta subíndices, agrupaciones equivalentes y agua de hidratación; distingue Co de CO. Las composiciones generales se indican expresamente. En este esquema el cuarzo se incluye en óxidos; esto no sustituye otros esquemas estructurales usados en docencia. En rocas se pregunta el grupo por origen y se muestra su composición: no se exige una fórmula química única. Asbesto y bauxita explican su naturaleza de hábito o mezcla.

Un fallo en cualquiera de los campos evaluados programa repaso a los diez minutos cuando pulsas **Continuar**. Los aciertos del nombre y de cada campo se conservan por separado en Progreso; se sincronizan en la misma cuenta. Los campos documentales pendientes no penalizan. La lectura del árbol no puntúa y no cambia la planificación.

Los rangos biológicos proceden de registros explícitos de iNaturalist, GBIF y Paleobiology Database, con enlaces por entrada. Las diferencias de circunscripción o nombre aceptado se muestran en la ficha; los rangos no se deducen de la posición en una lista. Los nombres vernáculos no son universales y pueden faltar. Las trazas, coprolitos y estromatolitos no se fuerzan a una clasificación corporal de un único productor.
'''
p=R/'README.md';s=p.read_text(encoding='utf8');s=s.split('\n## Clasificación y repaso por campos')[0]+text;p.write_text(s,encoding='utf8');print(json.dumps(a))
