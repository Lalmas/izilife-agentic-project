-- Extension idempotente des référentiels utilisés par le premier appel LLM.
-- Aucun id n'est codé en dur : les parents/catégories sont résolus par string_id.

INSERT IGNORE INTO MusicStyle (name,string_id,parent_id) VALUES
('Metal','metal',(SELECT id FROM MusicStyle m WHERE m.string_id='rock')),
('Heavy metal','heavy-metal',(SELECT id FROM MusicStyle m WHERE m.string_id='rock')),
('Indie pop','indie-pop',(SELECT id FROM MusicStyle m WHERE m.string_id='pop')),
('Synthpop','synthpop',(SELECT id FROM MusicStyle m WHERE m.string_id='pop')),
('Drum and bass','drum-and-bass',(SELECT id FROM MusicStyle m WHERE m.string_id='electro')),
('Hard techno','hard-techno',(SELECT id FROM MusicStyle m WHERE m.string_id='techno')),
('Acid techno','acid-techno',(SELECT id FROM MusicStyle m WHERE m.string_id='techno')),
('Chanson française','chanson-francaise',NULL),
('Musique baroque','musique-baroque',(SELECT id FROM MusicStyle m WHERE m.string_id='musique-classique')),
('Musique de chambre','musique-de-chambre',(SELECT id FROM MusicStyle m WHERE m.string_id='musique-classique')),
('Opéra','opera',(SELECT id FROM MusicStyle m WHERE m.string_id='musique-classique')),
('Slam','slam',(SELECT id FROM MusicStyle m WHERE m.string_id='rap')),
('Reggae','reggae',NULL),
('Dub','dub',(SELECT id FROM MusicStyle m WHERE m.string_id='reggae')),
('Musiques du monde','musiques-du-monde',NULL);

INSERT IGNORE INTO Dance (name,string_id,is_couple_activity_dance) VALUES
('Sévillanes','sevillanes',1),
('Lindy hop','lindy-hop',1),
('West coast swing','west-coast-swing',1),
('Rock 4 temps','rock-4-temps',1),
('Rock 6 temps','rock-6-temps',1),
('Danse africaine','danse-africaine',0),
('Danse irlandaise','danse-irlandaise',0),
('Danse indienne','danse-indienne',0),
('Danse tahitienne','danse-tahitienne',0),
('Claquettes','claquettes',0),
('Heels','heels',0),
('Commercial dance','commercial-dance',0),
('Danse inclusive','danse-inclusive',0);

INSERT IGNORE INTO Sport (name,string_id,sport_category_id,collective_sport) VALUES
('Escalade','escalade',(SELECT id FROM SportCategory WHERE string_id='autres-sports-athletiques'),0),
('Pétanque','petanque',(SELECT id FROM SportCategory WHERE string_id='sports-techniques'),0),
('Tir à l arc','tir-a-l-arc',(SELECT id FROM SportCategory WHERE string_id='sports-techniques'),0),
('Escrime','escrime',(SELECT id FROM SportCategory WHERE string_id='sports-de-combat'),0),
('Karaté','karate',(SELECT id FROM SportCategory WHERE string_id='sports-de-combat'),0),
('Kick-boxing','kick-boxing',(SELECT id FROM SportCategory WHERE string_id='sports-de-combat'),0),
('Muay-thaï','muay-thai',(SELECT id FROM SportCategory WHERE string_id='sports-de-combat'),0),
('Hockey sur glace','hockey-sur-glace',(SELECT id FROM SportCategory WHERE string_id='sports-de-glace'),1),
('Hockey sur gazon','hockey-sur-gazon',(SELECT id FROM SportCategory WHERE string_id='sports-collectifs'),1),
('Futsal','futsal',(SELECT id FROM SportCategory WHERE string_id='sports-collectifs'),1),
('Volley-ball','volley-ball',(SELECT id FROM SportCategory WHERE string_id='sports-collectifs'),1),
('Baseball','baseball',(SELECT id FROM SportCategory WHERE string_id='sports-collectifs'),1),
('Softball','softball',(SELECT id FROM SportCategory WHERE string_id='sports-collectifs'),1),
('Canoë-kayak','canoe-kayak',(SELECT id FROM SportCategory WHERE string_id='sports-nautiques'),0),
('Stand up paddle','stand-up-paddle',(SELECT id FROM SportCategory WHERE string_id='sports-nautiques'),0),
('Voile','voile',(SELECT id FROM SportCategory WHERE string_id='sports-nautiques'),0),
('Triathlon','triathlon',(SELECT id FROM SportCategory WHERE string_id='sports-combines'),0),
('Trail','trail',(SELECT id FROM SportCategory WHERE string_id='sport-a-pieds'),0),
('Course orientation','course-orientation',(SELECT id FROM SportCategory WHERE string_id='sport-a-pieds'),0),
('Roller','roller',(SELECT id FROM SportCategory WHERE string_id='sports-techniques'),0),
('Skateboard','skateboard',(SELECT id FROM SportCategory WHERE string_id='sports-techniques'),0);

