db = db.getSiblingDB('dawdle');

db.createUser({
  'user': 'dawdle',
  'pwd': 'dawdle',
  'roles': [
    {
      'role': 'readWrite',
      'db': 'dawdle',
    },
  ],
});
