db = db.getSiblingDB('mixir');
db.createUser({
  user: 'root',
  pwd: 'password',
  roles: [{ role: 'readWrite', db: 'mixir' }]
});
db.mycollection.insert({ name: 'MY_SAMPLE_DATA' });